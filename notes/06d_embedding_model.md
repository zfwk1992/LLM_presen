# 06d · RAG 里的 embedding 模型长什么样

这篇是 [06abc_rag_in_detail.md](06abc_rag_in_detail.md) 的补充，没有对应的 GIF。它回答三个问题：这个模型有多大、谁来提供、内部大概是什么样子。

> **一句话**：embedding 模型是一个比 LLM 小得多的 Transformer，它读完一段文字，输出一个固定长度的向量。搭 RAG 的人不需要训练它，从现成的模型里选一个用就行。

## 先回答两个问题

### 它是一个小模型吗？

**是的，相对 LLM 来说小得多。**

| | embedding 模型 | 回答问题的 LLM |
|---|---|---|
| 参数量 | 几千万到几亿 | 远大于此，商用模型一般不公布 |
| 文件大小 | 一百多 MB 到一两 GB | 远大于此 |
| 能在哪里跑 | 笔记本电脑的 CPU 就能跑 | 需要数据中心的 GPU |
| 处理一段文字 | 毫秒到几十毫秒 | 取决于输出长度，以秒计 |
| 输出 | 一个向量 | 一段文字 |

小的原因是它的任务简单得多：只需要"理解"一段话并压缩成一个向量，不需要生成任何东西。

### 需要搭 RAG 的人自己做吗？

**不需要自己做，需要自己选。**

训练一个 embedding 模型需要大量的文本对和算力，几乎没有人为了搭一个 RAG 去训练它。实际的做法是：

- **用开源模型**：下载下来，在自己的机器上跑。
- **用 API**：把文字发给服务商，对方返回向量。

搭 RAG 的人要做的是**选型**和**使用**：选哪个模型、在哪里跑、怎么切 chunk、向量存哪里。少数情况下，会在自己的领域数据上对现成模型做微调，但这是进阶做法，起步时不需要。

## 它内部长什么样

以一个 chunk 为例，文字进去、向量出来，中间经过五步：

```
"The Dcm receives diagnostic requests from the PduR. …"
        │
        ▼  ① 分词（它有自己的分词器）
[ The | ·Dcm | ·receives | ·diagnostic | ·requests | … ]      约 250 个 token
        │
        ▼  ② 查表：每个 token 一个向量（它有自己的 embedding 层）
250 个向量
        │
        ▼  ③ 经过若干层 Transformer（attention + MLP）
250 个向量，每个都融合了整段话的信息
        │
        ▼  ④ 池化（pooling）：把 250 个向量合成 1 个
1 个向量
        │
        ▼  ⑤ 归一化：把长度缩放成 1
1 个向量，例如 384 维或 1024 维
```

这个结构你应该很眼熟：前三步和 02a–02e 讲的 LLM 内部几乎一样。区别在第 ④ 步和第 ⑤ 步，以及第 ③ 步的一个细节。

### 和 LLM 的三处关键区别

**1. 它能看到整段话的前后文。**

LLM 里每个 token 只能读取它**前面**的 token（02e 讲过，因为后面的还没生成）。embedding 模型不生成任何东西，整段话一开始就都在，所以每个 token 可以同时读取它**前面和后面**的 token。这让它对整段话的理解更完整。

**2. 它最后做池化，而不是预测下一个 token。**

LLM 取最后一个位置的向量，去和词表里的每个 token 比对，得到下一个 token 的概率。

embedding 模型取所有位置的向量，合成一个。最常见的合法是**求平均**（mean pooling）：把 250 个向量逐维相加再除以 250。也有的模型在开头放一个特殊 token，只取它的输出向量。

**3. 它没有生成循环。**

一段文字进去，一次前向传播，一个向量出来，结束。没有"选一个 token 接回去再算"这回事。所以它很快。

### 一个容易绕晕的地方

embedding 模型的第 ② 步里，也有一个 embedding 层。所以准确地说：

- **embedding 层**（查表，每个 token 一个向量）：LLM 里有，embedding 模型里也有。它是 Transformer 的标准第一步。
- **embedding 模型**（整个网络，整段话一个向量）：指的是上面五步合起来的那个东西。

06b 那张图里对比的是"LLM 的 embedding 层"和"embedding 模型的最终输出"，这两者的输入、输出和用途都不同。

## 它是怎么训练出来的

LLM 的训练目标是"预测下一个 token"。embedding 模型的训练目标不一样，叫**对比学习**：

1. 准备大量的文本对：一个问题，和一段能回答它的文字。
2. 训练时要求：配对的两段，向量要**靠近**；不配对的两段，向量要**远离**。
3. 重复几亿次之后，模型学会了把"意思相关"的文字映射到相近的方向。

这就是为什么问题 "Dcm integration PduR ComM" 和讲 Dcm 与 PduR 交互的那段文字，虽然用词不完全一样，向量却很接近。

你不需要做这件事，但了解它能解释一个现象：**通用模型没见过你们的内部术语**。如果文档里充满了只有你们公司才用的缩写，检索效果可能打折扣，这时才需要考虑微调或者配合关键词检索。

## 具体例子

下面是一些常见的 embedding 模型，帮你建立量级上的概念。**这些数字是我凭记忆写的，各家也在不断更新，选型时请以官方页面为准。**

### 开源，可以在自己机器上跑

| 模型 | 参数量 | 向量维数 | 特点 |
|---|---|---|---|
| all-MiniLM-L6-v2 | 约 2,200 万 | 384 | 非常小、非常快，入门常用 |
| bge-small-en-v1.5 | 约 3,300 万 | 384 | 小，英文效果不错 |
| bge-base-en-v1.5 | 约 1.1 亿 | 768 | 中等 |
| bge-large-en-v1.5 | 约 3.4 亿 | 1024 | 较大，英文效果更好 |
| bge-m3 | 约 5.7 亿 | 1024 | 多语言，支持较长的输入 |
| multilingual-e5-large | 约 5.6 亿 | 1024 | 多语言 |

