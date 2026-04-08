---
title: LLM Fundamentals
category: tech/ai-basics
tags: [llm, transformer, attention, pretraining, finetuning, lora, peft, tokenization, embedding, decoder-only]
status: in-progress
priority: high
last_updated: 2026-04-07
created_from_jd:
---

# LLM Fundamentals

## Knowledge Map
- Prerequisites（前置知识）：[[Deep Learning Basics]], [[Attention Mechanism]]
- Related Topics（延伸话题）：[[LLM Inference Optimization]], [[Post-Training and RLHF]], [[Distributed Training Frameworks]], [[AI Agents Architecture]]
- Management（管理关联）：[[AI Evaluation and Testing]]

## Core Concepts

- **Evolution of architectures（技术演进）**: Linear regression → CNN/RNN for patterns → LSTM for sequences → Transformer. RNN/LSTM suffer from gradient vanishing on long sequences and cannot parallelize. Transformer's self-attention solves both problems simultaneously.
- **Self-attention mechanism（自注意力）**: Each token computes Q (query), K (key), V (value) vectors. Attention score = softmax(QKᵀ / √d_k) × V. Any two positions can attend to each other directly regardless of distance — no sequential dependency. O(n²) compute in sequence length.
- **Transformer architecture variants**: Encoder-decoder (T5, for seq2seq tasks like translation), encoder-only (BERT, for classification/understanding), decoder-only (GPT, LLaMA — current LLM standard, generates text autoregressively by predicting next token).
- **Tokenization & embeddings（分词与向量化）**: Text is split into subword tokens (BPE / SentencePiece, vocab ~32K–128K). Each token is mapped to a high-dimensional vector via a learnable embedding matrix. Semantically similar tokens cluster together in the vector space.
- **Pretraining（预训练）**: Self-supervised next-token prediction on massive unlabeled text. The model learns language rules, world knowledge, and reasoning patterns purely from predicting the next word. Requires enormous compute (thousands of GPUs, months of training).
- **Scaling laws（规模法则）**: Model loss scales predictably with compute, data, and parameters (Chinchilla law). Compute-optimal: train on ~20× more tokens than parameters. This guides decisions on model size vs training duration for a fixed compute budget.
- **Fine-tuning（微调）**: Adapt a pretrained model to a specific domain or task using a small, high-quality labeled dataset. Instruction tuning (SFT) trains the model on (instruction, response) pairs to improve instruction following.
- **PEFT / LoRA（参数高效微调）**: Full fine-tuning updates all parameters — expensive. LoRA freezes original weights and trains small low-rank "adapter" matrices alongside. Reduces trainable parameters by ~99% with minimal quality loss. Can merge adapters back into the base model at inference with zero overhead.
- **Quantization（量化）**: Reduce weight precision from FP16 to INT8 or INT4 (GPTQ, AWQ). Cuts memory footprint by 50–75%, enabling deployment on smaller hardware. Slight accuracy tradeoff depends on method and task.
- **Evaluation / benchmarks**: Standardized tests measure different capabilities — MMLU (knowledge), GSM8K (reasoning), HumanEval (coding), HELM (holistic). Benchmark choice should match fine-tuning objectives. Open LLM Leaderboard (Hugging Face) tracks community models.
- **Multi-headed attention（多头注意力）**: Instead of one attention function, run h parallel attention heads (8 in the original paper), each with its own WQ/WK/WV weight matrices. Each head learns to attend to different relationships (e.g. one head tracks subject-verb, another tracks coreference). Outputs are concatenated and projected through WO. This is why Q/K/V dimension is d_model/h (64 for d_model=512, h=8) — total compute stays constant.
- **Positional encoding（位置编码）**: Self-attention is permutation-invariant — it has no built-in notion of order. Position is injected by adding a positional encoding vector to each embedding before the first encoder layer. Original paper uses sinusoidal functions (different frequencies per dimension); modern LLMs use learned relative encodings (RoPE, ALiBi) which generalize better to longer sequences than seen during training.
- **Residual connections + Layer Norm**: Each sublayer (self-attention, FFN) is wrapped with a skip connection: output = LayerNorm(x + sublayer(x)). Residual connections allow gradients to flow directly through deep stacks; layer norm stabilizes activations. Critical for training models with 96+ layers.
- **Feed-forward network / FFN sublayer（前馈网络）**: Each Transformer block contains two sublayers: self-attention followed by a position-wise FFN. The FFN is two linear projections with a nonlinearity between them: FFN(x) = W₂ · GELU(W₁x + b₁) + b₂. The inner dimension is typically 4×d_model (e.g. 2048 for d_model=512). Attention is where tokens "communicate" with each other; the FFN is where each token independently "thinks" — it is believed to store factual knowledge learned during pretraining (see "knowledge neurons" research).
- **Pre-norm vs Post-norm（归一化位置）**: Original Transformer uses Post-norm: LayerNorm(x + sublayer(x)) — norm applied after the residual addition. Modern LLMs (LLaMA, GPT-NeoX, Mistral) use Pre-norm: x + sublayer(LayerNorm(x)) — norm applied to the input before the sublayer. Pre-norm produces more stable gradient flow in very deep networks and allows training without learning rate warmup. This is why descriptions of "residual + LayerNorm" in older literature look different from what you see in modern open-source LLM code.
- **Decoder: masked self-attention（掩码自注意力）**: Decoder self-attention uses a look-ahead mask — future positions are set to -∞ before softmax, so each position can only attend to itself and earlier positions. This enforces autoregressive generation (the model cannot "cheat" by seeing future tokens during training).
- **Encoder-decoder cross-attention**: In seq2seq Transformers, decoder layers include a cross-attention sublayer. Q comes from the decoder, K and V come from the encoder's final output. This is how the decoder "reads" the encoded source sequence at each generation step.
- **Decoding strategies（解码策略）**: Greedy decoding: pick the highest-probability token at each step — fast but suboptimal. Beam search: maintain top-k partial sequences (k = beam width), prune at each step — better quality, higher compute. Sampling with temperature/top-p: stochastic, enables diverse outputs. Most production LLMs use nucleus sampling (top-p) or beam search depending on task.

