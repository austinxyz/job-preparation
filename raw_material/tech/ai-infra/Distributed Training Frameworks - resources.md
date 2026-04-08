---
title: Distributed Training Frameworks - resources
source: (multiple)
date_saved: 2026-04-07
processed: true
skill_note: "[[skills/tech/ai-infra/Distributed Training Frameworks]]"
---

# Distributed Training Frameworks — Suggested Resources

## Reading List

- [Hugging Face — Intro to DeepSpeed ZeRO](https://huggingface.co/blog/zero-deepspeed-fairscale)
- [PyTorch — Distributed Data Parallel Tutorial](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)
- [Lillian Weng — Large-scale model training](https://lilianweng.github.io/posts/2021-09-25-train-large/)

## Notes

# Fit More and Train Faster With ZeRO via DeepSpeed and FairScale

Published January 19, 2021

**A guest blog post by Hugging Face fellow Stas Bekman**

As recent Machine Learning models have been growing much faster than the amount of GPU memory added to newly released cards, many users are unable to train or even just load some of those huge models onto their hardware. While there is an ongoing effort to distill some of those huge models to be of a more manageable size -- that effort isn't producing models small enough soon enough.

In the fall of 2019 Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase and Yuxiong He published a paper: [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054), which contains a plethora of ingenious new ideas on how one could make their hardware do much more than what it was thought possible before. A short time later [DeepSpeed](https://github.com/microsoft/deepspeed) has been released and it gave to the world the open source implementation of most of the ideas in that paper (a few ideas are still in works) and in parallel a team from Facebook released [FairScale](https://github.com/facebookresearch/fairscale/) which also implemented some of the core ideas from the ZeRO paper.

If you use the Hugging Face Trainer, as of `transformers` v4.2.0 you have the experimental support for DeepSpeed's and FairScale's ZeRO features. The new `--sharded_ddp` and `--deepspeed` command line `Trainer` arguments provide FairScale and DeepSpeed integration respectively. Here is [the full documentation](https://huggingface.co/transformers/master/main_classes/trainer.html#trainer-integrations).

This blog post will describe how you can benefit from ZeRO regardless of whether you own just a single GPU or a whole stack of them.

## [](https://huggingface.co/blog/zero-deepspeed-fairscale#huge-speedups-with-multi-gpu-setups)Huge Speedups with Multi-GPU Setups

Let's do a small finetuning with translation task experiment, using a `t5-large` model and the `finetune_trainer.py` script which you can find under [`examples/seq2seq`](https://github.com/huggingface/transformers/tree/master/examples/seq2seq) in the `transformers` GitHub repo.

We have 2x 24GB (Titan RTX) GPUs to test with.

This is just a proof of concept benchmarks so surely things can be improved further, so we will benchmark on a small sample of 2000 items for training and 500 items for evalulation to perform the comparisons. Evaluation does by default a beam search of size 4, so it's slower than training with the same number of samples, that's why 4x less eval items were used in these tests.

Here are the key command line arguments of our baseline:

```
export BS=16
python -m torch.distributed.launch --nproc_per_node=2 ./finetune_trainer.py \
--model_name_or_path t5-large --n_train 2000 --n_val 500 \
--per_device_eval_batch_size $BS --per_device_train_batch_size $BS \
--task translation_en_to_ro [...]
```

We are just using the `DistributedDataParallel` (DDP) and nothing else to boost the performance for the baseline. I was able to fit a batch size (BS) of 16 before hitting Out of Memory (OOM) error.

Note, that for simplicity and to make it easier to understand, I have only shown the command line arguments important for this demonstration. You will find the complete command line at [this post](https://github.com/huggingface/transformers/issues/8771#issuecomment-759248400).

Next, we are going to re-run the benchmark every time adding one of the following:

1. `--fp16`
2. `--sharded_ddp` (fairscale)
3. `--sharded_ddp --fp16` (fairscale)
4. `--deepspeed` without cpu offloading
5. `--deepspeed` with cpu offloading

Since the key optimization here is that each technique deploys GPU RAM more efficiently, we will try to continually increase the batch size and expect the training and evaluation to complete faster (while keeping the metrics steady or even improving some, but we won't focus on these here).

Remember that training and evaluation stages are very different from each other, because during training model weights are being modified, gradients are being calculated, and optimizer states are stored. During evaluation, none of these happen, but in this particular task of translation the model will try to search for the best hypothesis, so it actually has to do multiple runs before it's satisfied. That's why it's not fast, especially when a model is large.

Let's look at the results of these six test runs:

|Method|max BS|train time|eval time|
|---|---|---|---|
|baseline|16|30.9458|56.3310|
|fp16|20|21.4943|53.4675|
|sharded_ddp|30|25.9085|47.5589|
|sharded_ddp+fp16|30|17.3838|45.6593|
|deepspeed w/o cpu offload|40|**10.4007**|34.9289|
|deepspeed w/ cpu offload|**50**|20.9706|**32.1409**|

It's easy to see that both FairScale and DeepSpeed provide great improvements over the baseline, in the total train and evaluation time, but also in the batch size. DeepSpeed implements more magic as of this writing and seems to be the short term winner, but Fairscale is easier to deploy. For DeepSpeed you need to write a simple configuration file and change your command line's launcher, with Fairscale you only need to add the `--sharded_ddp` command line argument, so you may want to try it first as it's the most low-hanging fruit.

Following the 80:20 rule, I have only spent a few hours on these benchmarks and I haven't tried to squeeze every MB and second by refining the command line arguments and configuration, since it's pretty obvious from the simple table what you'd want to try next. When you will face a real project that will be running for hours and perhaps days, definitely spend more time to make sure you use the most optimal hyper-parameters to get your job done faster and at a minimal cost.

If you would like to experiment with this benchmark yourself or want to know more details about the hardware and software used to run it, please, refer to [this post](https://github.com/huggingface/transformers/issues/8771#issuecomment-759248400).

## [](https://huggingface.co/blog/zero-deepspeed-fairscale#fitting-a-huge-model-onto-one-gpu)Fitting A Huge Model Onto One GPU

While Fairscale gives us a boost only with multiple GPUs, DeepSpeed has a gift even for those of us with a single GPU.

Let's try the impossible - let's train [t5-3b](https://huggingface.co/t5-3b) on a 24GB RTX-3090 card.

First let's try to finetune the huge `t5-3b` using the normal single GPU setup:

```
export BS=1
CUDA_VISIBLE_DEVICES=0 ./finetune_trainer.py \
--model_name_or_path t5-3b --n_train 60 --n_val 10 \
--per_device_eval_batch_size $BS --per_device_train_batch_size $BS \
--task translation_en_to_ro --fp16 [...]
```

No cookie, even with BS=1 we get:

```
RuntimeError: CUDA out of memory. Tried to allocate 64.00 MiB (GPU 0; 23.70 GiB total capacity;
21.37 GiB already allocated; 45.69 MiB free; 22.05 GiB reserved in total by PyTorch)
```

Note, as earlier I'm showing only the important parts and the full command line arguments can be found [here](https://github.com/huggingface/transformers/issues/8771#issuecomment-759176685).

Now update your `transformers` to v4.2.0 or higher, then install DeepSpeed:

```
pip install deepspeed
```

and let's try again, this time adding DeepSpeed to the command line:

```
export BS=20
CUDA_VISIBLE_DEVICES=0 deepspeed --num_gpus=1 ./finetune_trainer.py \
--model_name_or_path t5-3b --n_train 60 --n_val 10 \
--per_device_eval_batch_size $BS --per_device_train_batch_size $BS \
--task translation_en_to_ro --fp16 --deepspeed ds_config_1gpu.json [...]
```

et voila! We get a batch size of 20 trained just fine. I could probably push it even further. The program failed with OOM at `BS=30`.

Here are the relevant results:

```
2021-01-12 19:06:31 | INFO | __main__ |   train_n_objs = 60
2021-01-12 19:06:31 | INFO | __main__ |   train_runtime = 8.8511
2021-01-12 19:06:35 | INFO | __main__ |   val_n_objs = 10
2021-01-12 19:06:35 | INFO | __main__ |   val_runtime = 3.5329
```

We can't compare these to the baseline, since the baseline won't even start and immediately failed with OOM.

Simply amazing!

I used only a tiny sample since I was primarily interested in being able to train and evaluate with this huge model that normally won't fit onto a 24GB GPU.

If you would like to experiment with this benchmark yourself or want to know more details about the hardware and software used to run it, please, refer to [this post](https://github.com/huggingface/transformers/issues/8771#issuecomment-759176685).

## [](https://huggingface.co/blog/zero-deepspeed-fairscale#the-magic-behind-zero)The Magic Behind ZeRO

Since `transformers` only integrated these fabulous solutions and wasn't part of their invention I will share the resources where you can discover all the details for yourself. But here are a few quick insights that may help understand how ZeRO manages these amazing feats.

The key feature of ZeRO is adding distributed data storage to the quite familiar concept of data parallel training.

The computation on each GPU is exactly the same as data parallel training, but the parameter, gradients and optimizer states are stored in a distributed/partitioned fashion across all the GPUs and fetched only when needed.

The following diagram, coming from this [blog post](https://www.microsoft.com/en-us/research/blog/zero-deepspeed-new-system-optimizations-enable-training-models-with-over-100-billion-parameters/) illustrates how this works:

[![ZeRO Partitioning](https://huggingface.co/blog/assets/11_zero_deepspeed_fairscale/zero-partitioning.png)](https://huggingface.co/blog/assets/11_zero_deepspeed_fairscale/zero-partitioning.png)

ZeRO's ingenious approach is to partition the params, gradients and optimizer states equally across all GPUs and give each GPU just a single partition (also referred to as a shard). This leads to zero overlap in data storage between GPUs. At runtime each GPU builds up each layer's data on the fly by asking participating GPUs to send the information it's lacking.

This idea could be difficult to grasp, and you will find my attempt at an explanation [here](https://github.com/huggingface/transformers/issues/8771#issuecomment-758418429).

As of this writing FairScale and DeepSpeed only perform Partitioning (Sharding) for the optimizer states and gradients. Model parameters sharding is supposedly coming soon in DeepSpeed and FairScale.

The other powerful feature is ZeRO-Offload ([paper](https://arxiv.org/abs/2101.06840)). This feature offloads some of the processing and memory needs to the host's CPU, thus allowing more to be fit onto the GPU. You saw its dramatic impact in the success at running `t5-3b` on a 24GB GPU.

One other problem that a lot of people complain about on pytorch forums is GPU memory fragmentation. One often gets an OOM error that may look like this:

```
RuntimeError: CUDA out of memory. Tried to allocate 1.48 GiB (GPU 0; 23.65 GiB total capacity;
16.22 GiB already allocated; 111.12 MiB free; 22.52 GiB reserved in total by PyTorch)
```

The program wants to allocate ~1.5GB and the GPU still has some 6-7GBs of unused memory, but it reports to have only ~100MB of contiguous free memory and it fails with the OOM error. This happens as chunks of different size get allocated and de-allocated again and again, and over time holes get created leading to memory fragmentation, where there is a lot of unused memory but no contiguous chunks of the desired size. In the example above the program could probably allocate 100MB of contiguous memory, but clearly it can't get 1.5GB in a single chunk.

DeepSpeed attacks this problem by managing GPU memory by itself and ensuring that long term memory allocations don't mix with short-term ones and thus there is much less fragmentation. While the paper doesn't go into details, the [source code](https://github.com/microsoft/DeepSpeed) is available, so it's possible to see how DeepSpeed accomplishes that.

As ZeRO stands for Zero Redundancy Optimizer, it's easy to see that it lives up to its name.

## [](https://huggingface.co/blog/zero-deepspeed-fairscale#the-future)The Future

Besides the anticipated upcoming support for model params sharding in DeepSpeed, it already released new features that we haven't explored yet. These include DeepSpeed Sparse Attention and 1-bit Adam, which are supposed to decrease memory usage and dramatically reduce inter-GPU communication overhead, which should lead to an even faster training and support even bigger models.

I trust we are going to see new gifts from the FairScale team as well. I think they are working on ZeRO stage 3 as well.

Even more exciting, [ZeRO is being integrated into pytorch](https://github.com/pytorch/pytorch/pull/46750).

## [](https://huggingface.co/blog/zero-deepspeed-fairscale#deployment)Deployment

If you found the results shared in this blog post enticing, please proceed [here](https://huggingface.co/transformers/master/main_classes/trainer.html#trainer-integrations) for details on how to use DeepSpeed and FairScale with the `transformers` Trainer.

You can, of course, modify your own trainer to integrate DeepSpeed and FairScale, based on each project's instructions or you can "cheat" and see how we did it in the `transformers` Trainer. If you go for the latter, to find your way around `grep` the source code for `deepspeed` and/or `sharded_ddp`.

The good news is that ZeRO requires no model modification. The only required modifications are in the training code.

## [](https://huggingface.co/blog/zero-deepspeed-fairscale#issues)Issues

If you encounter any issues with the integration part of either of these projects please open an Issue in [transformers](https://github.com/huggingface/transformers/issues).

But if you have problems with DeepSpeed and FairScale installation, configuration and deployment - you need to ask the experts in their domains, therefore, please, use [DeepSpeed Issue](https://github.com/microsoft/DeepSpeed/issues) or [FairScale Issue](https://github.com/facebookresearch/fairscale/issues) instead.

## [](https://huggingface.co/blog/zero-deepspeed-fairscale#resources)Resources

While you don't really need to understand how any of these projects work and you can just deploy them via the `transformers` Trainer, should you want to figure out the whys and hows please refer to the following resources.

- [FairScale GitHub](https://github.com/facebookresearch/fairscale)
    
- [DeepSpeed GitHub](https://github.com/microsoft/DeepSpeed)
    
- Paper: [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/abs/1910.02054). The paper is very interesting, but it's very terse.
    
- Here is a good [video discussion](https://www.youtube.com/watch?v=tC01FRB0M7w) of the paper with visuals
    
- Paper: [ZeRO-Offload: Democratizing Billion-Scale Model Training](https://arxiv.org/abs/2101.06840). Just published - this one goes into the details of ZeRO Offload feature.
    
- DeepSpeed [configuration and tutorials](https://www.deepspeed.ai/getting-started/)
    
- In addition to the paper, I highly recommend to read the following detailed blog posts with diagrams:
    
    - [DeepSpeed: Extreme-scale model training for everyone](https://www.microsoft.com/en-us/research/blog/deepspeed-extreme-scale-model-training-for-everyone/)
    - [ZeRO & DeepSpeed: New system optimizations enable training models with over 100 billion parameters](https://www.microsoft.com/en-us/research/blog/zero-deepspeed-new-system-optimizations-enable-training-models-with-over-100-billion-parameters/)
    - [Turing-NLG: A 17-billion-parameter language model by Microsoft](https://www.microsoft.com/en-us/research/blog/turing-nlg-a-17-billion-parameter-language-model-by-microsoft/)
- DeepSpeed [examples on GitHub](https://github.com/microsoft/DeepSpeedExamples)
    

## [](https://huggingface.co/blog/zero-deepspeed-fairscale#gratitude)Gratitude

We were quite astonished at the amazing level of support we received from the FairScale and DeepSpeed developer teams while working on integrating those projects into `transformers`.

In particular I'd like to thank:

- Benjamin Lefaudeux [@blefaudeux](https://github.com/blefaudeux)
- Mandeep Baines [@msbaines](https://github.com/msbaines)

from the FairScale team and:

- Jeff Rasley [@jeffra](https://github.com/jeffra)
- Olatunji Ruwase [@tjruwase](https://github.com/tjruwase)
- Samyam Rajbhandari [@samyam](https://github.com/samyam)

from the DeepSpeed team for your generous and caring support and prompt resolution of the issues we have encountered.

And HuggingFace for providing access to hardware the benchmarks were run on.

Sylvain Gugger [@sgugger](https://github.com/sgugger/) and Stas Bekman [@stas00](https://github.com/stas00) worked on the integration of these projects.
# Getting Started with Distributed Data Parallel

Created On: Apr 23, 2019 | Last Updated: Sep 23, 2025 | Last Verified: Nov 05, 2024

**Author**: [Shen Li](https://mrshenli.github.io/)

**Edited by**: [Joe Zhu](https://github.com/gunandrose4u), [Chirag Pandya](https://github.com/c-p-i-o)

Note

[![edit](https://docs.pytorch.org/tutorials/_images/pencil-16.png)](https://docs.pytorch.org/tutorials/_images/pencil-16.png) View and edit this tutorial in [github](https://github.com/pytorch/tutorials/blob/main/intermediate_source/ddp_tutorial.rst).

Prerequisites:

- [PyTorch Distributed Overview](https://docs.pytorch.org/tutorials/beginner/dist_overview.html)
    
- [DistributedDataParallel API documents](https://pytorch.org/docs/master/generated/torch.nn.parallel.DistributedDataParallel.html)
    
- [DistributedDataParallel notes](https://pytorch.org/docs/master/notes/ddp.html)
    

[DistributedDataParallel](https://pytorch.org/docs/stable/nn.html#module-torch.nn.parallel) (DDP) is a powerful module in PyTorch that allows you to parallelize your model across multiple machines, making it perfect for large-scale deep learning applications. To use DDP, you’ll need to spawn multiple processes and create a single instance of DDP per process.

But how does it work? DDP uses collective communications from the [torch.distributed](https://pytorch.org/tutorials/intermediate/dist_tuto.html) package to synchronize gradients and buffers across all processes. This means that each process will have its own copy of the model, but they’ll all work together to train the model as if it were on a single machine.

To make this happen, DDP registers an autograd hook for each parameter in the model. When the backward pass is run, this hook fires and triggers gradient synchronization across all processes. This ensures that each process has the same gradients, which are then used to update the model.

For more information on how DDP works and how to use it effectively, be sure to check out the [DDP design note](https://pytorch.org/docs/master/notes/ddp.html). With DDP, you can train your models faster and more efficiently than ever before!

The recommended way to use DDP is to spawn one process for each model replica. The model replica can span multiple devices. DDP processes can be placed on the same machine or across machines. Note that GPU devices cannot be shared across DDP processes (i.e. one GPU for one DDP process).

In this tutorial, we’ll start with a basic DDP use case and then demonstrate more advanced use cases, including checkpointing models and combining DDP with model parallel.

Note

The code in this tutorial runs on an 8-GPU server, but it can be easily generalized to other environments.

## Comparison between `DataParallel` and `DistributedDataParallel`

Before we dive in, let’s clarify why you would consider using `DistributedDataParallel` over `DataParallel`, despite its added complexity:

- First, `DataParallel` is single-process, multi-threaded, but it only works on a single machine. In contrast, `DistributedDataParallel` is multi-process and supports both single- and multi- machine training. Due to GIL contention across threads, per-iteration replicated model, and additional overhead introduced by scattering inputs and gathering outputs, `DataParallel` is usually slower than `DistributedDataParallel` even on a single machine.
    
- Recall from the [prior tutorial](https://pytorch.org/tutorials/intermediate/model_parallel_tutorial.html) that if your model is too large to fit on a single GPU, you must use **model parallel** to split it across multiple GPUs. `DistributedDataParallel` works with **model parallel**, while `DataParallel` does not at this time. When DDP is combined with model parallel, each DDP process would use model parallel, and all processes collectively would use data parallel.
    

## Basic Use Case

To create a DDP module, you must first set up process groups properly. More details can be found in [Writing Distributed Applications with PyTorch](https://pytorch.org/tutorials/intermediate/dist_tuto.html).

import os
import sys
import tempfile
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim
import torch.multiprocessing as mp

from torch.nn.parallel import DistributedDataParallel as DDP

# On Windows platform, the torch.distributed package only
# supports Gloo backend, FileStore and TcpStore.
# For FileStore, set init_method parameter in init_process_group
# to a local file. Example as follow:
# init_method="file:///f:/libtmp/some_file"
# dist.init_process_group(
#    "gloo",
#    rank=rank,
#    init_method=init_method,
#    world_size=world_size)
# For TcpStore, same way as on Linux.

def setup(rank, world_size):
    os.environ['MASTER_ADDR'] = 'localhost'
    os.environ['MASTER_PORT'] = '12355'

    # We want to be able to train our model on an `accelerator <https://pytorch.org/docs/stable/torch.html#accelerators>`__
    # such as CUDA, MPS, MTIA, or XPU.
    acc = torch.accelerator.current_accelerator()
    backend = torch.distributed.get_default_backend_for_device(acc)
    # initialize the process group
    dist.init_process_group(backend, rank=rank, world_size=world_size)

def cleanup():
    dist.destroy_process_group()

Now, let’s create a toy module, wrap it with DDP, and feed it some dummy input data. Please note, as DDP broadcasts model states from rank 0 process to all other processes in the DDP constructor, you do not need to worry about different DDP processes starting from different initial model parameter values.

class ToyModel(nn.Module):
    def __init__(self):
        super(ToyModel, self).__init__()
        self.net1 = nn.Linear(10, 10)
        self.relu = nn.ReLU()
        self.net2 = nn.Linear(10, 5)

    def forward(self, x):
        return self.net2(self.relu(self.net1(x)))

def demo_basic(rank, world_size):
    print(f"Running basic DDP example on rank {rank}.")
    setup(rank, world_size)

    # create model and move it to GPU with id rank
    model = ToyModel().to(rank)
    ddp_model = DDP(model, device_ids=[rank])

    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)

    optimizer.zero_grad()
    outputs = ddp_model(torch.randn(20, 10))
    labels = torch.randn(20, 5).to(rank)
    loss_fn(outputs, labels).backward()
    optimizer.step()

    cleanup()
    print(f"Finished running basic DDP example on rank {rank}.")

def run_demo(demo_fn, world_size):
    mp.spawn(demo_fn,
             args=(world_size,),
             nprocs=world_size,
             join=True)

As you can see, DDP wraps lower-level distributed communication details and provides a clean API as if it were a local model. Gradient synchronization communications take place during the backward pass and overlap with the backward computation. When the `backward()` returns, `param.grad` already contains the synchronized gradient tensor. For basic use cases, DDP only requires a few more lines of code to set up the process group. When applying DDP to more advanced use cases, some caveats require caution.

## Skewed Processing Speeds

In DDP, the constructor, the forward pass, and the backward pass are distributed synchronization points. Different processes are expected to launch the same number of synchronizations and reach these synchronization points in the same order and enter each synchronization point at roughly the same time. Otherwise, fast processes might arrive early and timeout while waiting for stragglers. Hence, users are responsible for balancing workload distributions across processes. Sometimes, skewed processing speeds are inevitable due to, e.g., network delays, resource contentions, or unpredictable workload spikes. To avoid timeouts in these situations, make sure that you pass a sufficiently large `timeout` value when calling [init_process_group](https://pytorch.org/docs/stable/distributed.html#torch.distributed.init_process_group).

## Save and Load Checkpoints

It’s common to use `torch.save` and `torch.load` to checkpoint modules during training and recover from checkpoints. See [SAVING AND LOADING MODELS](https://pytorch.org/tutorials/beginner/saving_loading_models.html) for more details. When using DDP, one optimization is to save the model in only one process and then load it on all processes, reducing write overhead. This works because all processes start from the same parameters and gradients are synchronized in backward passes, and hence optimizers should keep setting parameters to the same values. If you use this optimization (i.e. save on one process but restore on all), make sure no process starts loading before the saving is finished. Additionally, when loading the module, you need to provide an appropriate `map_location` argument to prevent processes from stepping into others’ devices. If `map_location` is missing, `torch.load` will first load the module to CPU and then copy each parameter to where it was saved, which would result in all processes on the same machine using the same set of devices. For more advanced failure recovery and elasticity support, please refer to [TorchElastic](https://pytorch.org/elastic).

def demo_checkpoint(rank, world_size):
    print(f"Running DDP checkpoint example on rank {rank}.")
    setup(rank, world_size)

    model = ToyModel().to(rank)
    ddp_model = DDP(model, device_ids=[rank])

    CHECKPOINT_PATH = tempfile.gettempdir() + "/model.checkpoint"
    if rank == 0:
        # All processes should see same parameters as they all start from same
        # random parameters and gradients are synchronized in backward passes.
        # Therefore, saving it in one process is sufficient.
        torch.save(ddp_model.state_dict(), CHECKPOINT_PATH)

    # Use a barrier() to make sure that process 1 loads the model after process
    # 0 saves it.
    dist.barrier()
    # We want to be able to train our model on an `accelerator <https://pytorch.org/docs/stable/torch.html#accelerators>`__
    # such as CUDA, MPS, MTIA, or XPU.
    acc = torch.accelerator.current_accelerator()
    # configure map_location properly
    map_location = {f'{acc}:0': f'{acc}:{rank}'}
    ddp_model.load_state_dict(
        torch.load(CHECKPOINT_PATH, map_location=map_location, weights_only=True))

    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)

    optimizer.zero_grad()
    outputs = ddp_model(torch.randn(20, 10))
    labels = torch.randn(20, 5).to(rank)

    loss_fn(outputs, labels).backward()
    optimizer.step()

    # Not necessary to use a dist.barrier() to guard the file deletion below
    # as the AllReduce ops in the backward pass of DDP already served as
    # a synchronization.

    if rank == 0:
        os.remove(CHECKPOINT_PATH)

    cleanup()
    print(f"Finished running DDP checkpoint example on rank {rank}.")

## Combining DDP with Model Parallelism

DDP also works with multi-GPU models. DDP wrapping multi-GPU models is especially helpful when training large models with a huge amount of data.

class ToyMpModel(nn.Module):
    def __init__(self, dev0, dev1):
        super(ToyMpModel, self).__init__()
        self.dev0 = dev0
        self.dev1 = dev1
        self.net1 = torch.nn.Linear(10, 10).to(dev0)
        self.relu = torch.nn.ReLU()
        self.net2 = torch.nn.Linear(10, 5).to(dev1)

    def forward(self, x):
        x = x.to(self.dev0)
        x = self.relu(self.net1(x))
        x = x.to(self.dev1)
        return self.net2(x)

When passing a multi-GPU model to DDP, `device_ids` and `output_device` must NOT be set. Input and output data will be placed in proper devices by either the application or the model `forward()` method.

def demo_model_parallel(rank, world_size):
    print(f"Running DDP with model parallel example on rank {rank}.")
    setup(rank, world_size)

    # setup mp_model and devices for this process
    dev0 = rank * 2
    dev1 = rank * 2 + 1
    mp_model = ToyMpModel(dev0, dev1)
    ddp_mp_model = DDP(mp_model)

    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(ddp_mp_model.parameters(), lr=0.001)

    optimizer.zero_grad()
    # outputs will be on dev1
    outputs = ddp_mp_model(torch.randn(20, 10))
    labels = torch.randn(20, 5).to(dev1)
    loss_fn(outputs, labels).backward()
    optimizer.step()

    cleanup()
    print(f"Finished running DDP with model parallel example on rank {rank}.")

if __name__ == "__main__":
    n_gpus = torch.accelerator.device_count()
    assert n_gpus >= 2, f"Requires at least 2 GPUs to run, but got {n_gpus}"
    world_size = n_gpus
    run_demo(demo_basic, world_size)
    run_demo(demo_checkpoint, world_size)
    world_size = n_gpus//2
    run_demo(demo_model_parallel, world_size)

## Initialize DDP with torch.distributed.run/torchrun

We can leverage PyTorch Elastic to simplify the DDP code and initialize the job more easily. Let’s still use the Toymodel example and create a file named `elastic_ddp.py`.

import os
import torch
import torch.distributed as dist
import torch.nn as nn
import torch.optim as optim

from torch.nn.parallel import DistributedDataParallel as DDP

class ToyModel(nn.Module):
    def __init__(self):
        super(ToyModel, self).__init__()
        self.net1 = nn.Linear(10, 10)
        self.relu = nn.ReLU()
        self.net2 = nn.Linear(10, 5)

    def forward(self, x):
        return self.net2(self.relu(self.net1(x)))

def demo_basic():
    torch.accelerator.set_device_index(int(os.environ["LOCAL_RANK"]))
    acc = torch.accelerator.current_accelerator()
    backend = torch.distributed.get_default_backend_for_device(acc)
    dist.init_process_group(backend)
    rank = dist.get_rank()
    print(f"Start running basic DDP example on rank {rank}.")
    # create model and move it to GPU with id rank
    device_id = rank % torch.accelerator.device_count()
    model = ToyModel().to(device_id)
    ddp_model = DDP(model, device_ids=[device_id])
    loss_fn = nn.MSELoss()
    optimizer = optim.SGD(ddp_model.parameters(), lr=0.001)

    optimizer.zero_grad()
    outputs = ddp_model(torch.randn(20, 10))
    labels = torch.randn(20, 5).to(device_id)
    loss_fn(outputs, labels).backward()
    optimizer.step()
    dist.destroy_process_group()
    print(f"Finished running basic DDP example on rank {rank}.")

if __name__ == "__main__":
    demo_basic()

One can then run a [torch elastic/torchrun](https://pytorch.org/docs/stable/elastic/quickstart.html) command on all nodes to initialize the DDP job created above:

torchrun --nnodes=2 --nproc_per_node=8 --rdzv_id=100 --rdzv_backend=c10d --rdzv_endpoint=$MASTER_ADDR:29400 elastic_ddp.py

In the example above, we are running the DDP script on two hosts and we run with 8 processes on each host. That is, we are running this job on 16 GPUs. Note that `$MASTER_ADDR` must be the same across all nodes.

Here `torchrun` will launch 8 processes and invoke `elastic_ddp.py` on each process on the node it is launched on, but user also needs to apply cluster management tools like slurm to actually run this command on 2 nodes.

For example, on a SLURM enabled cluster, we can write a script to run the command above and set `MASTER_ADDR` as:

export MASTER_ADDR=$(scontrol show hostname ${SLURM_NODELIST} | head -n 1)

Then we can just run this script using the SLURM command: `srun --nodes=2 ./torchrun_script.sh`.

This is just an example; you can choose your own cluster scheduling tools to initiate the `torchrun` job.

For more information about Elastic run, please see the [quick start document](https://pytorch.org/docs/stable/elastic/quickstart.html).

# How to Train Really Large Models on Many GPUs?

Date: September 24, 2021 | Estimated Reading Time: 21 min | Author: Lilian Weng

Table of Contents

- [Training Parallelism](https://lilianweng.github.io/posts/2021-09-25-train-large/#training-parallelism)
    - [Data Parallelism](https://lilianweng.github.io/posts/2021-09-25-train-large/#data-parallelism)
    - [Model Parallelism](https://lilianweng.github.io/posts/2021-09-25-train-large/#model-parallelism)
    - [Pipeline Parallelism](https://lilianweng.github.io/posts/2021-09-25-train-large/#pipeline-parallelism)
    - [Tensor Parallelism](https://lilianweng.github.io/posts/2021-09-25-train-large/#tensor-parallelism)
- [Mixture-of-Experts (MoE)](https://lilianweng.github.io/posts/2021-09-25-train-large/#mixture-of-experts-moe)
- [Other Memory Saving Designs](https://lilianweng.github.io/posts/2021-09-25-train-large/#other-memory-saving-designs)
    - [CPU Offloading](https://lilianweng.github.io/posts/2021-09-25-train-large/#cpu-offloading)
    - [Activation Recomputation](https://lilianweng.github.io/posts/2021-09-25-train-large/#activation-recomputation)
    - [Mixed Precision Training](https://lilianweng.github.io/posts/2021-09-25-train-large/#mixed-precision-training)
    - [Compression](https://lilianweng.github.io/posts/2021-09-25-train-large/#compression)
    - [Memory Efficient Optimizer](https://lilianweng.github.io/posts/2021-09-25-train-large/#memory-efficient-optimizer)
- [Citation](https://lilianweng.github.io/posts/2021-09-25-train-large/#citation)
- [References](https://lilianweng.github.io/posts/2021-09-25-train-large/#references)

[Updated on 2022-03-13: add [expert choice routing](https://lilianweng.github.io/posts/2021-09-25-train-large/#ec).]  
[Updated on 2022-06-10]: [Greg](https://gregbrockman.com/) and I wrote a shorted and upgraded version of this post, published on OpenAI Blog: [“Techniques for Training Large Neural Networks”](https://openai.com/blog/techniques-for-training-large-neural-networks/)

In recent years, we are seeing better results on many NLP benchmark tasks with larger pre-trained [language models](https://lilianweng.github.io/posts/2019-01-31-lm/). How to train large and deep neural networks is challenging, as it demands a large amount of GPU memory and a long horizon of training time.

However an individual GPU worker has limited memory and the sizes of many large models have grown beyond a single GPU. There are several parallelism paradigms to enable model training across multiple GPUs, as well as a variety of model architecture and memory saving designs to help make it possible to train _very large_ neural networks.

# Training Parallelism

The main bottleneck for training very large neural network models is the intense demand for a large amount of GPU memory, way above what can be hosted on an individual GPU machine. Besides the model weights (e.g. tens of billions of floating point numbers), it is usually even more expensive to store intermediate computation outputs such as gradients and optimizer states (e.g. momentums & variations in Adam). Additionally training a large model often pairs with a large training corpus and thus a single process may just take forever.

As a result, parallelism is necessary. Parallelism can happen at different dimensions, including data, model architecture, and tensor operation.

## Data Parallelism

The most naive way for **Data parallelism (DP)** is to copy the same model weights into multiple workers and assign a fraction of data to each worker to be processed at the same time.

Naive DP cannot work well if the model size is larger than a single GPU node’s memory. Methods like _GeePS_ ([Cui et al. 2016](https://www.pdl.cmu.edu/PDL-FTP/CloudComputing/GeePS-cui-eurosys16.pdf)) offload temporarily unused parameters back to CPU to work with limited GPU memory when the model is too big to fit into one machine. The data swapping transfer should happen at the backend and not interfere with training computation.

At the end of each minibatch, workers need to synchronize gradients or weights to avoid staleness. There are two main synchronization approaches and both have clear pros & cons.

1. _Bulk synchronous parallels (BSP)_: Workers sync data at the end of every minibatch. It prevents model weights staleness and good learning efficiency but each machine has to halt and wait for others to send gradients.
2. _Asynchronous parallel (ASP)_: Every GPU worker processes the data asynchronously, no waiting or stalling. However, it can easily lead to stale weights being used and thus lower the statistical learning efficiency. Even though it increases the computation time, it may not speed up training time to convergence.

Somewhere in the middle is to synchronize gradients globally once every  iterations (). This feature is called “gradient accumulation” in Distribution Data Parallel ([DDP](https://pytorch.org/tutorials/intermediate/ddp_tutorial.html)) since Pytorch v1.5 ([Li et al. 2021](https://arxiv.org/abs/2006.15704)). Bucketing gradients avoid immediate `AllReduce` operations but instead buckets multiple gradients into one `AllReduce` to improve throughput. Computation and communication scheduling optimization can be made based on the computation graph.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/pytorch-ddp.png)

Pseudo code for Pytorch DDP. (Image source: [Li et al. 2021](https://arxiv.org/abs/2006.15704))

## Model Parallelism

**Model parallelism (MP)** aims to solve the case when the model weights cannot fit into a single node. The computation and model parameters are partitioned across multiple machines. Different from data parallelism where each worker hosts a full copy of the entire model, MP only allocates a fraction of model parameters on one worker and thus both the memory usage and the computation are reduced.

Since deep neural networks usually contain a stack of vertical layers, it feels straightforward to split a large model by layer, where a small consecutive set of layers are grouped into one partition on one worker. However, a naive implementation for running every data batch through multiple such workers with sequential dependency leads to big bubbles of waiting time and severe under-utilization of computation resources.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/naive-data-parallelism.png)

A naive model parallelism setup where the model is vertically split into 4 partitions. Data is processed by one worker at a time due to sequential dependency, leading to large “bubbles” of idle time. (Image source: [Huang et al. 2019](https://arxiv.org/abs/1811.06965))

## Pipeline Parallelism

**Pipeline parallelism (PP)** combines model parallelism with data parallelism to reduce inefficient time “bubbles’’. The main idea is to split one minibatch into multiple microbatches and enable each stage worker to process one microbatch simultaneously. Note that every microbatch needs two passes, one forward and one backward. Inter-worker communication only transfers activations (forward) and gradients (backward). How these passes are scheduled and how the gradients are aggregated vary in different approaches. The number of partitions (workers) is also known as _pipeline depth_.

In _GPipe_ ([Huang et al. 2019](https://arxiv.org/abs/1811.06965)) gradients from multiple microbatches are aggregated and applied synchronously at the end. The synchronous gradient descent guarantees learning consistency and efficiency irrespective of the number of workers. As shown in Fig. 3, bubbles still exist but are much smaller than what’s in Given  evenly split microbatches and  partitions, assuming both forward and backward per microbatch take one unit of time, the fraction of bubble is:

The GPipe paper observed that the bubble overhead is almost negligible if the number of microbatches is more than 4x the number of partitions  (when [activation recomputation](https://lilianweng.github.io/posts/2021-09-25-train-large/#activation-recomputation) is applied).

![](https://lilianweng.github.io/posts/2021-09-25-train-large/gpipe.png)

Illustration of pipeline parallelism in GPipe with 4 microbatches and 4 partitions. GPipe aggregates and updates gradients across devices synchronously at the end of every batch. (Image source: [Huang et al. 2019](https://arxiv.org/abs/1811.06965))

GPipe achieves almost linear speedup in throughput with the number of devices, although it is not always guaranteed if the model parameters are not evenly distributed across workers.

_PipeDream_ ([Narayanan et al. 2019](https://cs.stanford.edu/~matei/papers/2019/sosp_pipedream.pdf)) schedules each worker to alternatively process the forward and backward passes (`1F1B`). PipeDream names each model partition “stage” and each stage worker can have multiple replicas to run data parallelism. In this process, PipeDream uses a deterministic round-robin load balancing strategy to assign work among multiple replicas of stages to ensure that the forward and backward passes for the same minibatch happen on the same replica.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/pipedream.png)

Illustration of `1F1B` microbatch scheduling in PipeDream. (Image source: [Harlap et al. 2018](https://arxiv.org/abs/1806.03377))

Since PipeDream does not have an end-of-batch global gradient sync across all the workers, an native implementation of 1F1B can easily lead to the forward and backward passes of one microbatch using different versions of model weights, thus lowering the learning efficiency. PipeDream proposed a few designs to tackle this issue:

- _Weight stashing_: Each worker keeps track of several model versions and makes sure that the same version of weights are used in the forward and backward passes given one data batch.
- _Vertical sync_ (Optional): The version of model weights flows between stage workers together with activations and gradients. Then the computation adopts the corresponding stashed version propagated from the previous worker. This process keeps version consistency across workers. Note that it is asynchronous, different from GPipe.

At the beginning of a training run, PipeDream first profiles the computation memory cost and time of each layer in the model and then optimizes a solution for partitioning layers into stages, which is a dynamic programming problem.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/pipedream-results.png)

Results for VGG16 on ILSVRC12. (Top) Accuracy vs time. The integer marks the number of stage workers. ASP = Asynchronous parallel & BSP = Bulk synchronous parallels. (Bottom) Training time speedup for different parallelism configurations. Straight pipeline refers to pipeline parallelism without data parallelism. (Image source: [Harlap et al. 2018](https://arxiv.org/abs/1806.03377))

Two variations of PipeDream were later proposed to reduce the memory footprint by stashed model versions ([Narayanan et al. 2021](https://arxiv.org/abs/2006.09503)).

_PipeDream-flush_ adds a globally synchronized pipeline flush periodically, just like GPipe. In this way, it greatly reduces the memory footprint (i.e. only maintain a single version of model weights) by sacrificing a little throughput.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/pipedream-flush.png)

Illustration of pipeline scheduling in PipeDream-flush. (Image source: ([Narayanan et al. 2021](https://arxiv.org/abs/2006.09503))

_PipeDream-2BW_ maintains only two versions of model weights, where “2BW” is short for “double-buffered weights”. It generates a new model version every  microbatches and  should be larger than the pipeline depth , . A newly updated model version cannot fully replace the old version immediately since some leftover backward passes still depend on the old version. In total only two versions need to be saved so the memory cost is much reduced.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/pipedream-2bw.png)

Illustration of pipeline scheduling in PipeDream-2BW. (Image source: ([Narayanan et al. 2021](https://arxiv.org/abs/2006.09503))

## Tensor Parallelism

Both model and pipeline parallelisms split a model vertically. OTOH we can horizontally partition the computation for one tensor operation across multiple devices, named **Tensor parallelism (TP)**.

Let’s take the transformer as an example given its popularity. The transformer model mainly consists of layers of MLP and self-attention blocks. _Megatron-LM_ ([Shoeybi et al. 2020](https://arxiv.org/abs/1909.08053)) adopts a simple way to parallelize intra-layer computation for MLP and self-attention.

A MLP layer in a transformer contains a GEMM (General matrix multiply) followed by an non-linear GeLU transfer. Let’s split weight matrix  by column:

The attention block runs GEMM with query (), key (), and value weights () according to the above partitioning in parallel and then combines them with another GEMM to produce the attention head results.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/Megatron-LM.png)

Illustration of tensor parallelism for key transformer components proposed in Megatron-LM. (Image source: [Shoeybi et al. 2020](https://arxiv.org/abs/1909.08053))

[Narayanan et al. (2021)](https://arxiv.org/abs/2104.04473) combined pipeline, tensor and data parallelism with a new pipeline scheduling strategy and named their approach _PTD-P_. Instead of only positioning a continuous set of layers (“model chunk”) on a device, each worker can be assigned with multiple chunks of smaller continuous subsets of layers (e.g. device 1 has layers 1, 2, 9, 10; device 2 has layers 3, 4, 11, 12; each has two model chunks). The number of microbatches in one batch should be exactly divided by the number of workers (). If there are  model chunks per worker, the pipeline bubble time can be reduced by a multiplier of  compared to a GPipe scheduling.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/PTD-P-interleaved.png)

(Top) Default `1F1B` pipeline schedule as in PipeDream-flush. (Bottom) Interleaved 1F1B pipeline schedule. First model chunks are in dark colors and second chunks are in light colors. (Image source: [Narayanan et al. 202)](https://arxiv.org/abs/2104.04473))

# Mixture-of-Experts (MoE)

The **Mixture-of-Experts (MoE)** approach attracts a lot of attention recently as researchers (mainly from Google) try to push the limit of model size. The core of the idea is [ensembling learning](https://en.wikipedia.org/wiki/Ensemble_learning): _Combination of multiple weak learners gives you a strong learner!_

Within one deep neural network, ensembling can be implemented with a gating mechanism connecting multiple experts ([Shazeer et al., 2017](https://arxiv.org/abs/1701.06538)). The gating mechanism controls which subset of the network (e.g. which experts) should be activated to produce outputs. The paper named it “sparsely gated mixture-of-experts” (MoE) layer.

Precisely one MoE layer contains

-  feed-forward networks as experts 
- A trainable gating network  to learn a probability distribution over  experts so as to route the traffic to a few selected experts.

Depending on the gating outputs, not every expert has to be evaluated. When the number of experts is too large, we can consider using a two-level hierarchical MoE.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/moe.png)

Illustration of a mixture-of-experts (MoE) layer. Only 2 out of  experts are selected and activated by the gating network. (Image source: [Shazeer et al., 2017](https://arxiv.org/abs/1701.06538))

A simple choice of  is to multiply the input with a trainable weight matrix  and then do softmax: . However, this produces a dense control vector for gating and does not help save computation resources because we don’t need to evaluate an expert only when . Thus the MoE layer only keeps the top  values. It also adds tunable Gaussian noise into  to improve load balancing. This mechanism is called _noisy top-k gating_.

where the superscript  denotes the i-th dimension of the vector . The function  selected the top  dimensions with highest values by setting other dimensions to .

To avoid the self-reinforcing effect that the gating network may favor a few strong experts all the time, [Shazeer et al. (2017)](https://arxiv.org/abs/1701.06538) proposed a soft constraint via an additional importance loss to encourage all the experts to have the same weights. It is equivalent to the square of the [coefficient of variation](https://en.wikipedia.org/wiki/Coefficient_of_variation) of batchwise average value per expert.

where  is the coefficient of variation and the loss weight  is a hyperparameter to tune.

Because every expert network only gets a fraction of training samples (“The shrinking batch problem”), we should try to use a batch size as large as possible in MoE. However, it is restricted by GPU memory. Data parallelism and model parallelism can be applied to improve the throughput.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/moe-experiments.png)

Test perplexity on 1-Billion-Word language modeling benchmark. (Left) The model capacity increases from left to right, containing 4, 32, 256, 256, 1024 and 4096 experts. (Right) Performance of the 4 billion parameters MoE model, the largest one in the left figure, under different computation budgets. (Image source: [Shazeer et al., 2017](https://arxiv.org/abs/1701.06538))

**GShard** ([Lepikhin et al., 2020](https://arxiv.org/abs/2006.16668)) scales the MoE transformer model up to 600 billion parameters with sharding. The MoE transformer replaces every other feed forward layer with a MoE layer. The _sharded MoE transformer_ only has the MoE layers sharded across multiple machines, while other layers are simply duplicated.

There are several improved designs for the gating function  in GShard:

- _Expert capacity_: The amount of tokens going through one expert should not go above a threshold, named “expert capacity”. If a token is routed to experts that have reached their capacity, the token would be marked “overflowed” and the gating output is changed to a zero vector.
- _Local group dispatching_: Tokens are evenly partitioned into multiple local groups and the expert capacity is enforced on the group level.
- _Auxiliary loss_: The motivation is similar to the original MoE aux loss. They add an auxiliary loss to minimize the mean square of the fraction of data routed to each expert.
- _Random routing_: The 2nd-best expert is selected with a probability proportional to its weight; otherwise, GShard follows a random routing, so as to add some randomness.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/gshard-algo.png)

Pseudo code of the group-level top-2 gating mechanism with auxiliary loss in GShard. (Image source: [Lepikhin et al., 2020](https://arxiv.org/abs/2006.16668))

**Switch Transformer** ([Fedus et al. 2021](https://arxiv.org/abs/2101.03961)) scales the model size up to trillions of parameters (!!) by replacing the dense feed forward layer with a _sparse switch FFN layer_ in which each input is only routed to _one_ expert network. The auxiliary loss for load balancing is  given  experts, where  is the fraction of tokens routed to the -th expert and  is the routing probability for expert  predicted by the gating network.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/switch-transformer.png)

Switch transformer. The sparse switch FFN layer is in the blue boxes. (Image source: [Fedus et al. 2021](https://arxiv.org/abs/2101.03961))

To improve training stability, switch transformer incorporates the following designs:

- _Selective precision_. They showed that selectively casting only a local part of the model to FP32 precision improves stability, while avoiding the expensive communication cost of FP32 tensors. The FP32 precision is only used within the body of the router function and the results are recast to FP16.
- _Smaller initialization_. The initialization of weight matrices is sampled from a truncated normal distribution with mean  and stdev . They also recommended reducing the transformer initialization scale parameter  to .
- _Use higher expert dropout_. Fine-tuning often works with a small dataset. To avoid overfitting, the dropout rate within each expert is increased by a significant amount. Interestingly they found that increasing dropout across all layers lead to poor performance. In the paper, they used a dropout rate 0.1 at non-expert layers but 0.4 within expert FF layers.

The switch transformer paper summarized different data and model parallelism strategies for training large models with a nice illustration:

![](https://lilianweng.github.io/posts/2021-09-25-train-large/switch-transformer-parallelism.png)

An illustration of various parallelism strategies on how (Top) model weights and (Bottom) data are split over multiple GPU cores. In the top row, each color denotes a unique weight matrix. In the bottom row, different colors indicate different sets of tokens. (Image source: [Fedus et al. 2021](https://arxiv.org/abs/2101.03961))

Both GShard top-2 and Switch Transformer top-1 depend on _token choice_, where each token picks the best one or two experts to route through. They both adopt an auxiliary loss to encourage more balanced load allocation but it does not guarantee the best performance. Furthermore, the expert capacity limit may lead to wasted tokens as they would be discarded if an expert reaches its capacity limit.

**Export Choice (EC)** ([Zhou et al. 2022](https://arxiv.org/abs/2202.09368)) routing instead enables each expert to select the top- tokens. In this way, each expert naturally guarantees a fixed capacity and each token may be routed to multiple experts. EC can achieve perfect load balancing and is shown to improve training convergence by 2x.

Given  experts and an input matrix , the token-to-expert affinity scores are computed by:

A token-to-expert assignment is represented by three matrices,  and .  annotates which token is the -th selection by the -th expert. The gating matrix  stores the routing weights of selected tokens.  is the one-hot version of , used to produce the input matrix () for the gated FFN layer.

One regularization that export choice routing explored is to limit the maximum number of experts per token.

where each entry  in  marks whether the -the expert selects the -th token. Solving this is non-trivial. The paper used [Dykstra’s algorithm](https://projecteuclid.org/journals/annals-of-probability/volume-13/issue-3/An-Iterative-Procedure-for-Obtaining-I-Projections-onto-the-Intersection/10.1214/aop/1176992918.full) that runs a sequence of multiple iterative computation steps. Capped expert choice results in a slight decrease in the fine-tuning performance in the experiments.

The parameter  is determined by , where  is the total number of tokens in one batch and  is a capacity factor indicating the average number of experts used by one token. The paper used  in most experiments, but EC with  still outperforms the top-1 token choice gating. Interestingly,  only marginally hurts the training performance.

One big drawback of EC is that it does not work when the batch size is too small, neither for auto-regressive text generation, because it needs to know the future tokens to do the top- selection.

# Other Memory Saving Designs

## CPU Offloading

When the GPU memory is full, one option is to offload temporarily unused data to CPU and read them back when needed later ([Rhu et al. 2016](https://arxiv.org/abs/1602.08124)). The idea of **CPU offloading** is straightforward but is less popular in recent years due to the slowdown it brings into the training time.

## Activation Recomputation

**Activation recomputation** (also known as “activation checkpointing” or “gradient checkpointing”; [Chen et al. 2016](https://arvix.org/abs/1604.06174)) is a smart yet simple idea to reduce memory footprint at the cost of computation time. It reduces the memory cost of training a  layer deep neural net to , which only additionally consumes an extra forward pass computation per batch.

Let’s say, we evenly divide an -layer network into  partitions. Only activations at partition boundaries are saved and communicated between workers. Intermediate activations at intra-partition layers are still needed for computing gradients so they are recomputed during backward passes. With activation recomputation, the memory cost for training  is:

The minimum cost is  at .

Activation recompuation trick can give sublinear memory cost with respect to the model size.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/activation-checkpointing.png)

The memory cost of different memory saving algorithms. Sharing: Memory used by intermediate results is recycled when no longer needed. Inplace: Save the output directly into memory of an input value. (Image source: [Chen et al. 2016](https://arvix.org/abs/1604.06174))

## Mixed Precision Training

[Narang & Micikevicius et al. (2018)](https://arxiv.org/abs/1710.03740) introduced a method to train models using half-precision floating point (FP16) numbers without losing model accuracy.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/mixed-precision-training.png)

The procedure of mixed precision training at one layer. (Image source: [Narang & Micikevicius, et al. 2018](https://arxiv.org/abs/1710.03740))

Three techniques to avoid losing critical information at half-precision:

- _Full-precision master copy of weights_. Maintain a full precision (FP32) copy of model weights that accumulates gradients. The numbers are rounded up to half-precision for forward & backward passes. The motivation is that each gradient update (i.e. gradient times the learning rate) might be too small to be fully contained within the FP16 range (i.e.  becomes zero in FP16).
- _Loss scaling_. Scale up the loss to better handle gradients with small magnitudes (See Fig. 16). Scaling up the gradients helps shift them to occupy a larger section towards the right section (containing larger values) of the representable range, preserving values that are otherwise lost.
- _Arithmetic precision_. For common network arithmetic (e.g. vector dot-product, reduction by summing up vector elements), we can accumulate the partial results in FP32 and then save the final output as FP16 before saving into memory. Point-wise operations can be executed in either FP16 or FP32.

![](https://lilianweng.github.io/posts/2021-09-25-train-large/gradient-histogram.png)

The histogram of gradients in full precision. The left part up to  will be zero-ed off once the model switches to FP16. (Image source: [Narang & Micikevicius, et al. 2018](https://arxiv.org/abs/1710.03740))

In their experiments, loss scaling is not needed for some networks (e.g. image classification, Faster R-CNN), but necessary for others (e.g. Multibox SSD, big LSTM language model).

## Compression

Intermediate results often consume a lot of memory, although they are only needed in one forward pass and one backward pass. There is a noticeable temporal gap between these two uses. Thus [Jain et al. (2018)](https://www.microsoft.com/en-us/research/uploads/prod/2018/04/fiddle-gist-isca18.pdf) proposed a data encoding strategy to compress the intermediate results after the first use in the first pass and then decode it back for back-propagation later.

Their system _Gist_ incorporates two encoding schemes: _Layer-specific lossless encoding_; focus on ReLU-Pool (“Binarize”) and ReLU-Conv (“Sparse storage and dense computation”) patterns. _Aggressive lossy encoding_; use delayed precision reduction (DPR). They observed that the first immediate use of feature maps should be kept at high precision but the second use can tolerate lower precision.

The experiments showed that Gist can reduce the memory cost by 2x across 5 SOTA image classification DNNs, with an average of 1.8x with only 4% performance overhead.

## Memory Efficient Optimizer

Optimizers are eager for memory consumption. Take the popular Adam optimizer as an example, it internally needs to maintain momentums and variances, both at the same scale as gradients and model parameters. All out of a sudden, we need to save 4x the memory of model weights.

Several optimizers have been proposed to reduce the memory footprint. For example, instead of storing the full momentums and variations as in Adam, _Adafactor_ ([Shazeer et al. 2018](https://arxiv.org/abs/1804.04235)) only tracks the per-row and per-column sums of the moving averages and then estimates the second moments based on these sums. _SM3_ ([Anil et al. 2019](https://arxiv.org/abs/1901.11150)) describes a different adaptive optimization method, leading to largely reduced memory as well.

_ZeRO_ (_Zero Redundancy Optimizer_; [Rajbhandari et al. 2019](https://arxiv.org/abs/1910.02054)) optimizes the memory used for training large models based on the observation about two major memory consumption of large model training:

1. The majority is occupied by _model states_, including optimizer states (e.g. Adam momentums and variances), gradients and parameters. Mixed-precision training demands a lot of memory since the optimizer needs to keep a copy of FP32 parameters and other optimizer states, besides the FP16 version.
2. The remaining is consumed by activations, temporary buffers and unusable fragmented memory (named _residual states_ in the paper).

ZeRO combines two approaches, _ZeRO-DP_ and _ZeRO-R_. ZeRO-DP is an enhanced data parallelism to avoid simple redundancy over model states. It partitions optimizer state, gradients and parameters across multiple data parallel processes via a dynamic communication schedule to minimize the communication volume. ZeRO-R optimizes the memory consumption of residual states, using partitioned activation recomputation, constant buffer size and on-the-fly memory defragmentation.

# Citation

Cited as:

> Weng, Lilian. (Sep 2021). How to train really large models on many GPUs? Lil’Log. https://lilianweng.github.io/posts/2021-09-25-train-large/.

Or

```
@article{weng2021large,
  title   = "How to Train Really Large Models on Many GPUs?",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io",
  year    = "2021",
  month   = "Sep",
  url     = "https://lilianweng.github.io/posts/2021-09-25-train-large/"
}
```

# References

[1] Li et al. [“PyTorch Distributed: Experiences on Accelerating Data Parallel Training”](https://arxiv.org/abs/2006.15704) VLDB 2020.

[2] Cui et al. [“GeePS: Scalable deep learning on distributed GPUs with a GPU-specialized parameter server”](https://www.pdl.cmu.edu/PDL-FTP/CloudComputing/GeePS-cui-eurosys16.pdf) EuroSys 2016

[3] Shoeybi et al. [“Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism.”](https://arxiv.org/abs/1909.08053) arXiv preprint arXiv:1909.08053 (2019).

[4] Narayanan et al. [“Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM.”](https://arxiv.org/abs/2104.04473) arXiv preprint arXiv:2104.04473 (2021).

[5] Huang et al. [“GPipe: Efficient Training of Giant Neural Networks using Pipeline Parallelism.”](https://arxiv.org/abs/1811.06965) arXiv preprint arXiv:1811.06965 (2018).

[6] Narayanan et al. [“PipeDream: Generalized Pipeline Parallelism for DNN Training.”](https://cs.stanford.edu/~matei/papers/2019/sosp_pipedream.pdf) SOSP 2019.

[7] Narayanan et al. [“Memory-Efficient Pipeline-Parallel DNN Training.”](https://arxiv.org/abs/2006.09503) ICML 2021.

[8] Shazeer et al. [“The Sparsely-Gated Mixture-of-Experts Layer Noam.”](https://arxiv.org/abs/1701.06538) arXiv preprint arXiv:1701.06538 (2017).

[9] Lepikhin et al. [“GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding.”](https://arxiv.org/abs/2006.16668) arXiv preprint arXiv:2006.16668 (2020).

[10] Fedus et al. [“Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity.”](https://arxiv.org/abs/2101.03961) arXiv preprint arXiv:2101.03961 (2021).

[11] Narang & Micikevicius, et al. [“Mixed precision training.”](https://arxiv.org/abs/1710.03740) ICLR 2018.

[12] Chen et al. 2016 [“Training Deep Nets with Sublinear Memory Cost.”](https://arxiv.org/abs/1604.06174) arXiv preprint arXiv:1604.06174 (2016).

[13] Jain et al. [“Gist: Efficient data encoding for deep neural network training.”](https://www.microsoft.com/en-us/research/uploads/prod/2018/04/fiddle-gist-isca18.pdf) ISCA 2018.

[14] Shazeer & Stern. [“Adafactor: Adaptive learning rates with sublinear memory cost.”](https://arxiv.org/abs/1804.04235) arXiv preprint arXiv:1804.04235 (2018).

[15] Anil et al. [“Memory-Efficient Adaptive Optimization.”](https://arxiv.org/abs/1901.11150) arXiv preprint arXiv:1901.11150 (2019).

[16] Rajbhandari et al. [“ZeRO: Memory Optimization Towards Training A Trillion Parameter Models Samyam.”](https://arxiv.org/abs/1910.02054) arXiv preprint arXiv:1910.02054 (2019).

[17] Zhou et al. [“Mixture-of-Experts with Expert Choice Routing”](https://arxiv.org/abs/2202.09368) arXiv preprint arXiv:2202.09368 (2022).<!-- Paste article content / notes here before running raw-material-processor -->
