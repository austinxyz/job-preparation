---
title: Distributed Training Frameworks
category: tech/ai-infra
tags: [pytorch, deepspeed, distributed-training, data-parallelism, model-parallelism, megatron, zero, fsdp]
status: in-progress
priority: high
last_updated: 2026-04-07
created_from_jd: [[positions/Sample AI Infra Manager - Test Co]]
---

# Distributed Training Frameworks

## Knowledge Map
- Prerequisites（前置知识）：[[GPU Cluster Management]], [[NCCL and Collective Communication]]
- Related Topics（延伸话题）：[[Model Parallelism]], [[Pipeline Parallelism]], [[LLM Fundamentals]], [[GPU Fleet Cost Optimization]]
- Management（管理关联）：[[AI Research Team Structure]]

## Core Concepts

- **DataParallel vs DistributedDataParallel（DP vs DDP）**: `DataParallel` is single-process, multi-threaded — all GPUs share one Python process, so the GIL limits throughput and it only works on one machine. `DistributedDataParallel` (DDP) spawns one process per GPU, eliminating GIL contention. DDP is almost always preferred: faster even on a single machine, and scales across nodes.
- **How DDP works**: Each process holds a full copy of the model. During the forward and backward passes, computation is independent per process. After backward, DDP fires an autograd hook per parameter that triggers an all-reduce operation (via NCCL) to average gradients across all processes. All processes then apply the same gradient update — keeping models in sync without a central parameter server.
- **Memory breakdown during training（显存组成）**: Training requires more than just model weights. For mixed-precision training (fp16 forward, fp32 optimizer): ~2 bytes fp16 weights + 2 bytes fp16 gradients + 4 bytes fp32 master weights + 8 bytes fp32 Adam optimizer states (momentum + variance) = ~16–18 bytes per parameter. A 7B model needs ~112–126 GB just for these — far beyond a single A100 80 GB.
- **ZeRO — Zero Redundancy Optimizer**: Instead of replicating all parameters, gradients, and optimizer states on every GPU (standard DDP), ZeRO partitions them equally across GPUs. Each GPU stores only its shard and fetches missing pieces during the forward/backward pass via all-gather / reduce-scatter collectives. Three stages: Stage 1 (shard optimizer states only, ~4× memory reduction), Stage 2 (+ gradient sharding, ~8×), Stage 3 (+ parameter sharding, memory scales linearly with GPU count). ZeRO requires no changes to model code — only training loop changes.
- **ZeRO-Offload**: Extends ZeRO by moving optimizer states (and optionally optimizer computation) to CPU RAM. GPU handles forward/backward; CPU handles weight updates. Allows training models that don't fit on GPU at all — e.g., running t5-3b fine-tuning on a single 24 GB GPU that would otherwise OOM. Tradeoff: PCIe bandwidth between CPU and GPU becomes a bottleneck for very large offload ratios.
- **GPU memory fragmentation（显存碎片化）**: Repeated allocation and de-allocation of tensors of different sizes creates "holes" — many GBs unused but no contiguous block large enough to allocate. OOM errors with `X GiB allocated; only Y MiB free` where X+Y << total capacity are a symptom. DeepSpeed mitigates this by managing its own memory pool, separating long-lived allocations (model weights) from short-lived ones (activations, temporary buffers).
- **FSDP (Fully Sharded Data Parallel)**: PyTorch's native implementation of ZeRO Stage 3, integrated into `torch.distributed`. Lower setup overhead than DeepSpeed (no separate config file), but fewer advanced features (no CPU offload equivalent to DeepSpeed's, no 1-bit Adam). Good choice when you want sharding without adding the DeepSpeed dependency.
- **Beyond data parallelism — model parallelism**: When a model is too large to fit on one GPU even with ZeRO, you must split the model itself. Tensor parallelism (Megatron-LM style) splits individual weight matrices across GPUs — high communication overhead, requires specialized model code. Pipeline parallelism splits layers into stages across GPUs — inter-GPU bubble time is the key inefficiency. In practice, large-scale training (GPT-4 class) uses 3D parallelism: data parallel × tensor parallel × pipeline parallel simultaneously.
- **Choosing the right strategy**: Models fitting on 1 GPU → DDP. Models needing 2–8 GPUs' combined memory → FSDP or DeepSpeed ZeRO Stage 2/3. Models requiring CPU offload → DeepSpeed ZeRO-Offload. Extremely large models (100B+) → Megatron-style tensor + pipeline parallelism. As an infra manager, the decision determines cluster topology, networking requirements (IB vs Ethernet), and training throughput per dollar.
- **torch.distributed key concepts（基础概念）**: Group = a subset of all processes that participate in collective operations. Backend = the communication library used (NCCL for GPU-to-GPU on the same/nearby nodes, Gloo for CPU or cross-platform, MPI for HPC environments). world_size = total number of processes in the group. Rank = unique integer ID assigned to each process (0 to world_size−1). Every DDP job requires setting MASTER_ADDR and MASTER_PORT so processes can rendezvous.
- **Collective communication primitives（集合通信原语）**: Six core operations underlie all distributed training: `broadcast` (one→all, same tensor), `scatter` (one→all, different chunks), `gather` (all→one), `reduce` (all→one with aggregation), `all_reduce` (all→all with aggregation — the core of DDP gradient sync), `all_gather` (all→all, no aggregation — used in ZeRO Stage 3 to fetch parameter shards). Knowing which primitive is used where explains the communication overhead profile of each parallelism strategy.
- **Blocking vs non-blocking P2P（阻塞与非阻塞）**: Point-to-point `send`/`recv` are blocking — the process halts until the transfer completes. `isend`/`irecv` are non-blocking — returns a request handle immediately; call `req.wait()` before accessing the tensor. Non-blocking P2P enables overlapping computation with communication (e.g., send activations to the next pipeline stage while computing gradients for the current stage).
- **DDP gradient bucketing（梯度分桶）**: DDP groups parameters into buckets (default `bucket_cap_mb=25 MB`) and triggers all-reduce as soon as a bucket is full during backward, rather than waiting for all gradients to be ready. This overlaps gradient communication with backward computation for earlier layers — reducing the idle time between the last gradient being computed and the optimizer step. Tuning bucket size affects the communication/compute overlap tradeoff.
- **Fault-tolerant training with torch.elastic**: Standard DDP crashes if any process fails. `torch.elastic` (torchrun) allows workers to dynamically join and leave during training — useful for spot/preemptible GPU instances where nodes can be reclaimed. Requires the model checkpoint to be saved frequently enough to resume from, and the training loop to implement elastic checkpoint logic.

