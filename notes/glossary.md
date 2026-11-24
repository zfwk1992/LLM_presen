# 术语表

按在演讲中出现的顺序排列。"页面"一列指这个词主要在哪一页讲到。

## LLM 基础

| 英文 | 中文 | 一句话解释 | 页面 |
|---|---|---|---|
| LLM (Large Language Model) | 大语言模型 | 根据已有的 token 预测下一个 token 的神经网络 | 全部 |
| Token | 词元 | 模型处理文本的最小单位，可能是一个词、词的一部分或一个标点 | 01 |
| Tokenization | 分词 | 把文本切成 token 并转换成整数 ID 的过程 | 01 |
| Vocabulary | 词表 | 模型认识的全部 token 的集合，训练后固定 | 01 |
| Sub-word | 子词 | 比词小、比字符大的片段 | 01 |
| BPE (Byte-Pair Encoding) | 字节对编码 | 通过反复合并最常见的相邻片段来构建词表的算法 | 01 |
| Token ID | 词元编号 | token 在词表里的位置编号，数值本身无含义 | 01 |
| Embedding | 嵌入（向量） | 表示一个 token（或一段文字）含义的一串数字 | 02 |
| Embedding matrix | 嵌入矩阵 | 形状为 V × d 的参数表，每个 token 占一行 | 02a |
| Dimension (d) | 维度 | 向量里数字的个数，量级为几千 | 02a |
| Cosine similarity | 余弦相似度 | 用两个向量夹角的余弦衡量相似程度，范围 −1 到 1 | 02b、06 |
| Transformer | — | 当前 LLM 采用的网络结构，由多层 attention + MLP 堆叠而成 | 03 |
| Attention | 注意力 | 让每个位置根据其他位置的内容更新自己的机制 | 03 |
| MLP | 多层感知机 | 每一层里对每个位置单独做变换的部分 | 03 |
| Weights / Parameters | 权重 / 参数 | 网络里通过训练学到的数值，推理时固定不变 | 03、10a |
| Forward pass | 前向传播 | 输入从第一层算到最后一层的一次完整计算 | 03 |
| Logits | — | 网络最后输出的原始分数，词表里每个 token 一个 | 03 |
| Softmax | — | 把一组分数变成加起来等于 1 的概率 | 03 |
| Temperature (T) | 温度 | 控制抽样随机性的参数，越高输出越多样 | 03 |
| Sampling | 采样 | 按概率分布随机选出下一个 token | 03 |
| Autoregressive | 自回归 | 把自己的输出追加到输入里，再生成下一个 | 03 |
| max_tokens | 最大输出长度 | 调用方设定的输出 token 上限 | 03 |
| Inference | 推理 | 使用训练好的模型生成输出（区别于训练） | 03 |

## Agent 与工具

| 英文 | 中文 | 一句话解释 | 页面 |
|---|---|---|---|
| Agent | 智能体 | LLM + 工具 + 循环：能根据结果自己决定下一步的系统 | 04 |
| Agent loop | Agent 循环 | 思考 → 行动 → 观察，重复直到不再需要工具 | 04 |
| Harness | 运行框架 | 模型外面的程序，负责调用模型、执行工具、管理上下文 | 04、05 |
| Context | 上下文 | 模型在某一步能看到的全部内容 | 04、09 |
| Tool | 工具 | 模型可以请求调用的外部功能 | 05 |
| Tool calling / Tool use | 工具调用 | 模型输出结构化的调用请求，由 harness 执行 | 05 |
| tool_use | — | 模型回复中表示"请求调用工具"的内容块 | 05 |
| tool_result | — | 执行结果返回给模型时使用的内容块 | 05 |
| JSON Schema | — | 描述 JSON 数据格式的标准，用于定义工具的参数 | 05 |
| System prompt | 系统提示 | 对话开始前给模型的固定说明 | 05、09 |
| Prompt injection | 提示注入 | 外部内容里夹带指令，试图误导模型 | 05、07 |

## 扩展能力