### 通过 API 使用

| 提供方 | 模型举例 | 向量维数 |
|---|---|---|
| OpenAI | text-embedding-3-small / -large | 1536 / 3072 |
| Voyage AI | voyage 系列 | 约 1024 |
| Cohere | embed 系列 | 约 1024 |
| Google | Gemini 的 embedding 模型 | 约 768 起 |

Anthropic 自己不提供 embedding 模型，文档里推荐配合第三方的使用。

作为对比：上表里最大的开源模型也只有几亿参数，而当前的 LLM 要大出好几个数量级。

## 用起来是什么样子

下面是用开源库调用一个小模型的示意代码，帮你建立直观印象。**这段代码我没有在你的机器上运行过。**

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-small-en-v1.5")   # 约 130 MB，会自动下载

chunks = [
    "The Dcm receives diagnostic requests from the PduR. Reception starts with Dcm_StartOfReception …",
    "The response is sent with PduR_DcmTransmit. The PduR fetches the data through Dcm_CopyTxData …",
    "Dcm_GetSesCtrlType returns the active session …",
]

# 建索引：每个 chunk 一个向量
chunk_vectors = model.encode(chunks, normalize_embeddings=True)
print(chunk_vectors.shape)        # (3, 384)：3 个 chunk，每个 384 个数字

# 提问：问题也用同一个模型变成向量
question = model.encode(["Dcm integration PduR ComM"], normalize_embeddings=True)

# 向量已归一化，点积就是余弦相似度
scores = chunk_vectors @ question.T
print(scores)                     # 前两段的分数应明显高于第三段
```

整个"建索引加检索"的核心就是这几行。真实的 RAG 系统在此之上加了：文档解析、切分、向量数据库、结果重排序。

## 搭 RAG 的人实际要做的决定

对你们的场景（AUTOSAR 规范和内部文档），选型时要考虑：

| 问题 | 为什么重要 | 对你们的提示 |
|---|---|---|
| **数据能不能出公司？** | 用 API 意味着把文档内容发给第三方 | 内部文档或受限的规范，优先考虑本地运行的开源模型 |
| **什么语言？** | 英文模型处理不好中文 | 规范是英文，但如果同事用中文提问，需要多语言模型 |
| **一次能读多长？** | 每个模型有最大输入长度，老一些的模型约 512 个 token | chunk 的大小不能超过模型的上限，否则后面的内容被截断 |
| **向量多少维？** | 维数越高，存储和检索越贵，效果通常略好 | 几千个 chunk 的规模下，这不是瓶颈 |
| **速度和成本** | 建索引时每个 chunk 跑一次，检索时每个问题跑一次 | 1,840 个 chunk 用小模型在 CPU 上几分钟就能建完 |

两条硬规则：

- **建索引和检索必须用同一个模型。** 不同模型的向量不在同一个空间里，无法比较。
- **换模型就要重建全部索引。** 所以选型值得一开始就想清楚。

## 常见问题

**Q：embedding 模型能回答问题吗？**
不能。它只输出一个向量，没有生成文字的能力。

**Q：能不能直接用 LLM 来做 embedding？**
概念上可以从 LLM 的内部取出向量，也有基于 LLM 改造的 embedding 模型。但专门训练的 embedding 模型又小又快，效果也好，通常没必要。

**Q：向量能还原回原文吗？**
不能可靠地还原。它是有损的压缩：一千个数字装不下一段话的全部细节。所以向量数据库必须把原文存在旁边。

**Q：embedding 模型和 LLM 必须是同一家的吗？**
不必。它们之间没有任何技术上的关联：embedding 模型只负责检索，检索出来的是文字，文字可以交给任何 LLM。

**Q：效果不好怎么办？**
先检查切分（chunk 是否被切得支离破碎），再看是否需要加上关键词检索，然后才考虑换模型或微调。多数问题出在切分和文档解析上，而不是模型上。

## 和前面内容的对应

| 这里讲的 | 对应的页 |
|---|---|
| 分词、embedding 层、Transformer 层 | 01、02a、02d、02e |
| "意思相近则方向相近" | 02b |
| 余弦相似度的计算 | 02b、06c |
| 每个 chunk 一个向量，存入数据库 | 06b |
| 问题用同一个模型变成向量 | 06c |

## 自测

<details>
<summary>1. embedding 模型和 LLM 相比，大小大概差多少？</summary>

embedding 模型是几千万到几亿参数，笔记本电脑就能跑；LLM 要大出好几个数量级，需要数据中心的 GPU。
</details>

<details>
<summary>2. 搭 RAG 的人需要训练 embedding 模型吗？</summary>

不需要。从开源模型或 API 里选一个现成的。少数情况下才做微调。
</details>

<details>
<summary>3. 一段 250 个 token 的文字在 embedding 模型里经历了什么？</summary>

分词 → 每个 token 查表得到向量 → 经过若干层 Transformer → 把 250 个向量池化成 1 个 → 归一化。
</details>

<details>
<summary>4. embedding 模型和 LLM 在结构上有哪三处关键区别？</summary>

它的每个 token 能同时读取前后文；它最后做池化而不是预测下一个 token；它没有生成循环，一次前向传播就结束。
</details>

<details>
<summary>5. 为什么建索引和检索必须用同一个模型？</summary>

不同模型产生的向量不在同一个空间里，相似度没有意义。
</details>