## Key Questions

**Q: Explain the self-attention mechanism — why is it better than RNN for language modeling?**
Answer framework: Describe Q/K/V and the attention score formula. Key advantage #1: parallel computation (no sequential dependency → faster training). Key advantage #2: direct long-range connections (any token attends to any other in one step, vs RNN's gradual propagation that causes vanishing gradients). Mention the O(n²) cost as the tradeoff.

**Q: What are the three types of Transformer architectures and when do you use each?**
Answer framework: Encoder-only (BERT) — bidirectional context, good for understanding/classification but can't generate. Decoder-only (GPT, LLaMA) — autoregressive, generates text, current standard for LLMs. Encoder-decoder (T5) — separate encode/decode phases, suited for seq2seq (translation, summarization). Modern LLMs are decoder-only because pretraining (next-token prediction) naturally fits the decoder structure.

**Q: What are scaling laws and how do they influence infrastructure decisions?**
Answer framework: Loss decreases predictably as a power law of compute, data, and parameters. Chinchilla showed previous models were undertrained — optimal is ~20 tokens per parameter. Practical implication: given a fixed compute budget, you can calculate the optimal model size AND training data volume before starting. This directly informs cluster sizing, data pipeline capacity, and training duration estimates.

**Q: What is LoRA and why is it preferred over full fine-tuning?**
Answer framework: LoRA adds trainable low-rank matrices (A × B) alongside frozen pretrained weights. Only A and B are updated, reducing trainable params from billions to millions. Benefits: lower GPU memory, faster training, multiple adapters per base model (multi-task), can be merged at inference for zero latency overhead. Tradeoff: expressiveness is limited compared to full fine-tuning for very large domain shifts.