| 英文 | 中文 | 一句话解释 | 页面 |
|---|---|---|---|
| RAG (Retrieval-Augmented Generation) | 检索增强生成 | 先检索相关内容，放进 prompt，再让模型回答 | 06 |
| Chunk | 文本块 | 文档被切分后的小段 | 06 |
| Indexing | 建索引 | 把文档切块、向量化并存入向量库的离线过程 | 06 |
| Vector database | 向量数据库 | 能快速找到与给定向量最相近的向量的数据库 | 06 |
| Embedding model | 嵌入模型 | 把一整段文字变成一个向量的模型 | 06 |
| Top-k | — | 取相似度最高的前 k 个结果 | 06 |
| Grounded | 有依据的 | 回答基于提供的材料，可追溯出处 | 06 |
| Fine-tuning | 微调 | 用额外数据继续训练模型，改变权重 | 06 |
| MCP (Model Context Protocol) | 模型上下文协议 | AI 应用与外部系统之间的开放通信协议 | 07 |
| Host | 宿主 | 用户直接使用的 AI 应用（如 Claude Code） | 07b |
| MCP client | MCP 客户端 | Host 内部负责和一个 server 通信的部件 | 07b |
| MCP server | MCP 服务器 | 把某个系统的能力按 MCP 格式暴露出来的程序 | 07b |
| Resources | 资源 | MCP server 提供的可读取数据 | 07b |
| Prompts | 提示模板 | MCP server 提供的可复用提示 | 07b |
| JSON-RPC 2.0 | — | MCP 使用的请求/响应消息格式 | 07b |
| stdio | 标准输入输出 | MCP 的本地传输方式，server 是本机子进程 | 07b |
| Skill | 技能 | 包含某类任务的说明和脚本的文件夹 | 08 |
| SKILL.md | — | Skill 的核心文件：名字、简介和操作说明 | 08 |
| Progressive disclosure | 渐进式加载 | 分级按需把内容放进上下文 | 08 |
| CLAUDE.md | — | 项目记忆文件，每次会话都加载 | 08、09 |

## 上下文管理

| 英文 | 中文 | 一句话解释 | 页面 |
|---|---|---|---|
| Context window | 上下文窗口 | 模型一次能处理的 token 数量上限 | 09 |
| Context engineering | 上下文工程 | 管理模型在每一步看到的全部内容 | 09 |
| Prompt engineering | 提示工程 | 琢磨单条指令怎么写 | 09 |
| Context rot | 上下文腐化 | 上下文过长、噪声过多导致效果下降 | 09 |
| Compaction | 压缩 | 把旧的对话总结成简短摘要以释放空间 | 09 |
| Sub-agent | 子 Agent | 在独立上下文中执行任务、只返回结论的 Agent | 09 |
| Prompt caching | 提示缓存 | 重复使用的上下文前缀按更低价格计费 | 10c |

## 模型与成本

| 英文 | 中文 | 一句话解释 | 页面 |
|---|---|---|---|
| Model | 模型 | 一套特定的权重，决定每个 token 的计算量和能力上限 | 10a |
| FLOPs | 浮点运算次数 | 衡量计算量的单位 | 10a |
| Effort | 努力程度 | 同一个模型在一次请求里投入多少工作量 | 10b |
| Thinking | 思考 | 模型在给出答案前生成的推理文字，同样计入输出 token | 10b |
| Input tokens | 输入 token | 发给模型的内容，Agent 每一轮都要重新计入 | 10c |
| Output tokens | 输出 token | 模型生成的内容，包括思考、工具调用和回答 | 10c |
| Latency | 延迟 | 从发出请求到得到结果的时间 | 10c |

## 例子里出现的汽车电子术语

演讲的例子都来自 AUTOSAR 场景，听众如果不是这个领域的，可能需要一句话解释。

| 术语 | 含义 |
|---|---|
| AUTOSAR | 汽车电子软件的标准架构 |
| ECU | 电子控制单元，车上的嵌入式控制器 |
| CAN / LIN / FlexRay / Ethernet | 车内的几种通信总线 |
| Com | AUTOSAR 的通信模块，负责信号的打包与收发 |
| NvM | 非易失性存储管理模块，负责掉电后仍需保存的数据 |
| Dem | 诊断事件管理模块，负责故障记录 |
| NVM_REQ_NOT_OK | NvM 的一个作业结果，表示上一次作业失败 |
| ARXML | AUTOSAR 的 XML 配置文件格式 |
| MISRA C | 汽车行业常用的 C 语言编码规范 |
| ABS / ESP | 防抱死制动系统 / 电子稳定程序 |
