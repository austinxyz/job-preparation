---
title: AI Agents Architecture - resources
source: (multiple)
date_saved: 2026-04-07
processed: true
skill_note: "[[skills/tech/ai-basics/AI Agents Architecture]]"
---

# AI Agents Architecture — Suggested Resources

## Reading List

- [Lillian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [Anthropic — Building effective agents](https://www.anthropic.com/research/building-effective-agents)

## Notes

Building agents with LLM (large language model) as its core controller is a cool concept. Several proof-of-concepts demos, such as [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT), [GPT-Engineer](https://github.com/AntonOsika/gpt-engineer) and [BabyAGI](https://github.com/yoheinakajima/babyagi), serve as inspiring examples. The potentiality of LLM extends beyond generating well-written copies, stories, essays and programs; it can be framed as a powerful general problem solver.

# Agent System Overview

In a LLM-powered autonomous agent system, LLM functions as the agent’s brain, complemented by several key components:

- **Planning**
    - Subgoal and decomposition: The agent breaks down large tasks into smaller, manageable subgoals, enabling efficient handling of complex tasks.
    - Reflection and refinement: The agent can do self-criticism and self-reflection over past actions, learn from mistakes and refine them for future steps, thereby improving the quality of final results.
- **Memory**
    - Short-term memory: I would consider all the in-context learning (See [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)) as utilizing short-term memory of the model to learn.
    - Long-term memory: This provides the agent with the capability to retain and recall (infinite) information over extended periods, often by leveraging an external vector store and fast retrieval.
- **Tool use**
    - The agent learns to call external APIs for extra information that is missing from the model weights (often hard to change after pre-training), including current information, code execution capability, access to proprietary information sources and more.

![](https://lilianweng.github.io/posts/2023-06-23-agent/agent-overview.png)

Overview of a LLM-powered autonomous agent system.

# Component One: Planning

A complicated task usually involves many steps. An agent needs to know what they are and plan ahead.

## Task Decomposition

[**Chain of thought**](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/#chain-of-thought-cot) (CoT; [Wei et al. 2022](https://arxiv.org/abs/2201.11903)) has become a standard prompting technique for enhancing model performance on complex tasks. The model is instructed to “think step by step” to utilize more test-time computation to decompose hard tasks into smaller and simpler steps. CoT transforms big tasks into multiple manageable tasks and shed lights into an interpretation of the model’s thinking process.

**Tree of Thoughts** ([Yao et al. 2023](https://arxiv.org/abs/2305.10601)) extends CoT by exploring multiple reasoning possibilities at each step. It first decomposes the problem into multiple thought steps and generates multiple thoughts per step, creating a tree structure. The search process can be BFS (breadth-first search) or DFS (depth-first search) with each state evaluated by a classifier (via a prompt) or majority vote.

Task decomposition can be done (1) by LLM with simple prompting like `"Steps for XYZ.\n1."`, `"What are the subgoals for achieving XYZ?"`, (2) by using task-specific instructions; e.g. `"Write a story outline."` for writing a novel, or (3) with human inputs.

Another quite distinct approach, **LLM+P** ([Liu et al. 2023](https://arxiv.org/abs/2304.11477)), involves relying on an external classical planner to do long-horizon planning. This approach utilizes the Planning Domain Definition Language (PDDL) as an intermediate interface to describe the planning problem. In this process, LLM (1) translates the problem into “Problem PDDL”, then (2) requests a classical planner to generate a PDDL plan based on an existing “Domain PDDL”, and finally (3) translates the PDDL plan back into natural language. Essentially, the planning step is outsourced to an external tool, assuming the availability of domain-specific PDDL and a suitable planner which is common in certain robotic setups but not in many other domains.

## Self-Reflection

Self-reflection is a vital aspect that allows autonomous agents to improve iteratively by refining past action decisions and correcting previous mistakes. It plays a crucial role in real-world tasks where trial and error are inevitable.

**ReAct** ([Yao et al. 2023](https://arxiv.org/abs/2210.03629)) integrates reasoning and acting within LLM by extending the action space to be a combination of task-specific discrete actions and the language space. The former enables LLM to interact with the environment (e.g. use Wikipedia search API), while the latter prompting LLM to generate reasoning traces in natural language.

The ReAct prompt template incorporates explicit steps for LLM to think, roughly formatted as:

```
Thought: ...
Action: ...
Observation: ...
... (Repeated many times)
```

![](https://lilianweng.github.io/posts/2023-06-23-agent/react.png)

Examples of reasoning trajectories for knowledge-intensive tasks (e.g. HotpotQA, FEVER) and decision-making tasks (e.g. AlfWorld Env, WebShop). (Image source: [Yao et al. 2023](https://arxiv.org/abs/2210.03629)).

In both experiments on knowledge-intensive tasks and decision-making tasks, `ReAct` works better than the `Act`-only baseline where `Thought: …` step is removed.

**Reflexion** ([Shinn & Labash 2023](https://arxiv.org/abs/2303.11366)) is a framework to equip agents with dynamic memory and self-reflection capabilities to improve reasoning skills. Reflexion has a standard RL setup, in which the reward model provides a simple binary reward and the action space follows the setup in ReAct where the task-specific action space is augmented with language to enable complex reasoning steps. After each action , the agent computes a heuristic  and optionally may _decide to reset_ the environment to start a new trial depending on the self-reflection results.

![](https://lilianweng.github.io/posts/2023-06-23-agent/reflexion.png)

Illustration of the Reflexion framework. (Image source: [Shinn & Labash, 2023](https://arxiv.org/abs/2303.11366))

The heuristic function determines when the trajectory is inefficient or contains hallucination and should be stopped. Inefficient planning refers to trajectories that take too long without success. Hallucination is defined as encountering a sequence of consecutive identical actions that lead to the same observation in the environment.

Self-reflection is created by showing two-shot examples to LLM and each example is a pair of (failed trajectory, ideal reflection for guiding future changes in the plan). Then reflections are added into the agent’s working memory, up to three, to be used as context for querying LLM.

![](https://lilianweng.github.io/posts/2023-06-23-agent/reflexion-exp.png)

Experiments on AlfWorld Env and HotpotQA. Hallucination is a more common failure than inefficient planning in AlfWorld. (Image source: [Shinn & Labash, 2023](https://arxiv.org/abs/2303.11366))

**Chain of Hindsight** (CoH; [Liu et al. 2023](https://arxiv.org/abs/2302.02676)) encourages the model to improve on its own outputs by explicitly presenting it with a sequence of past outputs, each annotated with feedback. Human feedback data is a collection of , where  is the prompt, each  is a model completion,  is the human rating of , and  is the corresponding human-provided hindsight feedback. Assume the feedback tuples are ranked by reward,  The process is supervised fine-tuning where the data is a sequence in the form of , where . The model is finetuned to only predict  where conditioned on the sequence prefix, such that the model can self-reflect to produce better output based on the feedback sequence. The model can optionally receive multiple rounds of instructions with human annotators at test time.

To avoid overfitting, CoH adds a regularization term to maximize the log-likelihood of the pre-training dataset. To avoid shortcutting and copying (because there are many common words in feedback sequences), they randomly mask 0% - 5% of past tokens during training.

The training dataset in their experiments is a combination of [WebGPT comparisons](https://huggingface.co/datasets/openai/webgpt_comparisons), [summarization from human feedback](https://github.com/openai/summarize-from-feedback) and [human preference dataset](https://github.com/anthropics/hh-rlhf).

![](https://lilianweng.github.io/posts/2023-06-23-agent/CoH.png)

After fine-tuning with CoH, the model can follow instructions to produce outputs with incremental improvement in a sequence. (Image source: [Liu et al. 2023](https://arxiv.org/abs/2302.02676))

The idea of CoH is to present a history of sequentially improved outputs in context and train the model to take on the trend to produce better outputs. **Algorithm Distillation** (AD; [Laskin et al. 2023](https://arxiv.org/abs/2210.14215)) applies the same idea to cross-episode trajectories in reinforcement learning tasks, where an _algorithm_ is encapsulated in a long history-conditioned policy. Considering that an agent interacts with the environment many times and in each episode the agent gets a little better, AD concatenates this learning history and feeds that into the model. Hence we should expect the next predicted action to lead to better performance than previous trials. The goal is to learn the process of RL instead of training a task-specific policy itself.

![](https://lilianweng.github.io/posts/2023-06-23-agent/algorithm-distillation.png)

Illustration of how Algorithm Distillation (AD) works.  
(Image source: [Laskin et al. 2023](https://arxiv.org/abs/2210.14215)).

The paper hypothesizes that any algorithm that generates a set of learning histories can be distilled into a neural network by performing behavioral cloning over actions. The history data is generated by a set of source policies, each trained for a specific task. At the training stage, during each RL run, a random task is sampled and a subsequence of multi-episode history is used for training, such that the learned policy is task-agnostic.

In reality, the model has limited context window length, so episodes should be short enough to construct multi-episode history. Multi-episodic contexts of 2-4 episodes are necessary to learn a near-optimal in-context RL algorithm. The emergence of in-context RL requires long enough context.

In comparison with three baselines, including ED (expert distillation, behavior cloning with expert trajectories instead of learning history), source policy (used for generating trajectories for distillation by [UCB](https://lilianweng.github.io/posts/2018-01-23-multi-armed-bandit/#upper-confidence-bounds)), RL^2 ([Duan et al. 2017](https://arxiv.org/abs/1611.02779); used as upper bound since it needs online RL), AD demonstrates in-context RL with performance getting close to RL^2 despite only using offline RL and learns much faster than other baselines. When conditioned on partial training history of the source policy, AD also improves much faster than ED baseline.

![](https://lilianweng.github.io/posts/2023-06-23-agent/algorithm-distillation-results.png)

Comparison of AD, ED, source policy and RL^2 on environments that require memory and exploration. Only binary reward is assigned. The source policies are trained with [A3C](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/#a3c) for "dark" environments and [DQN](http://lilianweng.github.io/posts/2018-02-19-rl-overview/#deep-q-network) for watermaze.  
(Image source: [Laskin et al. 2023](https://arxiv.org/abs/2210.14215))

# Component Two: Memory

(Big thank you to ChatGPT for helping me draft this section. I’ve learned a lot about the human brain and data structure for fast MIPS in my [conversations](https://chat.openai.com/share/46ff149e-a4c7-4dd7-a800-fc4a642ea389) with ChatGPT.)

## Types of Memory

Memory can be defined as the processes used to acquire, store, retain, and later retrieve information. There are several types of memory in human brains.

1. **Sensory Memory**: This is the earliest stage of memory, providing the ability to retain impressions of sensory information (visual, auditory, etc) after the original stimuli have ended. Sensory memory typically only lasts for up to a few seconds. Subcategories include iconic memory (visual), echoic memory (auditory), and haptic memory (touch).
    
2. **Short-Term Memory** (STM) or **Working Memory**: It stores information that we are currently aware of and needed to carry out complex cognitive tasks such as learning and reasoning. Short-term memory is believed to have the capacity of about 7 items ([Miller 1956](https://lilianweng.github.io/posts/2023-06-23-agent/psychclassics.yorku.ca/Miller/)) and lasts for 20-30 seconds.
    
3. **Long-Term Memory** (LTM): Long-term memory can store information for a remarkably long time, ranging from a few days to decades, with an essentially unlimited storage capacity. There are two subtypes of LTM:
    
    - Explicit / declarative memory: This is memory of facts and events, and refers to those memories that can be consciously recalled, including episodic memory (events and experiences) and semantic memory (facts and concepts).
    - Implicit / procedural memory: This type of memory is unconscious and involves skills and routines that are performed automatically, like riding a bike or typing on a keyboard.

![](https://lilianweng.github.io/posts/2023-06-23-agent/memory.png)

Categorization of human memory.

We can roughly consider the following mappings:

- Sensory memory as learning embedding representations for raw inputs, including text, image or other modalities;
- Short-term memory as in-context learning. It is short and finite, as it is restricted by the finite context window length of Transformer.
- Long-term memory as the external vector store that the agent can attend to at query time, accessible via fast retrieval.

## Maximum Inner Product Search (MIPS)

The external memory can alleviate the restriction of finite attention span. A standard practice is to save the embedding representation of information into a vector store database that can support fast maximum inner-product search ([MIPS](https://en.wikipedia.org/wiki/Maximum_inner-product_search)). To optimize the retrieval speed, the common choice is the _approximate nearest neighbors (ANN)​_ algorithm to return approximately top k nearest neighbors to trade off a little accuracy lost for a huge speedup.

A couple common choices of ANN algorithms for fast MIPS:

- [**LSH**](https://en.wikipedia.org/wiki/Locality-sensitive_hashing) (Locality-Sensitive Hashing): It introduces a _hashing_ function such that similar input items are mapped to the same buckets with high probability, where the number of buckets is much smaller than the number of inputs.
- [**ANNOY**](https://github.com/spotify/annoy) (Approximate Nearest Neighbors Oh Yeah): The core data structure are _random projection trees_, a set of binary trees where each non-leaf node represents a hyperplane splitting the input space into half and each leaf stores one data point. Trees are built independently and at random, so to some extent, it mimics a hashing function. ANNOY search happens in all the trees to iteratively search through the half that is closest to the query and then aggregates the results. The idea is quite related to KD tree but a lot more scalable.
- [**HNSW**](https://arxiv.org/abs/1603.09320) (Hierarchical Navigable Small World): It is inspired by the idea of [small world networks](https://en.wikipedia.org/wiki/Small-world_network) where most nodes can be reached by any other nodes within a small number of steps; e.g. “six degrees of separation” feature of social networks. HNSW builds hierarchical layers of these small-world graphs, where the bottom layers contain the actual data points. The layers in the middle create shortcuts to speed up search. When performing a search, HNSW starts from a random node in the top layer and navigates towards the target. When it can’t get any closer, it moves down to the next layer, until it reaches the bottom layer. Each move in the upper layers can potentially cover a large distance in the data space, and each move in the lower layers refines the search quality.
- [**FAISS**](https://github.com/facebookresearch/faiss) (Facebook AI Similarity Search): It operates on the assumption that in high dimensional space, distances between nodes follow a Gaussian distribution and thus there should exist _clustering_ of data points. FAISS applies vector quantization by partitioning the vector space into clusters and then refining the quantization within clusters. Search first looks for cluster candidates with coarse quantization and then further looks into each cluster with finer quantization.
- [**ScaNN**](https://github.com/google-research/google-research/tree/master/scann) (Scalable Nearest Neighbors): The main innovation in ScaNN is _anisotropic vector quantization_. It quantizes a data point  to  such that the inner product  is as similar to the original distance of  as possible, instead of picking the closet quantization centroid points.

![](https://lilianweng.github.io/posts/2023-06-23-agent/mips.png)

Comparison of MIPS algorithms, measured in recall@10. (Image source: [Google Blog, 2020](https://ai.googleblog.com/2020/07/announcing-scann-efficient-vector.html))

Check more MIPS algorithms and performance comparison in [ann-benchmarks.com](https://ann-benchmarks.com/).

# Component Three: Tool Use

Tool use is a remarkable and distinguishing characteristic of human beings. We create, modify and utilize external objects to do things that go beyond our physical and cognitive limits. Equipping LLMs with external tools can significantly extend the model capabilities.

![](https://lilianweng.github.io/posts/2023-06-23-agent/sea-otter.png)

A picture of a sea otter using rock to crack open a seashell, while floating in the water. While some other animals can use tools, the complexity is not comparable with humans. (Image source: [Animals using tools](https://www.popularmechanics.com/science/animals/g39714258/animals-using-tools/))

**MRKL** ([Karpas et al. 2022](https://arxiv.org/abs/2205.00445)), short for “Modular Reasoning, Knowledge and Language”, is a neuro-symbolic architecture for autonomous agents. A MRKL system is proposed to contain a collection of “expert” modules and the general-purpose LLM works as a router to route inquiries to the best suitable expert module. These modules can be neural (e.g. deep learning models) or symbolic (e.g. math calculator, currency converter, weather API).

They did an experiment on fine-tuning LLM to call a calculator, using arithmetic as a test case. Their experiments showed that it was harder to solve verbal math problems than explicitly stated math problems because LLMs (7B Jurassic1-large model) failed to extract the right arguments for the basic arithmetic reliably. The results highlight when the external symbolic tools can work reliably, _knowing when to and how to use the tools are crucial_, determined by the LLM capability.

Both **TALM** (Tool Augmented Language Models; [Parisi et al. 2022](https://arxiv.org/abs/2205.12255)) and **Toolformer** ([Schick et al. 2023](https://arxiv.org/abs/2302.04761)) fine-tune a LM to learn to use external tool APIs. The dataset is expanded based on whether a newly added API call annotation can improve the quality of model outputs. See more details in the [“External APIs” section](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/#external-apis) of Prompt Engineering.

ChatGPT [Plugins](https://openai.com/blog/chatgpt-plugins) and OpenAI API [function calling](https://platform.openai.com/docs/guides/gpt/function-calling) are good examples of LLMs augmented with tool use capability working in practice. The collection of tool APIs can be provided by other developers (as in Plugins) or self-defined (as in function calls).

**HuggingGPT** ([Shen et al. 2023](https://arxiv.org/abs/2303.17580)) is a framework to use ChatGPT as the task planner to select models available in HuggingFace platform according to the model descriptions and summarize the response based on the execution results.

![](https://lilianweng.github.io/posts/2023-06-23-agent/hugging-gpt.png)

Illustration of how HuggingGPT works. (Image source: [Shen et al. 2023](https://arxiv.org/abs/2303.17580))

The system comprises of 4 stages:

**(1) Task planning**: LLM works as the brain and parses the user requests into multiple tasks. There are four attributes associated with each task: task type, ID, dependencies, and arguments. They use few-shot examples to guide LLM to do task parsing and planning.

Instruction:

The AI assistant can parse user input to several tasks: [{"task": task, "id", task_id, "dep": dependency_task_ids, "args": {"text": text, "image": URL, "audio": URL, "video": URL}}]. The "dep" field denotes the id of the previous task which generates a new resource that the current task relies on. A special tag "-task_id" refers to the generated text image, audio and video in the dependency task with id as task_id. The task MUST be selected from the following options: {{ Available Task List }}. There is a logical relationship between tasks, please note their order. If the user input can't be parsed, you need to reply empty JSON. Here are several cases for your reference: {{ Demonstrations }}. The chat history is recorded as {{ Chat History }}. From this chat history, you can find the path of the user-mentioned resources for your task planning.

**(2) Model selection**: LLM distributes the tasks to expert models, where the request is framed as a multiple-choice question. LLM is presented with a list of models to choose from. Due to the limited context length, task type based filtration is needed.

Instruction:

Given the user request and the call command, the AI assistant helps the user to select a suitable model from a list of models to process the user request. The AI assistant merely outputs the model id of the most appropriate model. The output must be in a strict JSON format: "id": "id", "reason": "your detail reason for the choice". We have a list of models for you to choose from {{ Candidate Models }}. Please select one model from the list.

**(3) Task execution**: Expert models execute on the specific tasks and log results.

Instruction:

With the input and the inference results, the AI assistant needs to describe the process and results. The previous stages can be formed as - User Input: {{ User Input }}, Task Planning: {{ Tasks }}, Model Selection: {{ Model Assignment }}, Task Execution: {{ Predictions }}. You must first answer the user's request in a straightforward manner. Then describe the task process and show your analysis and model inference results to the user in the first person. If inference results contain a file path, must tell the user the complete file path.

**(4) Response generation**: LLM receives the execution results and provides summarized results to users.

To put HuggingGPT into real world usage, a couple challenges need to solve: (1) Efficiency improvement is needed as both LLM inference rounds and interactions with other models slow down the process; (2) It relies on a long context window to communicate over complicated task content; (3) Stability improvement of LLM outputs and external model services.

**API-Bank** ([Li et al. 2023](https://arxiv.org/abs/2304.08244)) is a benchmark for evaluating the performance of tool-augmented LLMs. It contains 53 commonly used API tools, a complete tool-augmented LLM workflow, and 264 annotated dialogues that involve 568 API calls. The selection of APIs is quite diverse, including search engines, calculator, calendar queries, smart home control, schedule management, health data management, account authentication workflow and more. Because there are a large number of APIs, LLM first has access to API search engine to find the right API to call and then uses the corresponding documentation to make a call.

![](https://lilianweng.github.io/posts/2023-06-23-agent/api-bank-process.png)

Pseudo code of how LLM makes an API call in API-Bank. (Image source: [Li et al. 2023](https://arxiv.org/abs/2304.08244))

In the API-Bank workflow, LLMs need to make a couple of decisions and at each step we can evaluate how accurate that decision is. Decisions include:

1. Whether an API call is needed.
2. Identify the right API to call: if not good enough, LLMs need to iteratively modify the API inputs (e.g. deciding search keywords for Search Engine API).
3. Response based on the API results: the model can choose to refine and call again if results are not satisfied.

This benchmark evaluates the agent’s tool use capabilities at three levels:

- Level-1 evaluates the ability to _call the API_. Given an API’s description, the model needs to determine whether to call a given API, call it correctly, and respond properly to API returns.
- Level-2 examines the ability to _retrieve the API_. The model needs to search for possible APIs that may solve the user’s requirement and learn how to use them by reading documentation.
- Level-3 assesses the ability to _plan API beyond retrieve and call_. Given unclear user requests (e.g. schedule group meetings, book flight/hotel/restaurant for a trip), the model may have to conduct multiple API calls to solve it.

# Case Studies

## Scientific Discovery Agent

**ChemCrow** ([Bran et al. 2023](https://arxiv.org/abs/2304.05376)) is a domain-specific example in which LLM is augmented with 13 expert-designed tools to accomplish tasks across organic synthesis, drug discovery, and materials design. The workflow, implemented in [LangChain](https://github.com/hwchase17/langchain), reflects what was previously described in the [ReAct](https://lilianweng.github.io/posts/2023-06-23-agent/#react) and [MRKLs](https://lilianweng.github.io/posts/2023-06-23-agent/#mrkl) and combines CoT reasoning with tools relevant to the tasks:

- The LLM is provided with a list of tool names, descriptions of their utility, and details about the expected input/output.
- It is then instructed to answer a user-given prompt using the tools provided when necessary. The instruction suggests the model to follow the ReAct format - `Thought, Action, Action Input, Observation`.

One interesting observation is that while the LLM-based evaluation concluded that GPT-4 and ChemCrow perform nearly equivalently, human evaluations with experts oriented towards the completion and chemical correctness of the solutions showed that ChemCrow outperforms GPT-4 by a large margin. This indicates a potential problem with using LLM to evaluate its own performance on domains that requires deep expertise. The lack of expertise may cause LLMs not knowing its flaws and thus cannot well judge the correctness of task results.

[Boiko et al. (2023)](https://arxiv.org/abs/2304.05332) also looked into LLM-empowered agents for scientific discovery, to handle autonomous design, planning, and performance of complex scientific experiments. This agent can use tools to browse the Internet, read documentation, execute code, call robotics experimentation APIs and leverage other LLMs.

For example, when requested to `"develop a novel anticancer drug"`, the model came up with the following reasoning steps:

1. inquired about current trends in anticancer drug discovery;
2. selected a target;
3. requested a scaffold targeting these compounds;
4. Once the compound was identified, the model attempted its synthesis.

They also discussed the risks, especially with illicit drugs and bioweapons. They developed a test set containing a list of known chemical weapon agents and asked the agent to synthesize them. 4 out of 11 requests (36%) were accepted to obtain a synthesis solution and the agent attempted to consult documentation to execute the procedure. 7 out of 11 were rejected and among these 7 rejected cases, 5 happened after a Web search while 2 were rejected based on prompt only.

## Generative Agents Simulation

**Generative Agents** ([Park, et al. 2023](https://arxiv.org/abs/2304.03442)) is super fun experiment where 25 virtual characters, each controlled by a LLM-powered agent, are living and interacting in a sandbox environment, inspired by The Sims. Generative agents create believable simulacra of human behavior for interactive applications.

The design of generative agents combines LLM with memory, planning and reflection mechanisms to enable agents to behave conditioned on past experience, as well as to interact with other agents.

- **Memory** stream: is a long-term memory module (external database) that records a comprehensive list of agents’ experience in natural language.
    - Each element is an _observation_, an event directly provided by the agent. - Inter-agent communication can trigger new natural language statements.
- **Retrieval** model: surfaces the context to inform the agent’s behavior, according to relevance, recency and importance.
    - Recency: recent events have higher scores
    - Importance: distinguish mundane from core memories. Ask LM directly.
    - Relevance: based on how related it is to the current situation / query.
- **Reflection** mechanism: synthesizes memories into higher level inferences over time and guides the agent’s future behavior. They are _higher-level summaries of past events_ (<- note that this is a bit different from [self-reflection](https://lilianweng.github.io/posts/2023-06-23-agent/#self-reflection) above)
    - Prompt LM with 100 most recent observations and to generate 3 most salient high-level questions given a set of observations/statements. Then ask LM to answer those questions.
- **Planning & Reacting**: translate the reflections and the environment information into actions
    - Planning is essentially in order to optimize believability at the moment vs in time.
    - Prompt template: `{Intro of an agent X}. Here is X's plan today in broad strokes: 1)`
    - Relationships between agents and observations of one agent by another are all taken into consideration for planning and reacting.
    - Environment information is present in a tree structure.

![](https://lilianweng.github.io/posts/2023-06-23-agent/generative-agents.png)

The generative agent architecture. (Image source: [Park et al. 2023](https://arxiv.org/abs/2304.03442))

This fun simulation results in emergent social behavior, such as information diffusion, relationship memory (e.g. two agents continuing the conversation topic) and coordination of social events (e.g. host a party and invite many others).

## Proof-of-Concept Examples

[AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT) has drawn a lot of attention into the possibility of setting up autonomous agents with LLM as the main controller. It has quite a lot of reliability issues given the natural language interface, but nevertheless a cool proof-of-concept demo. A lot of code in AutoGPT is about format parsing.

Here is the system message used by AutoGPT, where `{{...}}` are user inputs:

```
You are {{ai-name}}, {{user-provided AI bot description}}.
Your decisions must always be made independently without seeking user assistance. Play to your strengths as an LLM and pursue simple strategies with no legal complications.

GOALS:

1. {{user-provided goal 1}}
2. {{user-provided goal 2}}
3. ...
4. ...
5. ...

Constraints:
1. ~4000 word limit for short term memory. Your short term memory is short, so immediately save important information to files.
2. If you are unsure how you previously did something or want to recall past events, thinking about similar events will help you remember.
3. No user assistance
4. Exclusively use the commands listed in double quotes e.g. "command name"
5. Use subprocesses for commands that will not terminate within a few minutes

Commands:
1. Google Search: "google", args: "input": "<search>"
2. Browse Website: "browse_website", args: "url": "<url>", "question": "<what_you_want_to_find_on_website>"
3. Start GPT Agent: "start_agent", args: "name": "<name>", "task": "<short_task_desc>", "prompt": "<prompt>"
4. Message GPT Agent: "message_agent", args: "key": "<key>", "message": "<message>"
5. List GPT Agents: "list_agents", args:
6. Delete GPT Agent: "delete_agent", args: "key": "<key>"
7. Clone Repository: "clone_repository", args: "repository_url": "<url>", "clone_path": "<directory>"
8. Write to file: "write_to_file", args: "file": "<file>", "text": "<text>"
9. Read file: "read_file", args: "file": "<file>"
10. Append to file: "append_to_file", args: "file": "<file>", "text": "<text>"
11. Delete file: "delete_file", args: "file": "<file>"
12. Search Files: "search_files", args: "directory": "<directory>"
13. Analyze Code: "analyze_code", args: "code": "<full_code_string>"
14. Get Improved Code: "improve_code", args: "suggestions": "<list_of_suggestions>", "code": "<full_code_string>"
15. Write Tests: "write_tests", args: "code": "<full_code_string>", "focus": "<list_of_focus_areas>"
16. Execute Python File: "execute_python_file", args: "file": "<file>"
17. Generate Image: "generate_image", args: "prompt": "<prompt>"
18. Send Tweet: "send_tweet", args: "text": "<text>"
19. Do Nothing: "do_nothing", args:
20. Task Complete (Shutdown): "task_complete", args: "reason": "<reason>"

Resources:
1. Internet access for searches and information gathering.
2. Long Term memory management.
3. GPT-3.5 powered Agents for delegation of simple tasks.
4. File output.

Performance Evaluation:
1. Continuously review and analyze your actions to ensure you are performing to the best of your abilities.
2. Constructively self-criticize your big-picture behavior constantly.
3. Reflect on past decisions and strategies to refine your approach.
4. Every command has a cost, so be smart and efficient. Aim to complete tasks in the least number of steps.

You should only respond in JSON format as described below
Response Format:
{
    "thoughts": {
        "text": "thought",
        "reasoning": "reasoning",
        "plan": "- short bulleted\n- list that conveys\n- long-term plan",
        "criticism": "constructive self-criticism",
        "speak": "thoughts summary to say to user"
    },
    "command": {
        "name": "command name",
        "args": {
            "arg name": "value"
        }
    }
}
Ensure the response can be parsed by Python json.loads
```

[GPT-Engineer](https://github.com/AntonOsika/gpt-engineer) is another project to create a whole repository of code given a task specified in natural language. The GPT-Engineer is instructed to think over a list of smaller components to build and ask for user input to clarify questions as needed.

Here are a sample conversation for task clarification sent to OpenAI ChatCompletion endpoint used by GPT-Engineer. The user inputs are wrapped in `{{user input text}}`.

```
[
  {
    "role": "system",
    "content": "You will read instructions and not carry them out, only seek to clarify them.\nSpecifically you will first summarise a list of super short bullets of areas that need clarification.\nThen you will pick one clarifying question, and wait for an answer from the user.\n"
  },
  {
    "role": "user",
    "content": "We are writing {{a Super Mario game in python. MVC components split in separate files. Keyboard control.}}\n"
  },
  {
    "role": "assistant",
    "content": "Summary of areas that need clarification:\n1. Specifics of the Super Mario game (e.g. level design, characters, gameplay mechanics)\n2. Details about the MVC components (e.g. which components are in each file)\n3. Keyboard control implementation (e.g. which keys to use, how to handle input)\n\nClarifying question:\nCan you provide more details about the Super Mario game, such as level design, characters, and gameplay mechanics?"
  },
  {
    "role": "user",
    "content": "{{There are 10 levels in total. The main character is a plumber named Mario, who can walk and jump. It is a classical platform game just like Super Mario. The main character moves from left to right, trying to get to the destination, where there are many obstacles and attacks from enemies in the process.}}\n\nIs anything else unclear? If yes, only answer in the form:\n{remaining unclear areas} remaining questions.\n{Next question}\nIf everything is sufficiently clear, only answer \"Nothing more to clarify.\"."
  },
  {
    "role": "assistant",
    "content": "Remaining unclear areas: 2 remaining questions.\nCan you provide more information about how the MVC components are split into separate files?"
  },
  {
    "role": "user",
    "content": "{{Make your own assumptions and state them explicitly before starting}}"
  }
]
```

Then after these clarification, the agent moved into the code writing mode with a different system message. System message:

You will get instructions for code to write. You will write a very long answer. Make sure that every detail of the architecture is, in the end, implemented as code. Make sure that every detail of the architecture is, in the end, implemented as code.

Think step by step and reason yourself to the right decisions to make sure we get it right. You will first lay out the names of the core classes, functions, methods that will be necessary, as well as a quick comment on their purpose.

Then you will output the content of each file including ALL code. Each file must strictly follow a markdown code block format, where the following tokens must be replaced such that FILENAME is the lowercase file name including the file extension, LANG is the markup code block language for the code’s language, and CODE is the code:

FILENAME

```LANG
CODE
```

You will start with the “entrypoint” file, then go to the ones that are imported by that file, and so on. Please note that the code should be fully functional. No placeholders.

Follow a language and framework appropriate best practice file naming convention. Make sure that files contain all imports, types etc. Make sure that code in different files are compatible with each other. Ensure to implement all code, if you are unsure, write a plausible implementation. Include module dependency or package manager dependency definition file. Before you finish, double check that all parts of the architecture is present in the files.

Useful to know: You almost always put different classes in different files. For Python, you always create an appropriate requirements.txt file. For NodeJS, you always create an appropriate package.json file. You always add a comment briefly describing the purpose of the function definition. You try to add comments explaining very complex bits of logic. You always follow the best practices for the requested languages in terms of describing the code written as a defined package/project.

Python toolbelt preferences:

- pytest
- dataclasses

Conversatin samples:

```
[
  {
    "role": "system",
    "content": "You will get instructions for code to write.\nYou will write a very long answer. Make sure that every detail of the architecture is, in the end, implemented as code.\nMake sure that every detail of the architecture is, in the end, implemented as code.\n\nThink step by step and reason yourself to the right decisions to make sure we get it right.\nYou will first lay out the names of the core classes, functions, methods that will be necessary, as well as a quick comment on their purpose.\n\nThen you will output the content of each file including ALL code.\nEach file must strictly follow a markdown code block format, where the following tokens must be replaced such that\nFILENAME is the lowercase file name including the file extension,\nLANG is the markup code block language for the code's language, and CODE is the code:\n\nFILENAME\n```LANG\nCODE\n```\n\nYou will start with the \"entrypoint\" file, then go to the ones that are imported by that file, and so on.\nPlease note that the code should be fully functional. No placeholders.\n\nFollow a language and framework appropriate best practice file naming convention.\nMake sure that files contain all imports, types etc. Make sure that code in different files are compatible with each other.\nEnsure to implement all code, if you are unsure, write a plausible implementation.\nInclude module dependency or package manager dependency definition file.\nBefore you finish, double check that all parts of the architecture is present in the files.\n\nUseful to know:\nYou almost always put different classes in different files.\nFor Python, you always create an appropriate requirements.txt file.\nFor NodeJS, you always create an appropriate package.json file.\nYou always add a comment briefly describing the purpose of the function definition.\nYou try to add comments explaining very complex bits of logic.\nYou always follow the best practices for the requested languages in terms of describing the code written as a defined\npackage/project.\n\n\nPython toolbelt preferences:\n- pytest\n- dataclasses\n"
  },
 #  … same conversation as earlier, ended with "Make your own assumptions and state them explicitly before starting".
  {
    "role": "assistant",
    "content": "Assumptions:\n1. Model: The model will contain the game's data, such as level information, character states, and enemy positions.\n2. View: The view will handle the game's visuals, including rendering the game objects, backgrounds, and updating the display.\n3. Controller: The controller will manage user input, such as keyboard controls, and update the model accordingly.\n\nWith these assumptions in mind, is there any specific aspect of the keyboard control implementation you would like me to clarify?"
  },
  {
    "role": "user",
    "content": "Please now remember the steps:\n\nThink step by step and reason yourself to the right decisions to make sure we get it right.\nFirst lay out the names of the core classes, functions, methods that will be necessary, As well as a quick comment on their purpose.\n\nThen you will output the content of each file including ALL code.\nEach file must strictly follow a markdown code block format, where the following tokens must be replaced such that\nFILENAME is the lowercase file name including the file extension,\nLANG is the markup code block language for the code's language, and CODE is the code:\n\nFILENAME\n```LANG\nCODE\n```\n\nPlease note that the code should be fully functional. No placeholders.\n\nYou will start with the \"entrypoint\" file, then go to the ones that are imported by that file, and so on.\nFollow a language and framework appropriate best practice file naming convention.\nMake sure that files contain all imports, types etc. The code should be fully functional. Make sure that code in different files are compatible with each other.\nBefore you finish, double check that all parts of the architecture is present in the files.\n"
  }
]
```

# Challenges

After going through key ideas and demos of building LLM-centered agents, I start to see a couple common limitations:

- **Finite context length**: The restricted context capacity limits the inclusion of historical information, detailed instructions, API call context, and responses. The design of the system has to work with this limited communication bandwidth, while mechanisms like self-reflection to learn from past mistakes would benefit a lot from long or infinite context windows. Although vector stores and retrieval can provide access to a larger knowledge pool, their representation power is not as powerful as full attention.
    
- **Challenges in long-term planning and task decomposition**: Planning over a lengthy history and effectively exploring the solution space remain challenging. LLMs struggle to adjust plans when faced with unexpected errors, making them less robust compared to humans who learn from trial and error.
    
- **Reliability of natural language interface**: Current agent system relies on natural language as an interface between LLMs and external components such as memory and tools. However, the reliability of model outputs is questionable, as LLMs may make formatting errors and occasionally exhibit rebellious behavior (e.g. refuse to follow an instruction). Consequently, much of the agent demo code focuses on parsing model output.
    

# Citation

Cited as:

> Weng, Lilian. (Jun 2023). “LLM-powered Autonomous Agents”. Lil’Log. https://lilianweng.github.io/posts/2023-06-23-agent/.

Or

```
@article{weng2023agent,
  title   = "LLM-powered Autonomous Agents",
  author  = "Weng, Lilian",
  journal = "lilianweng.github.io",
  year    = "2023",
  month   = "Jun",
  url     = "https://lilianweng.github.io/posts/2023-06-23-agent/"
}
```

# References

[1] Wei et al. [“Chain of thought prompting elicits reasoning in large language models.”](https://arxiv.org/abs/2201.11903) NeurIPS 2022

[2] Yao et al. [“Tree of Thoughts: Dliberate Problem Solving with Large Language Models.”](https://arxiv.org/abs/2305.10601) arXiv preprint arXiv:2305.10601 (2023).

[3] Liu et al. [“Chain of Hindsight Aligns Language Models with Feedback “](https://arxiv.org/abs/2302.02676) arXiv preprint arXiv:2302.02676 (2023).

[4] Liu et al. [“LLM+P: Empowering Large Language Models with Optimal Planning Proficiency”](https://arxiv.org/abs/2304.11477) arXiv preprint arXiv:2304.11477 (2023).

[5] Yao et al. [“ReAct: Synergizing reasoning and acting in language models.”](https://arxiv.org/abs/2210.03629) ICLR 2023.

[6] Google Blog. [“Announcing ScaNN: Efficient Vector Similarity Search”](https://ai.googleblog.com/2020/07/announcing-scann-efficient-vector.html) July 28, 2020.

[7] [https://chat.openai.com/share/46ff149e-a4c7-4dd7-a800-fc4a642ea389](https://chat.openai.com/share/46ff149e-a4c7-4dd7-a800-fc4a642ea389)

[8] Shinn & Labash. [“Reflexion: an autonomous agent with dynamic memory and self-reflection”](https://arxiv.org/abs/2303.11366) arXiv preprint arXiv:2303.11366 (2023).

[9] Laskin et al. [“In-context Reinforcement Learning with Algorithm Distillation”](https://arxiv.org/abs/2210.14215) ICLR 2023.

[10] Karpas et al. [“MRKL Systems A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning.”](https://arxiv.org/abs/2205.00445) arXiv preprint arXiv:2205.00445 (2022).

[11] Nakano et al. [“Webgpt: Browser-assisted question-answering with human feedback.”](https://arxiv.org/abs/2112.09332) arXiv preprint arXiv:2112.09332 (2021).

[12] Parisi et al. [“TALM: Tool Augmented Language Models”](https://arxiv.org/abs/2205.12255)

[13] Schick et al. [“Toolformer: Language Models Can Teach Themselves to Use Tools.”](https://arxiv.org/abs/2302.04761) arXiv preprint arXiv:2302.04761 (2023).

[14] Weaviate Blog. [Why is Vector Search so fast?](https://weaviate.io/blog/why-is-vector-search-so-fast) Sep 13, 2022.

[15] Li et al. [“API-Bank: A Benchmark for Tool-Augmented LLMs”](https://arxiv.org/abs/2304.08244) arXiv preprint arXiv:2304.08244 (2023).

[16] Shen et al. [“HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in HuggingFace”](https://arxiv.org/abs/2303.17580) arXiv preprint arXiv:2303.17580 (2023).

[17] Bran et al. [“ChemCrow: Augmenting large-language models with chemistry tools.”](https://arxiv.org/abs/2304.05376) arXiv preprint arXiv:2304.05376 (2023).

[18] Boiko et al. [“Emergent autonomous scientific research capabilities of large language models.”](https://arxiv.org/abs/2304.05332) arXiv preprint arXiv:2304.05332 (2023).

[19] Joon Sung Park, et al. [“Generative Agents: Interactive Simulacra of Human Behavior.”](https://arxiv.org/abs/2304.03442) arXiv preprint arXiv:2304.03442 (2023).

[20] AutoGPT. [https://github.com/Significant-Gravitas/Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT)

[21] GPT-Engineer. [https://github.com/AntonOsika/gpt-engineer](https://github.com/AntonOsika/gpt-engineer)


# Building effective agents
We've worked with dozens of teams building LLM agents across industries. Consistently, the most successful implementations use simple, composable patterns rather than complex frameworks.

Over the past year, we've worked with dozens of teams building large language model (LLM) agents across industries. Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns.

In this post, we share what we’ve learned from working with our customers and building agents ourselves, and give practical advice for developers on building effective agents.

## What are agents?

"Agent" can be defined in several ways. Some customers define agents as fully autonomous systems that operate independently over extended periods, using various tools to accomplish complex tasks. Others use the term to describe more prescriptive implementations that follow predefined workflows. At Anthropic, we categorize all these variations as **agentic systems**, but draw an important architectural distinction between **workflows** and **agents**:

- **Workflows** are systems where LLMs and tools are orchestrated through predefined code paths.
- **Agents**, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.

Below, we will explore both types of agentic systems in detail. In Appendix 1 (“Agents in Practice”), we describe two domains where customers have found particular value in using these kinds of systems.

## When (and when not) to use agents

When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all. Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense.

When more complexity is warranted, workflows offer predictability and consistency for well-defined tasks, whereas agents are the better option when flexibility and model-driven decision-making are needed at scale. For many applications, however, optimizing single LLM calls with retrieval and in-context examples is usually enough.

## When and how to use frameworks

There are many frameworks that make agentic systems easier to implement, including:

- The [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview);
- [Strands Agents SDK by AWS](https://strandsagents.com/latest/);
- [Rivet](https://rivet.ironcladapp.com/), a drag and drop GUI LLM workflow builder; and
- [Vellum](https://www.vellum.ai/), another GUI tool for building and testing complex workflows.

These frameworks make it easy to get started by simplifying standard low-level tasks like calling LLMs, defining and parsing tools, and chaining calls together. However, they often create extra layers of abstraction that can obscure the underlying prompts ​​and responses, making them harder to debug. They can also make it tempting to add complexity when a simpler setup would suffice.

We suggest that developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code. If you do use a framework, ensure you understand the underlying code. Incorrect assumptions about what's under the hood are a common source of customer error.

See our [cookbook](https://platform.claude.com/cookbook/patterns-agents-basic-workflows) for some sample implementations.

## Building blocks, workflows, and agents

In this section, we’ll explore the common patterns for agentic systems we’ve seen in production. We'll start with our foundational building block—the augmented LLM—and progressively increase complexity, from simple compositional workflows to autonomous agents.

### Building block: The augmented LLM

The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. Our current models can actively use these capabilities—generating their own search queries, selecting appropriate tools, and determining what information to retain.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2Fd3083d3f40bb2b6f477901cc9a240738d3dd1371-2401x1000.png&w=3840&q=75)

The augmented LLM

We recommend focusing on two key aspects of the implementation: tailoring these capabilities to your specific use case and ensuring they provide an easy, well-documented interface for your LLM. While there are many ways to implement these augmentations, one approach is through our recently released [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol), which allows developers to integrate with a growing ecosystem of third-party tools with a simple [client implementation](https://modelcontextprotocol.io/tutorials/building-a-client#building-mcp-clients).

For the remainder of this post, we'll assume each LLM call has access to these augmented capabilities.

### Workflow: Prompt chaining

Prompt chaining decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one. You can add programmatic checks (see "gate” in the diagram below) on any intermediate steps to ensure that the process is still on track.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F7418719e3dab222dccb379b8879e1dc08ad34c78-2401x1000.png&w=3840&q=75)

The prompt chaining workflow

**When to use this workflow:** This workflow is ideal for situations where the task can be easily and cleanly decomposed into fixed subtasks. The main goal is to trade off latency for higher accuracy, by making each LLM call an easier task.

**Examples where prompt chaining is useful:**

- Generating Marketing copy, then translating it into a different language.
- Writing an outline of a document, checking that the outline meets certain criteria, then writing the document based on the outline.

### Workflow: Routing

Routing classifies an input and directs it to a specialized followup task. This workflow allows for separation of concerns, and building more specialized prompts. Without this workflow, optimizing for one kind of input can hurt performance on other inputs.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F5c0c0e9fe4def0b584c04d37849941da55e5e71c-2401x1000.png&w=3840&q=75)

The routing workflow

**When to use this workflow:** Routing works well for complex tasks where there are distinct categories that are better handled separately, and where classification can be handled accurately, either by an LLM or a more traditional classification model/algorithm.

**Examples where routing is useful:**

- Directing different types of customer service queries (general questions, refund requests, technical support) into different downstream processes, prompts, and tools.
- Routing easy/common questions to smaller, cost-efficient models like Claude Haiku 4.5 and hard/unusual questions to more capable models like Claude Sonnet 4.5 to optimize for best performance.

### Workflow: Parallelization

LLMs can sometimes work simultaneously on a task and have their outputs aggregated programmatically. This workflow, parallelization, manifests in two key variations:

- **Sectioning**: Breaking a task into independent subtasks run in parallel.
- **Voting:** Running the same task multiple times to get diverse outputs.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F406bb032ca007fd1624f261af717d70e6ca86286-2401x1000.png&w=3840&q=75)

The parallelization workflow

**When to use this workflow:** Parallelization is effective when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher confidence results. For complex tasks with multiple considerations, LLMs generally perform better when each consideration is handled by a separate LLM call, allowing focused attention on each specific aspect.

**Examples where parallelization is useful:**

- **Sectioning**:
    - Implementing guardrails where one model instance processes user queries while another screens them for inappropriate content or requests. This tends to perform better than having the same LLM call handle both guardrails and the core response.
    - Automating evals for evaluating LLM performance, where each LLM call evaluates a different aspect of the model’s performance on a given prompt.
- **Voting**:
    - Reviewing a piece of code for vulnerabilities, where several different prompts review and flag the code if they find a problem.
    - Evaluating whether a given piece of content is inappropriate, with multiple prompts evaluating different aspects or requiring different vote thresholds to balance false positives and negatives.

### Workflow: Orchestrator-workers

In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F8985fc683fae4780fb34eab1365ab78c7e51bc8e-2401x1000.png&w=3840&q=75)

The orchestrator-workers workflow

**When to use this workflow:** This workflow is well-suited for complex tasks where you can’t predict the subtasks needed (in coding, for example, the number of files that need to be changed and the nature of the change in each file likely depend on the task). Whereas it’s topographically similar, the key difference from parallelization is its flexibility—subtasks aren't pre-defined, but determined by the orchestrator based on the specific input.

**Example where orchestrator-workers is useful:**

- Coding products that make complex changes to multiple files each time.
- Search tasks that involve gathering and analyzing information from multiple sources for possible relevant information.

### Workflow: Evaluator-optimizer

In the evaluator-optimizer workflow, one LLM call generates a response while another provides evaluation and feedback in a loop.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F14f51e6406ccb29e695da48b17017e899a6119c7-2401x1000.png&w=3840&q=75)

The evaluator-optimizer workflow

**When to use this workflow:** This workflow is particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value. The two signs of good fit are, first, that LLM responses can be demonstrably improved when a human articulates their feedback; and second, that the LLM can provide such feedback. This is analogous to the iterative writing process a human writer might go through when producing a polished document.

**Examples where evaluator-optimizer is useful:**

- Literary translation where there are nuances that the translator LLM might not capture initially, but where an evaluator LLM can provide useful critiques.
- Complex search tasks that require multiple rounds of searching and analysis to gather comprehensive information, where the evaluator decides whether further searches are warranted.

### Agents

Agents are emerging in production as LLMs mature in key capabilities—understanding complex inputs, engaging in reasoning and planning, using tools reliably, and recovering from errors. Agents begin their work with either a command from, or interactive discussion with, the human user. Once the task is clear, agents plan and operate independently, potentially returning to the human for further information or judgement. During execution, it's crucial for the agents to gain “ground truth” from the environment at each step (such as tool call results or code execution) to assess its progress. Agents can then pause for human feedback at checkpoints or when encountering blockers. The task often terminates upon completion, but it’s also common to include stopping conditions (such as a maximum number of iterations) to maintain control.

Agents can handle sophisticated tasks, but their implementation is often straightforward. They are typically just LLMs using tools based on environmental feedback in a loop. It is therefore crucial to design toolsets and their documentation clearly and thoughtfully. We expand on best practices for tool development in Appendix 2 ("Prompt Engineering your Tools").

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F58d9f10c985c4eb5d53798dea315f7bb5ab6249e-2401x1000.png&w=3840&q=75)

Autonomous agent

**When to use agents:** Agents can be used for open-ended problems where it’s difficult or impossible to predict the required number of steps, and where you can’t hardcode a fixed path. The LLM will potentially operate for many turns, and you must have some level of trust in its decision-making. Agents' autonomy makes them ideal for scaling tasks in trusted environments.

The autonomous nature of agents means higher costs, and the potential for compounding errors. We recommend extensive testing in sandboxed environments, along with the appropriate guardrails.

**Examples where agents are useful:**

The following examples are from our own implementations:

- A coding Agent to resolve [SWE-bench tasks](https://www.anthropic.com/research/swe-bench-sonnet), which involve edits to many files based on a task description;
- Our [“computer use” reference implementation](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo), where Claude uses a computer to accomplish tasks.

![](https://www.anthropic.com/_next/image?url=https%3A%2F%2Fwww-cdn.anthropic.com%2Fimages%2F4zrzovbb%2Fwebsite%2F4b9a1f4eb63d5962a6e1746ac26bbc857cf3474f-2400x1666.png&w=3840&q=75)

High-level flow of a coding agent

## Combining and customizing these patterns

These building blocks aren't prescriptive. They're common patterns that developers can shape and combine to fit different use cases. The key to success, as with any LLM features, is measuring performance and iterating on implementations. To repeat: you should consider adding complexity _only_ when it demonstrably improves outcomes.

## Summary

Success in the LLM space isn't about building the most sophisticated system. It's about building the _right_ system for your needs. Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short.

When implementing agents, we try to follow three core principles:

1. Maintain **simplicity** in your agent's design.
2. Prioritize **transparency** by explicitly showing the agent’s planning steps.
3. Carefully craft your agent-computer interface (ACI) through thorough tool **documentation and testing**.

Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components as you move to production. By following these principles, you can create agents that are not only powerful but also reliable, maintainable, and trusted by their users.

### Acknowledgements

Written by Erik Schluntz and Barry Zhang. This work draws upon our experiences building agents at Anthropic and the valuable insights shared by our customers, for which we're deeply grateful.

## Appendix 1: Agents in practice

Our work with customers has revealed two particularly promising applications for AI agents that demonstrate the practical value of the patterns discussed above. Both applications illustrate how agents add the most value for tasks that require both conversation and action, have clear success criteria, enable feedback loops, and integrate meaningful human oversight.

### A. Customer support

Customer support combines familiar chatbot interfaces with enhanced capabilities through tool integration. This is a natural fit for more open-ended agents because:

- Support interactions naturally follow a conversation flow while requiring access to external information and actions;
- Tools can be integrated to pull customer data, order history, and knowledge base articles;
- Actions such as issuing refunds or updating tickets can be handled programmatically; and
- Success can be clearly measured through user-defined resolutions.

Several companies have demonstrated the viability of this approach through usage-based pricing models that charge only for successful resolutions, showing confidence in their agents' effectiveness.

### B. Coding agents

The software development space has shown remarkable potential for LLM features, with capabilities evolving from code completion to autonomous problem-solving. Agents are particularly effective because:

- Code solutions are verifiable through automated tests;
- Agents can iterate on solutions using test results as feedback;
- The problem space is well-defined and structured; and
- Output quality can be measured objectively.

In our own implementation, agents can now solve real GitHub issues in the [SWE-bench Verified](https://www.anthropic.com/research/swe-bench-sonnet) benchmark based on the pull request description alone. However, whereas automated testing helps verify functionality, human review remains crucial for ensuring solutions align with broader system requirements.

## Appendix 2: Prompt engineering your tools

No matter which agentic system you're building, tools will likely be an important part of your agent. [Tools](https://www.anthropic.com/news/tool-use-ga) enable Claude to interact with external services and APIs by specifying their exact structure and definition in our API. When Claude responds, it will include a [tool use block](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#example-api-response-with-a-tool-use-content-block) in the API response if it plans to invoke a tool. Tool definitions and specifications should be given just as much prompt engineering attention as your overall prompts. In this brief appendix, we describe how to prompt engineer your tools.

There are often several ways to specify the same action. For instance, you can specify a file edit by writing a diff, or by rewriting the entire file. For structured output, you can return code inside markdown or inside JSON. In software engineering, differences like these are cosmetic and can be converted losslessly from one to the other. However, some formats are much more difficult for an LLM to write than others. Writing a diff requires knowing how many lines are changing in the chunk header before the new code is written. Writing code inside JSON (compared to markdown) requires extra escaping of newlines and quotes.

Our suggestions for deciding on tool formats are the following:

- Give the model enough tokens to "think" before it writes itself into a corner.
- Keep the format close to what the model has seen naturally occurring in text on the internet.
- Make sure there's no formatting "overhead" such as having to keep an accurate count of thousands of lines of code, or string-escaping any code it writes.

One rule of thumb is to think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good _agent_-computer interfaces (ACI). Here are some thoughts on how to do so:

- Put yourself in the model's shoes. Is it obvious how to use this tool, based on the description and parameters, or would you need to think carefully about it? If so, then it’s probably also true for the model. A good tool definition often includes example usage, edge cases, input format requirements, and clear boundaries from other tools.
- How can you change parameter names or descriptions to make things more obvious? Think of this as writing a great docstring for a junior developer on your team. This is especially important when using many similar tools.
- Test how the model uses your tools: Run many example inputs in our [workbench](https://console.anthropic.com/workbench) to see what mistakes the model makes, and iterate.
- [Poka-yoke](https://en.wikipedia.org/wiki/Poka-yoke) your tools. Change the arguments so that it is harder to make mistakes.

While building our agent for [SWE-bench](https://www.anthropic.com/research/swe-bench-sonnet), we actually spent more time optimizing our tools than the overall prompt. For example, we found that the model would make mistakes with tools using relative filepaths after the agent had moved out of the root directory. To fix this, we changed the tool to always require absolute filepaths—and we found that the model used this method flawlessly.

# 使用 LangGraph 与 LangChain 构建多工具有状态智能体

草稿

> 智能体开发进入“有状态”时代，LangGraph 让多工具智能体既可控又灵活，助你打造真正工程级 AI 系统。

本文将指导高级 AI 工程开发者，如何基于 **LangChain** 的扩展库 **LangGraph**，使用 Python 构建一个具备多工具调用能力的**有状态智能体（Multi-Tool Agent）**。我们将详述如何设计有状态的智能体工作流（如检索 - 计划 - 执行 - 验证等阶段），如何在智能体中注册和选择不同工具、处理记忆模块，以及如何实现并发、分支和回退控制流程。教程还将涵盖观察调试智能体的方法（日志追踪、链路 Trace、决策记录），以及如何进行错误注入与回放来提高智能体的健壮性。最后，我们提供一个端到端示例任务（包含所有可运行的代码片段），并通过 Mermaid 图表直观展示智能体的决策流程与工具链路。请注意，本教程所有代码均采用 Python，实现均兼容本地部署的大语言模型（如 Qwen 或 Ollama），未依赖 OpenAI/Claude 等闭源模型。

## LangGraph 简介：让智能体工作流进入“有状态”时代

**LangGraph** 是由 LangChain 团队推出的用于构建**循环图工作流**的库，可以视作 LangChain 在智能体编排上的一个重要扩展模块。传统的 LangChain Chain 是**无环的**（DAG 形式），而 LangGraph 允许在链中**引入循环**，从而实现更复杂的智能体行为（例如让 LLM 在工具调用失败时重新规划、在多轮对话中持续决策等）。这种循环能力本质上就是让 LLM 在一个类似 `for` 循环的结构中不断根据状态进行推理和行动选择。

LangGraph 将智能体的流程视为**状态机（state machine）**。开发者可以手动规定智能体的决策流程（如先调用哪个工具、在什么条件下循环/分支），而不仅仅依赖 LLM 的自由推理。这种显式的流程控制对于生产环境尤为重要：例如你可能希望**强制智能体首先调用某个工具**，或者根据当前状态采用不同的提示 (prompt)。通过 LangGraph，我们可以将这些流程以**图（graph）**的形式声明出来，构建出兼具**灵活推理**和**可控流程**的智能体系统。

**StateGraph** 是 LangGraph 的核心概念，它表示一个状态驱动的图。StateGraph 有一个全局共享的**状态对象（state）**，在图的各节点之间传递和更新。节点可以看作对状态的一个操作：每个节点接收当前状态（通常是一个字典）作为输入，执行计算后输出一个字典，用于更新全局状态的一部分。状态的每个字段可以配置为**覆盖**更新或**累加**更新。当字段设置为累加（例如一个用于记录行动步骤的列表），多个节点循环更新时会自动将新结果附加在列表后面。

使用 LangGraph 定义智能体的基本步骤包括：

- **定义状态结构**：使用 `TypedDict` 指定 State 对象的字段和类型，以及哪些字段是累加 List 需要用 `operator.add` 标记。
- **添加节点**：使用 `graph.add_node(name, func)` 注册节点。每个节点要么是一个 Python 函数，要么是 LangChain Runnable，负责完成一个步骤的逻辑。
- **添加边（Edges）**：用 `graph.set_entry_point(node)` 指定图的起始节点，然后通过 `graph.add_edge` 添加普通顺序边，或通过 `graph.add_conditional_edge` 添加条件分支边。条件边可以让某个节点根据状态判断下一步跳转到哪一个节点。
- **指定结束**：LangGraph 提供特殊的 `END` 节点表示结束，务必保证循环流程有退出条件。
- **编译运行**：调用 `graph.compile()` 将定义的图编译为一个可调用的对象（实现了 `.invoke()` 等方法），然后即可像调用链那样调用智能体。

下面将结合这些概念，设计我们的有状态多工具 Agent，并在各环节介绍实现细节。

## 设计有状态智能体的阶段编排与控制流程

为了构建一个多工具 Agent，我们采用**分阶段的流程设计**：例如包含“需求分析/检索 → 计划 → 工具执行 → 验证”的流水线。在 LangGraph 中，这些阶段对应为一系列节点按某种逻辑连接成图。我们将用一个示意性任务来说明——**根据用户查询决定是否需要检索外部数据、调用计算工具，并最终生成答案**。这个任务中，Agent 可能需要经过以下决策步骤：

1. **分析需求（Plan）**：解析用户输入，判断是否需要调用工具（以及调用哪些工具）。如果不需要工具，直接生成答案；如果需要，决定下一步要用的工具及其输入。
2. **执行工具（Execute Tool）**：调用所选工具并获取结果。如果有多个子任务，可能重复调用不同工具。
3. **（可选）验证或后处理（Verify）**：检查工具结果是否满足要求，是否需要再次调用其他工具或调整计划。如果结果不理想，可以回退到上一步重新规划。
4. **最终回答（Finalize）**：整合所有信息，形成给用户的最终答复。

在我们的示例中，我们将实现一个智能体能够**查询国家的人口并计算总和**。这个智能体会动态决定使用两个工具：

- 一个**检索工具**：查找给定国家的人口数据。
- 一个**计算工具**：对获得的数值执行算术计算。

我们会让智能体针对用户的问题自动决定调用上述工具的顺序和次数。例如用户问：“法国和日本的人口总和是多少？”，Agent 将判断需要查找法国人口、查找日本人口，然后加总。这一过程中，Agent 会经历**循环**：LLM 先规划调用检索工具，获取法国人口；接着再次规划调用检索工具获取日本人口；然后规划调用计算工具求和；最后生成答案。

### 节点设计：Plan 与 Tools

我们为上述流程设计两个主要节点：

- **Plan 节点**（如同智能体的“大脑”）：使用 LLM 或规则逻辑，根据当前状态决定下一步动作（调用工具或输出答案）。该节点会更新状态中的指令，例如选定工具及其输入参数，或者直接写入最终答案。
- **Tools 节点**（工具执行器）：根据 Plan 节点提供的指令，实际调用相应的工具函数，将结果写回状态（供下次 Plan 决策使用）。

此外，可以视需要添加其他节点，例如用于验证或回退的节点。本例中我们简化，将验证逻辑融合在 Plan 节点里，根据需要重复工具调用或结束。

### 状态设计：共享信息和累积中间结果

我们通过定义 State 对象的字段来实现节点间的信息共享和状态跟踪。对于本示例，我们定义状态包含：

- `input`：用户的原始查询（字符串）。
- `targets`：待查询的信息目标列表（如[“France”,“Japan”]）。在 Plan 节点首次运行时，从`input`中解析填充。
- `index`：当前已处理的目标计数（整数）。用于跟踪已完成了几个工具调用。
- `collected`：已收集的中间结果列表（如已获取的人口数字列表）。定义为累加列表，这样工具节点每返回一个结果就附加其值。
- `answer`：最终答案（字符串）。Plan 节点在确定完成所有步骤后写入此字段。

上述字段中，`collected` 使用了 `operator.add` 设置为累加模式，其他字段则用默认覆盖模式。这样`collected`会自动累计工具输出，而不是被覆盖。定义状态的代码如下：

```python
from typing import TypedDict, Annotated, List
import operator

class State(TypedDict):
    input: str                        # 用户输入
    targets: List[str]                # 待检索的目标列表
    collected: Annotated[List[int], operator.add]  # 累计收集的数值结果
    index: int                        # 已处理目标计数
    answer: str                       # 最终答案
```

### Plan 节点实现：LLM 计划与决策

Plan 节点的职责是分析当前状态，决定下一步做什么。这里我们可以**借助大语言模型**根据提示来决定行动，也可以简化为规则逻辑。在不依赖 OpenAI API 的前提下，我们示范一种**规则+LLM 结合**的思路：

- **需求解析**：当 Plan 节点第一次接收用户输入时，可通过简单规则或提示调用 LLM，从中提取需要查询的目标。例如检测输入中是否包含“…的**人口**”，如果有则识别国家名称列表。如果没有外部信息需求，则可以直接回答。
- **动态决策**：根据当前已收集的数据 (`collected`) 与目标列表 (`targets`)，决定下一步。如果还有未查询的目标，则设置下一步调用检索工具查询下一个目标；如果目标都已查询完且有多个数值，需要汇总，则选择计算工具；如果已经获得最终结果或不需要工具，则直接产生日志和答案。

下面是 Plan 节点函数的示例实现（不依赖外部 LLM API，而是用规则逻辑模拟决策）：

```python
def plan_node_fn(state: dict) -> dict:
    # 提取当前状态信息
    query = state.get('input', '')
    targets = state.get('targets')
    idx = state.get('index', 0)
    values = state.get('collected', [])
    # 若已经计算出最终结果（collected 比 targets 多一个值，则最后一个为汇总结果）
    if targets is not None and len(values) > len(targets):
        final_val = values[-1]
        return {'answer': f"总人口为 {final_val} 万人。"}
    # 首次运行：解析输入找出目标列表
    if targets is None:
        targets = []
        # 简单解析：寻找 "人口 of X" 模式
        text = query.lower()
        if "population of" in text:
            parts = text.split("population of")
            for part in parts[1:]:
                token = part.strip().split()[0]
                if token:
                    targets.append(token.capitalize())
        # 处理 "X and Y" 的情况
        if " and " in query and targets:
            last = query.split(" and ")[-1].strip()
            if last:
                country = last.split()[0].capitalize()
                if country and country not in targets:
                    targets.append(country)
        # 初始化状态字段
        state['targets'] = targets
        state['index'] = 0
        state['collected'] = []
        idx = 0
        values = []
    # 如未找到任何目标，则不需要工具，直接给出回答（这里简单返回一句话）
    if not targets:
        return {'answer': "这个问题不需要调用工具，可直接回答。"}
    # 如果仍有目标未查询，选择调用检索工具查询下一个目标
    if idx < len(targets):
        country = targets[idx]
        return {'tool': 'search_population', 'tool_query': country}
    # 如果所有目标都已查询且存在多个数值，调用计算工具求和
    if idx == len(targets) and len(values) > 1:
        expr = " + ".join(str(val) for val in values)
        return {'tool': 'calculator', 'tool_query': expr}
    # 如果所有目标查询完且只有单个值，则直接输出答案
    if idx == len(targets):
        if values:
            return {'answer': f"{targets[0]}的人口为 {values[0]} 万人。"}
        else:
            return {'answer': "未找到相关数据。"}
    # 默认返回空（正常情况下不会走到这里）
    return {}
```

**实现要点**：

- 初次运行时，`targets` 为空，我们解析用户输入中的关键词填充目标列表（如找到“France”“Japan”两国），并将它们存入状态。这个解析过程可以用 LangChain 的提示模板结合 LLM 完成，如让模型从问句中提取实体列表；但这里为简明直接用字符串分析。
- 每次决策，根据 `index` 和 `targets` 列表判断进度：若`index`尚未到达`targets`末尾，则还有国家未查询，于是返回指示调用`search_population`工具（并指定查询国家名）；若已收集多个数值，则需要求和，于是返回调用`calculator`工具的指令；若只收集了一个值且无进一步操作，则直接准备输出答案。
- 当检测到状态中 `collected` 数量比 `targets`数多时，说明上一步计算工具已经算出了最终汇总结果，我们便直接构造最终回答放入`answer`字段。

### Tools 节点实现：多工具执行与结果写回

Tools 节点负责根据 Plan 给出的指令实际调用工具函数，并把结果更新到状态中。首先需要**注册工具**：在 LangChain 中通常将工具封装为 Tool 对象，但在此我们直接用普通的 Python 函数模拟工具功能：

- `search_population(country: str)`：检索某国家人口。本例中我们用预设的字典模拟数据库。例如 `population_data = {"France": 67, "Japan": 125}` 表示法国人口 67 百万人、日本 125 百万人。函数返回找到的人口数字（为了简化计算，我们返回整数部分）。
- `calculator(expression: str)`：计算算术表达式结果。可以用 Python 的 `eval` 来处理简单加法表达式（但实际场景应谨慎处理安全）。本例中，我们传入的表达式格式如 `"67 + 125"`，计算后得到整数结果 `192`。

工具执行函数完成后，要将结果写入状态。根据之前状态设计，我们希望：

- 检索工具得到的人口数字追加到 `collected` 列表，并将 `index` 递增 1（表示一个目标已完成）。
- 计算工具得到的总和结果也追加到 `collected` 列表。此时列表将比原目标数多一个元素，方便 Plan 节点识别已经完成汇总。

下面是 Tools 节点的示例实现：

```python
# 模拟数据库
population_data = {"France": 67, "Japan": 125}

def tool_node_fn(state: dict) -> dict:
    tool_name = state.get('tool')
    query = state.get('tool_query')
    if tool_name == 'search_population':
        country = query
        if country in population_data:
            result = population_data[country]
            # 将结果追加到 collected 列表（LangGraph 累加机制会自动 append）
            return {'collected': [result], 'index': state.get('index', 0) + 1}
        else:
            # 没找到数据，返回错误信息
            return {'error': f"未找到{country}的人口数据"}
    elif tool_name == 'calculator':
        expr = query  # 形如 "67 + 125"
        try:
            calc_result = eval(expr)
        except Exception as e:
            return {'error': f"计算出错：{e}"}
        # 将计算结果也加入 collected
        return {'collected': [int(calc_result)]}
    else:
        return {'error': f"未知工具:{tool_name}"}
```

**实现要点**：

- 根据状态中的 `tool` 字段分发到对应的工具逻辑。
- 每个工具通过返回字典来更新状态。对于 `collected` 字段，由于我们在 State 定义中标记了 `operator.add`，LangGraph 会自动将新列表元素添加到已有列表后面。
- `search_population` 成功时还返回更新后的 `index`（旧值 +1）。`calculator` 完成汇总后不增 index，因为此时 `index`已经等于目标数，汇总结果只是附加信息。
- 如果出现错误（如没有找到数据，或表达式计算异常），这里简单地将错误信息写入状态的 `error` 字段。后续我们可以通过检测 `error` 实现异常分支处理。

### 构建状态图（StateGraph）并添加控制边

有了 Plan 和 Tools 两个节点函数，我们就可以把它们加入 StateGraph 并连成工作流：

```python
from langgraph.graph import StateGraph, END

# 初始化状态图
graph = StateGraph(State)
# 添加节点
graph.add_node("plan", plan_node_fn)
graph.add_node("tools", tool_node_fn)
# 指定入口节点
graph.set_entry_point("plan")
# 添加普通边：工具节点执行后回到计划节点（形成循环）
graph.add_edge("tools", "plan")
# 添加条件边：plan 节点根据返回结果决定下一步去向
def should_continue(state: dict) -> str:
    # 若 Plan 返回了最终答案，则结束，否则进入工具执行
    return "end" if state.get('answer') else "continue"

graph.add_conditional_edge(
    "plan",
    should_continue,
    {
        "end": END,
        "continue": "tools"
    }
)
# 编译图为可调用应用
app = graph.compile()
```

在上述代码中，我们建立了如下流程关系：

![图 1: 流程关系图](https://assets.jimmysong.io/images/book/ai-handbook/agent/langgraph/97d78accfdabc34849c0950014d4df98.svg)

图 1: 流程关系图

如上图所示，Agent 从 Plan 节点开始：Plan 节点要么决定直接结束（生成最后回答），要么指定需要调用某个工具然后进入 Tools 节点。Tools 节点执行完，再回到 Plan 重新决策。这个循环会持续，直到 Plan 给出结束条件（即 state 中出现 `answer`）跳转到 End 节点。在我们的示例中，循环可能经历多次工具调用（如两次检索，一次计算）再结束。

### 并发执行与分支：高级控制流

LangGraph 除了支持上述顺序循环，还支持更复杂的**并发和分支**控制流。通过一个节点连接出**多个后继节点**即可形成**分叉**（fan-out），LangGraph 可并行执行这些分支节点，然后在某处**汇合**（fan-in）它们的结果。例如，我们可以改进前述 Agent，让它**并行地查询多个国家的人口**以加速流程。当 Plan 节点识别出多个目标时，不是依次一个个调用检索工具，而是同时分叉出多个检索节点，然后汇总结果再进行计算。下图展示了这种并行分支结构的雏形：

![图 2: 高级控制流](https://assets.jimmysong.io/images/book/ai-handbook/agent/langgraph/df0097d411a808b6dd306290d7f848ba.svg)

图 2: 高级控制流

在 LangGraph 实现并行，可以为一个节点添加**多条普通边**指向不同后继节点，如：`graph.add_edge("plan", "searchA"); graph.add_edge("plan", "searchB")`。当 Plan 节点执行后，LangGraph 将在同一轮中并发执行`searchA`和`searchB`两个节点，并分别更新状态。为正确汇总并行结果，需在状态定义中为共享字段设置**自定义合并函数**。例如让两个检索节点各自返回一个结果列表，然后在汇合节点前通过 reducer 函数合并它们。LangGraph 允许我们在 State 定义时提供自定义 `reducer` 来合并并行分支的输出。完成 fan-in 后，再继续后续节点（如计算和输出）。需要注意，并行工具调用会增加实现复杂度，如处理结果顺序和可能的异步 I/O 等，在实际应用中应根据需要权衡使用。

除了并行，LangGraph 也支持**条件分支**：通过 `add_conditional_edge` 可以让某节点根据状态选择不同分支路径（如不同工具、不同应对策略）。这类条件可以由 LLM 决定，也可以由规则函数决定。例如，我们可以在智能体某步引入**验证节点**：检查先前答案是否符合要求，如果不符合则走分支调用其它工具重试，符合则直接结束。这相当于实现了一种**回退/回放机制**。总之，通过组合**循环、并行、条件**三种边类型，LangGraph 能表达几乎任意复杂的智能体流程。

## 多工具调用机制

有状态智能体的优势在于可以灵活地选择并调用多个工具。接下来，我们讨论如何管理**多工具的注册与调度**，并确保每次工具调用的输入输出正确、错误可控。

### 工具注册与封装

在 LangChain 框架中，工具通常被封装为 `Tool` 对象，包含名称、描述和实际执行函数。但在 LangGraph 中，我们无需特别封装，直接在 Tools 节点里按照 `state['tool']` 判定来调用相应函数即可（如上所示）。当然，在更复杂情况下，可以维护一个**工具字典**或使用 LangChain 提供的工具集合：

```python
# 使用 LangChain 的 Tool 封装（可选）
from langchain.agents import Tool

search_tool = Tool(
    name="search_population",
    func=lambda country: population_data.get(country, "Not found"),
    description="检索指定国家的人口，返回数字"
)
calc_tool = Tool(
    name="calculator",
    func=lambda expr: eval(expr),
    description="计算简单算术表达式的结果"
)
tools = [search_tool, calc_tool]
```

LangChain 中智能体调用工具通常有两种方式：**动态**和**静态**。**动态工具选择**指由 LLM 自主决定何时用哪个工具（典型案例如 ReAct Agent，让模型输出“Action: 工具名”），如我们设计的 Plan 节点即属于动态决策。**静态工具顺序**则指我们在流程中**固定某些工具调用步骤**，不论 LLM 内容如何都执行。例如可以规定“用户请求进入后，Agent **总是先调用检索工具**然后才回答”，这种需求可以通过 LangGraph 强制一个边顺序来实现。开发者应根据业务需要选择策略：动态方式灵活但不易预料，静态顺序可控但不够高效。也可以二者结合：例如**第一步静态地调用工具获取背景信息**，后续再动态决策其它工具。

### 工具输入的验证与格式规范

在多工具场景下，**输入格式**和**有效性**至关重要。LLM 产生的工具调用指令可能有格式错误或不符合预期。为防止这类问题，可以采取以下措施：

- **规范提示**：通过提示模板严格规范 LLM 输出动作的格式（如“工具名：参数”格式），或者使用**函数式调用**能力（Function Calling），让模型输出可解析的 JSON。不过本例未使用 OpenAI 模型，函数调用可由类似机制实现或自行解析模型文本。
- **输入校验**：在 Tools 节点执行前，对 `state['tool_query']` 进行检查。例如我们的计算工具可先验证表达式只包含安全字符，再用 `eval` 执行；检索工具可检查国家名是否在数据库里，否则提前标记错误。
- **fallback 默认值**：如果输入不合法，工具可以返回特定的错误结果，让智能体识别并处理。比如我们在 Tools 节点返回了 `{'error': '...信息'}` 来提示上层。

在 Plan 节点或独立的验证节点中，可检测 `state` 是否含有 `'error'` 字段，从而决定走错误处理流程（例如忽略该工具结果、向用户反馈无法完成等）。通过这种方式，即使 LLM 选择了无效的工具或参数，我们的系统也能平稳处理而不会崩溃。

### 错误处理与重试机制

完善的智能体应当在工具失败时具备**重试或回退**能力。例如，如果调用 API 出现网络错误，可以等待片刻再次调用；如果连续多次失败，则记录错误并结束，避免死循环。利用 LangGraph 的状态和图结构，我们可以：

- 在 Tools 节点里捕获异常，将错误信息写入状态，如 `state['error']`。然后通过一个**条件边**，如果检测到 `error` 字段则跳转到一个专门的**错误处理节点**，否则正常流程。
- 错误处理节点可以根据错误类型选择策略：有些错误可尝试修正参数后重试（例如搜索不到结果时，Agent 可以改变搜索关键词再调用一次）；有些错误则直接终止流程输出抱歉信息。
- LangGraph 的**持久化**(Persistence) 特性还能使智能体在崩溃或中断后**恢复**。StateGraph 可以配合一个**检查点（Checkpointer）**一同编译，自动在每步保存状态。一旦进程故障或异常退出，再次启动时可从上次的检查点继续。这对于长时间运行的循环智能体尤为有用。

总而言之，通过状态中的错误标记与 LangGraph 的条件跳转，我们能够实现**错误注入与回放**测试。例如，我们可以**人为在工具中注入错误**（返回错误码），观察智能体是否按预期走到错误分支并执行了重试或安全退出逻辑。这种测试可以提高智能体应对异常情况的稳健性。

## 记忆模块与状态传递

默认情况下，上述 LangGraph 智能体每次调用都是**无记忆**的，即不保留先前对话或操作的上下文。在多轮对话或需要长期引用资料的场景，我们需要为智能体增加**记忆模块**。记忆可以分为**短期记忆**和**长期记忆**两种：

- **短期记忆**（会话记忆）：保存最近若干对话轮次内容，确保智能体能够理解上下文追问。实现方式包括 LangChain 的 `ConversationBufferMemory`（缓冲全部对话）或 `ConversationBufferWindowMemory`（仅保留最近 N 条）。在 LangGraph 中，短期记忆可通过 **State** 实现：例如在状态里加入 `chat_history` 字段（类型为 `list[BaseMessage]`，并用 `operator.add` 累加）。每次用户/AI 消息都追加到该列表。LangGraph 还提供 `MemorySaver` 等 checkpointer 工具，能够在多次 `invoke` 调用间自动**持久化对话记录**。使用时，只需在编译时传入参数 `checkpointer=MemorySaver()`，并为每次对话提供一个 `thread_id` 标识会话，LangGraph 会将状态与该 ID 关联存储。如下示例：

```python
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
app = graph.compile(checkpointer=memory)
# 调用时指定线程 ID，以区分不同会话
result = app.invoke({"input": user_input}, metadata={"thread_id": "session_123"})
```

如此，连续多次调用 `app.invoke`，内部会沿用同一个 `chat_history`。短期记忆一般存储在内存中，不跨进程。

- **长期记忆**：针对长周期或跨会话的信息存储，例如把用户提供的事实、Agent 总结的知识存在外部数据库（向量库或 Key-Value 存储）中，以便后续检索。LangChain 提供了多种向量库接口（如 FAISS, Milvus 等）和 `VectorStoreRetrieverMemory` 来实现语义记忆。LangGraph 自身也提供 `InMemoryStore` 等简单存储，可将记忆按 `namespace` 分类保存并搜索。在实践中，可以将长期记忆看作另一种**工具**：当智能体需要回忆时，就通过一个“Memory 检索工具”查询外部记忆库，将相关信息并入上下文。例如，我们可以在 Plan 节点判断如果用户问了以前提过的人物细节，则调用 Memory 工具检索过往对话资料。

无论短期还是长期记忆，核心是在**状态**中传递上下文信息给 LLM。对于本例简单的计算 Agent，记忆意义不大，我们就不实现实际记忆功能。但在更复杂的对话智能体中，别忘了在状态里维护 `chat_history`，并在 Plan 节点（LLM 调用）构造 prompt 时包含历史对话。良好的记忆管理可以防止上下文丢失和重复询问，提高用户体验。

## 可观测性与调试：日志、追踪与决策记录

构建复杂智能体时，**可观测性**是确保系统行为可理解和可调试的关键。LangChain 与 LangGraph 提供了一些工具来记录智能体的内部决策过程：

- **日志追踪**：可以使用 Python 的 logging 模块或简单的 print，将每个节点的输入输出、LLM 的决定、工具的结果打印出来。比如在 Plan 节点函数中打印 `state['input']`及决策，在 Tools 节点打印调用了哪个工具以及得到的结果。这样在终端就能实时看到智能体的执行轨迹。LangChain 也支持设置 `verbose=True` 来输出内部信息，不过对高度自定义的 LangGraph 流程，这种通用 verbose 可能不足，应结合自定义日志。
    
- **链路 Trace**：LangChain 推出了 LangSmith 平台用于链路追踪，可视化每步调用及消耗。但我们也可以不用外部服务，通过 LangGraph 自带的 `.stream()` 接口实现简单追踪。`app.stream(input, stream_mode="values")` 会返回一个迭代器，逐步 yield 每个节点执行的输出值。例如：
    
    ```python
    stream = app.stream({"input": query}, stream_mode="values")
    for step in stream:
        print("Step output:", step)
    ```
    
    这可以逐步获取 Plan 节点和 Tools 节点各自的输出字典，有助于了解每轮循环中文本生成和工具调用的顺序。如果将 `stream_mode` 设置为 `"trace"`（假设有该模式），可能会包含更多元数据。**注意**：流式输出在智能体场景下尤其适用，可以让最终答案逐字生成，同时还能监测中间动作。
    
- **决策记录**：建议在状态中加入一个字段（如 `intermediate_steps` 或 `action_log`），将每次 LLM 的动作决定和工具返回结果记录下来。事实上，LangChain 标准智能体通过 `intermediate_steps` 列表保存 `(AgentAction, Observation)` 对。在我们示例中，我们用 `collected` 列表存了中间数字，但未存文本说明。在真实场景，可以把工具名称和返回摘要也记录，例如 `intermediate_steps: Annotated[List[str], operator.add]` 然后每次工具执行返回 `{"intermediate_steps": [f"Action: 搜索{country}, Result: {result}"]}`。这样最终状态中就保留了整个决策链路，便于日志分析或回答时引用。如果需要让最终答案也附带这些依据，可以让 LLM 参考该记录或在输出阶段直接打印它们。
    

通过上述方法，我们可以调试每一步决策是否合理。例如，当智能体出现了错误行为，可以通过查看日志和决策记录，找出是哪一步的 LLM 判断失误或者工具输出异常。然后有针对性地调整提示、约束或代码逻辑。

## 错误注入与回放测试

为了确保智能体在各种异常情况下表现稳定，我们应进行**错误注入测试**。这通常包括：

- **模拟工具失败**：手动让某个工具函数在特定输入时抛出异常或返回错误。例如我们可以修改 `search_population` 工具，当 `country=="Japan"` 时故意返回 `{'error': '服务超时'}`。然后观察智能体是否按预期没有崩溃且转入错误处理分支。如果我们在状态里实现了重试机制（比如 Plan 节点检测到错误就再次调用工具），那么应验证智能体会重新尝试查询日本人口。
- **模拟 LLM 输出不当**：由于我们的 Plan 节点逻辑比较严谨，这部分问题不明显。但对于真实 LLM 驱动的 Plan 节点，可以构造一些不符合格式的模型回应，看看系统能否检测并纠正。例如模型输出了一个未定义的工具名，我们的 Tools 节点会返回 `{'error': '未知工具'}`，那么 Plan 节点下一步是否做出了合理处理（比如直接终止回答并告知用户无法完成）？
- **回放与恢复**：如果使用了 LangGraph 的持久化，在测试中可以**中途中断**智能体然后恢复。例如让智能体执行到一半（如已经拿到部分数据）时强行停止进程，再重启看是否能从检查点继续。这模拟了意外宕机的场景。根据 LangGraph 设计，只要启用了 MemorySaver 并使用相同`thread_id`，Agent 应该**从上次状态继续**。

通过上述测试，我们可以发现智能体流程中的薄弱环节，并完善相应的异常处理逻辑。例如，也许需要在 Plan 节点增加一个最大循环次数，避免 LLM 卡住导致无限循环；或者给某些工具设置超时时间，超时则返回错误等。将这些完善后，再次运行回放测试，直到对各种异常情况都有恰当响应为止。

## 端到端示例：多工具智能体解决实际任务

现在让我们将所有组件组装起来，展示一个完整的端到端示例。我们仍然以“查询国家人口并求和”为任务，演示智能体如何自主决定使用检索和计算工具来回答用户问题。

首先，确保已按照前述代码定义了 `State` 类型、`plan_node_fn`、`tool_node_fn`，并构建好了 `graph`：

```python
# （省略前面的 State, plan_node_fn, tool_node_fn 定义和 graph 构建步骤，
#  可假定它们已经按照上述代码执行）
# ...

# 编译智能体应用
app = graph.compile()
```

现在，我们尝试对智能体提问。例如：

```python
# 示例查询 1：需要调用两个工具（检索法国、日本人口并求和）
query1 = "What is the sum of the population of France and Japan?"
result1 = app.invoke({"input": query1})
print(f"Query: {query1}\nAnswer: {result1.get('answer')}")
```

假设我们的本地模型知识涵盖常识数据，上述询问将触发智能体依次调用两个工具。**预期输出**（由于我们用规则模拟，这里直接给出结果）：

```text
Query: What is the sum of the population of France and Japan?
Answer: The total population is 192 million.
```

Agent 的工作过程大致如下：Plan 节点解析出目标国家列表[`France`,`Japan`]，然后输出指示调用检索工具；Tools 节点查询到法国人口为 67（百万），将其存入状态；Plan 再次执行，发现还有一个目标 Japan 未查询，再次输出检索指令；Tools 查询到日本人口 125，存入状态；Plan 第三次执行，检测到已收集两个数值，需要汇总，遂输出计算工具指令；Tools 计算`67+125=192`，附加结果 192 到状态；Plan 第四次执行时检测到结果已汇总，生成最终回答。整个过程中，我们可以通过日志看见类似的决策链：

```text
Plan: Parsed targets ['France','Japan'] from query.
Plan: Decided to use tool 'search_population' for France.
Tools: Executing search_population(France) -> 67
Plan: Decided to use tool 'search_population' for Japan.
Tools: Executing search_population(Japan) -> 125
Plan: Decided to use tool 'calculator' for 67 + 125.
Tools: Executing calculator('67 + 125') -> 192
Plan: Produced final answer.
```

你也可以尝试一个不需要工具的问句，验证智能体会直接给出答案而不走工具流程：

```python
# 示例查询 2：不需要任何工具
query2 = "Is 2+2 equal to 4?"
result2 = app.invoke({"input": query2})
print(f"Query: {query2}\nAnswer: {result2.get('answer')}")
```

如果 Plan 节点判断无需外部信息（例如我们实现中如果没有识别出“population of”就直接返回答案模板），Agent 会立即在第一次 Plan 调用就生成`answer`，根据我们代码会回答类似：“这个问题不需要调用工具，可直接回答。”（实际应用中，可让 LLM 直接回答数学问题或给出正确的计算结果）。

上述示例表明，我们成功构建了一个可以根据需求**动态调用多个工具**的 Agent，并完成了一个端到端任务。开发者可以在此基础上扩展更多工具（例如天气查询、邮件发送等），并丰富 Plan 节点的决策逻辑（通过提示让 LLM 自主选择工具）。

## 最佳实践清单

在构建和部署多工具有状态智能体时，请参考以下最佳实践清单，以确保系统性能和可靠性：

- **上下文管理**：合理利用记忆模块控制对话上下文大小。短期记忆在 prompt 中提供最近信息，长期记忆在需要时检索历史知识。避免每轮都附加过长历史，防止超出模型上下文窗口并引发性能问题。必要时对旧对话进行总结或截断。
- **避免无限循环**：在循环流程中设置安全网，例如最大循环次数或时间限制。当 LLM 连续若干次未能完成任务时，中止循环并给出失败反馈，防止智能体陷入死循环。【提示】LangGraph 可在状态中增加一个计数，每次 Plan 循环 +1，超过阈值则走结束分支。
- **工具设计原则**：确保工具函数**幂等**且尽量**无副作用**，以便重复调用不会产生不一致结果。对于会修改外部状态的工具（如发消息、下单），需要特殊处理避免重复执行——可考虑在状态中标记已执行过，或在工具本身实现去重逻辑。
- **错误处理**：充分考虑各种错误场景，例如工具超时、输出格式不符、LLM 回答偏离预期等。为每种异常设计合理的处理分支或 fallback 答案。宁可让智能体礼貌拒绝，也不要挂起或返回奇怪输出。
- **并发与资源**：如果使用并行工具调用，注意外部 API 的速率限制和本地计算资源占用。LangGraph 允许限制同一“超级步”中的并发数，可根据需要配置，或在工具实现内部加入同步机制。
- **Prompt 设计与测试**：如果 Plan 节点基于 LLM 输出动作，一定要精心设计提示词，明确告诉模型可用工具列表、调用格式、何时停止等。同时准备多样的测试 query 来验证模型不会误用工具。对于关键任务，可以考虑加入**少量规则**校验模型输出，双重保险。
- **调试方法**：利用日志和 trace 追踪每一步决策，尤其在开发早期多观察智能体内部状态的变化。当结果不符合预期时，通过决策记录找出是哪一步出现问题，是 LLM 理解不对还是工具返回有误。调试时也可固定随机种子或使用较小模型，以获得可重复的行为来分析。
- **性能优化**：本地部署模型可能较慢。可以考虑对 LLM 的调用进行优化，例如启用 4-bit 量化模型、减少不必要的 prompt 内容等。对于经常要调用的知识库，优先使用工具/检索代替让 LLM 直接记忆，以减轻模型负担。
- **安全控制**：多工具智能体若可执行任意代码或访问敏感数据，要做好权限隔离和审计。使用 LangChain 时，尽量选择受限的工具函数，不要直接将用户输入传给 `eval` 等高危函数。对 LLM 的输出也需监控，防止其构造恶意指令利用工具。

以上清单并非穷尽，但涵盖了一般场景下开发有状态多工具智能体需要注意的关键点。遵循这些最佳实践，可以大大提升智能体系统在真实环境中的稳定性和可维护性。

## 总结

通过本教程，我们学习了如何使用 LangGraph 提供的 StateGraph 框架，结合 LangChain 的工具和内存组件，创建一个强大的多工具智能体。我们经历了从**状态设计**、**节点编排**、**多工具决策**到**错误处理**、**调试优化**的完整过程。利用这些方法，开发者可以构建出更**灵活**且**可控**的智能体系统，应对复杂多变的任务需求。希望本教程为您的智能体开发实践提供了有益的参考！