**Q: How would you set up an evaluation pipeline after fine-tuning a model?**
Answer framework: Choose benchmarks that match fine-tuning objective (don't use generic benchmarks for a domain-specific model). Automate evaluation in CI: run evals on every checkpoint. Compare against baseline (pretrained model) to measure delta. Watch for both capability gains AND regressions on general tasks. For production: add A/B testing and collect real user feedback signals alongside offline benchmarks.

**Q: A researcher asks for a 70B model fine-tuned on domain data but you only have 8×A100s. What's your approach?**
Answer framework: Full fine-tuning of 70B at FP16 requires ~140GB just for weights, plus gradients and optimizer states → impossible on 8×A100 80GB. Use: (1) LoRA to reduce trainable params; (2) 4-bit quantization of base model weights (QLoRA) to cut memory further; (3) gradient checkpointing to trade compute for memory; (4) DeepSpeed ZeRO-3 to shard optimizer states + parameters across GPUs. With QLoRA + LoRA, 70B fine-tuning is feasible on a single 8×A100 node.

**Q: What is multi-headed attention and why is it better than single-head attention?**
Answer framework: Multi-headed attention runs h parallel attention functions on projected subspaces of Q/K/V. Each head independently learns to attend to different aspects of the input (syntactic relationships, coreference, semantic roles). Concatenating and projecting the outputs allows the model to jointly reason across all these perspectives. Single-head attention forces the model to average all relationships into one representation, limiting expressiveness. The key insight: total compute is the same because each head operates at d_model/h dimensions.

**Q: Why does Transformer need positional encoding, and what are the tradeoffs between sinusoidal vs learned approaches?**
Answer framework: Self-attention is order-agnostic — shuffling input tokens produces the same output. Positional encoding injects position information by adding position-specific vectors to token embeddings. Original sinusoidal encoding (fixed, deterministic) generalizes to sequence lengths unseen during training. Learned absolute positions (GPT-2 style) are simpler but don't generalize beyond training length. Modern approaches (RoPE, ALiBi) encode relative positions directly in attention scores — better generalization and enables context extension techniques like RoPE scaling.

**Q: What is the role of the FFN sublayer in a Transformer block, and why is its inner dimension 4× wider?**
Answer framework: Each Transformer block has two sublayers — self-attention (tokens communicate across positions) and FFN (each token is processed independently). The FFN applies two linear projections with a nonlinearity (GELU/ReLU): W₂ · GELU(W₁x). The 4× expansion (d_model → 4·d_model → d_model) provides a "working memory" large enough to store and retrieve factual associations learned during pretraining. Research on "knowledge neurons" suggests specific FFN weights store specific facts — ablating them causes targeted factual failures.

**Q: What is the difference between Pre-norm and Post-norm Transformers, and why do modern LLMs use Pre-norm?**
Answer framework: Post-norm (original paper) applies LayerNorm after the residual addition: LayerNorm(x + sublayer(x)). Pre-norm applies LayerNorm before the sublayer: x + sublayer(LayerNorm(x)). Post-norm can cause unstable gradients in very deep networks because the residual stream grows unbounded. Pre-norm keeps the residual stream scale stable regardless of depth, making training more robust — especially important for models with 32–96+ layers. Practical consequence: most modern open-source LLMs (LLaMA, Mistral) use Pre-norm with RMSNorm (a simplified LayerNorm), which you'll see in their source code.

**Q: What is the difference between encoder self-attention and decoder self-attention?**
Answer framework: Encoder self-attention is bidirectional — each token can attend to all other tokens (both left and right context). Decoder self-attention is causal/masked — each token can only attend to itself and previous tokens (look-ahead mask sets future positions to -∞ before softmax). This is necessary for autoregressive generation: the model must not see future tokens during training, mirroring the inference-time constraint. The decoder also has a third sublayer (cross-attention) that attends to encoder outputs.

## Summary

Large Language Models are built on the Transformer architecture, which replaced RNNs by using self-attention to process all tokens in a sequence simultaneously. Instead of passing information step-by-step, self-attention allows each token to directly "look at" every other token, solving the long-range dependency problem while enabling massive parallelization during training. Modern LLMs use the decoder-only variant (GPT, LLaMA), which generates text autoregressively by repeatedly predicting the next token. Text is first converted to tokens (subwords), then to dense vector embeddings that encode semantic relationships — similar concepts cluster in the high-dimensional embedding space.

Pretraining on internet-scale data teaches the model language, facts, and reasoning by self-supervised next-token prediction. Scaling laws describe how model quality improves predictably with more parameters, more data, and more compute — the Chinchilla result showed that compute-optimal training requires roughly 20 tokens per parameter. After pretraining, instruction tuning (SFT) on (prompt, response) pairs makes models useful for following directions. Parameter-efficient fine-tuning techniques like LoRA allow adapting a pretrained model to new domains with a fraction of the compute, by adding small trainable adapter matrices while keeping the base weights frozen.

For an AI Infra Manager, LLM fundamentals matter in two ways: first, you need enough depth to have credible conversations with researchers about model architecture choices, training efficiency, and quality-compute tradeoffs; second, these fundamentals directly drive infrastructure requirements — model size determines GPU memory needs, training duration determines cluster utilization planning, and fine-tuning strategy (LoRA vs full fine-tune) determines the size of the GPU job. The adjacent topics to solidify are distributed training (how you actually train at scale), inference optimization (how you serve efficiently), and RLHF/post-training (how models are aligned after pretraining).

## Raw Material
- [[raw_material/tech/ai-basics/LLM 从零开始]]
- [[raw_material/tech/ai-basics/The Illustrated Transformer]]
- [Karpathy — Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY)