## Key Questions

**Q: Explain how DDP synchronizes gradients — what happens under the hood after the backward pass?**
Answer framework: Each process computes its own gradients independently. DDP registers autograd hooks per parameter; when backward completes, hooks trigger all-reduce via NCCL to average gradients across all processes. All processes end up with identical averaged gradients and apply the same update — no parameter server needed. Key insight: communication (all-reduce) overlaps with computation (backward pass for earlier layers), reducing the overhead vs a naive synchronize-then-update approach.

**Q: What are the three ZeRO stages and what does each shard?**
Answer framework: Stage 1 shards optimizer states (Adam's momentum + variance) — ~4× memory reduction with no communication overhead increase. Stage 2 additionally shards gradients — ~8× reduction, slight reduce-scatter overhead. Stage 3 additionally shards model parameters — memory scales as 1/N where N = number of GPUs, but requires all-gather before every forward pass (extra communication). Most production training uses Stage 2 or 3; Stage 3 is necessary for the largest models.

**Q: A researcher wants to fine-tune a 13B parameter model and has 4×A100 80GB GPUs. What training strategy would you recommend?**
Answer framework: First calculate memory: 13B params × ~16 bytes = ~208 GB total — exceeds 4×80 GB (320 GB) if you also account for activations and batch data. With LoRA/QLoRA you can reduce trainable param memory drastically. For full fine-tune: use DeepSpeed ZeRO Stage 2 or 3 (shards optimizer states + gradients/params across 4 GPUs), plus gradient checkpointing to trade compute for activation memory. ZeRO Stage 3 with fp16 makes 13B feasible on 4×A100. If still tight: ZeRO-Offload to CPU. Distinguish the problem (memory vs throughput) before recommending.

**Q: When would you choose DeepSpeed over PyTorch FSDP?**
Answer framework: FSDP is simpler to set up (native PyTorch, no config file) and sufficient for ZeRO Stage 3 sharding. Choose DeepSpeed when you need: ZeRO-Offload (CPU offload), advanced communication optimizations (1-bit Adam, sparse attention), or the ecosystem of DeepSpeed extensions (inference optimization, curriculum learning). For most fine-tuning use cases FSDP is enough; DeepSpeed adds value at the frontier of model scale or for optimizing training cost at large GPU counts.

**Q: What is GPU memory fragmentation and how do you diagnose and fix it?**
Answer framework: Fragmentation occurs when free memory exists but not in a contiguous block large enough to satisfy an allocation request. Symptom: OOM with `X GiB allocated, only Y MiB free` where Y << expected free. Fix options: use DeepSpeed's memory manager (separates long- vs short-lived allocations), set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (PyTorch 2.0+ feature), or reduce batch size to lower peak memory. For infra managers: recurring fragmentation OOMs signal that the training job's memory access pattern needs profiling with `torch.cuda.memory_snapshot()`.

**Q: What are the six collective communication primitives in PyTorch? Which ones are used in DDP gradient synchronization, and which in ZeRO Stage 3?**
Answer framework: The six are broadcast, scatter, gather, reduce, all_reduce, all_gather. DDP uses all_reduce after each backward pass to average gradients across all ranks — every process ends with the same averaged gradient. ZeRO Stage 3 uses all_gather before the forward pass to reconstruct full parameter tensors from shards, and reduce_scatter after backward to aggregate gradients and re-shard them. Knowing this reveals why ZeRO Stage 3 has higher communication volume than DDP: it does both all_gather and reduce_scatter per layer, vs DDP's single all_reduce per parameter.

**Q: What is DDP gradient bucketing (bucket_cap_mb) and how does it affect training performance?**
Answer framework: DDP groups parameters into ~25 MB buckets (tunable via bucket_cap_mb). As soon as all gradients in a bucket are ready during backward, DDP fires the all_reduce for that bucket — overlapping gradient communication with backward computation for remaining layers. If buckets are too small, you get many small all_reduce calls with high per-call overhead. If too large, you lose the overlap benefit (must wait for a full large bucket). Tuning bucket_cap_mb is a practical lever for improving DDP throughput on high-latency networks.

**Q: What is 3D parallelism and when is it necessary?**
Answer framework: 3D parallelism combines data parallelism (replicate model, shard data), tensor parallelism (shard weight matrices within a layer across GPUs), and pipeline parallelism (shard layers across GPU groups). Each dimension addresses a different constraint: data parallelism scales throughput, tensor parallelism fits large layers that won't shard enough via ZeRO, pipeline parallelism handles extreme depth. Necessary for 100B+ parameter models trained from scratch (GPT-4, LLaMA 3 405B). Complexity cost is high: debugging requires understanding all three communication patterns simultaneously. Megatron-LM is the de facto library for 3D parallelism.

## Summary

Distributed training frameworks are the primary infrastructure layer between a researcher's model code and the cluster's GPU hardware. The foundational building block is **DistributedDataParallel (DDP)**: each GPU runs an identical copy of the model on a different data shard, and NCCL all-reduce synchronizes gradients after each backward pass. DDP is fast and simple, but requires the full model to fit on a single GPU — which fails for anything beyond ~7B parameters in full precision.

For larger models, **ZeRO** (Zero Redundancy Optimizer, implemented in DeepSpeed and PyTorch FSDP) eliminates memory redundancy by partitioning optimizer states, gradients, and model parameters across GPUs instead of replicating them. ZeRO Stage 2 (shard optimizer states + gradients) is the practical sweet spot for most fine-tuning: it achieves ~8× memory reduction per GPU with modest communication overhead, making 13B–70B parameter fine-tuning accessible on 8–16 GPU nodes. **ZeRO-Offload** extends this further by moving optimizer states to CPU RAM, enabling billion-parameter training even on a single GPU at the cost of PCIe bandwidth. PyTorch FSDP covers ZeRO Stage 3 natively; DeepSpeed adds CPU offload, memory management, and advanced optimizer variants (1-bit Adam).

For extremely large models (100B+) trained from scratch, ZeRO alone is insufficient because even sharded parameters don't fit — you need **3D parallelism**: data parallel × tensor parallel (Megatron-style weight matrix splitting) × pipeline parallel (layer-stage splitting). This is the domain of Megatron-LM and custom training stacks. As an AI Infra Manager, the practical decisions are: (1) DDP vs FSDP/DeepSpeed (model size threshold ~7B for A100s), (2) which ZeRO stage to use (Stage 2 default, Stage 3 + offload when tight), and (3) whether 3D parallelism is justified by model scale. These choices directly determine cluster topology, networking requirements (InfiniBand vs Ethernet), and training cost per token.

## Raw Material
- [[raw_material/tech/ai-infra/Distributed Training Frameworks - resources]]
- [[raw_material/tech/ai-infra/PyTorch 源码解读之分布式训练]]
