# 06 · RAG（检索增强生成）

![RAG](../llm_agent_animations_single_page/06_rag.gif)

> 这一页是总览。想把每一步讲细（PDF 怎么变成 chunk、chunk 怎么变成向量、它和 LLM 内部的 embedding 层有什么区别、Agent 实际怎么调用），看 [06abc_rag_in_detail.md](06abc_rag_in_detail.md) 里的三页。

> **一句话**：模型不知道你们公司的文档。RAG 的做法是先把相关的段落找出来，贴进 prompt，再让模型回答。模型本身不需要重新训练。

## 在演讲里的位置

第三章的第一页。这一章四页（RAG、MCP、Skills、Context Engineering）回答同一个问题：**怎样在正确的时刻把正确的信息放进上下文**。RAG 是其中最经典的一种：信息来自你自己的文档库。它用到 02b 的余弦相似度，讲的时候可以回扣。

## 名字拆解

**R**etrieval-**A**ugmented **G**eneration：

- **Retrieval**（检索）：从文档库里找出相关内容。
- **Augmented**（增强）：把找到的内容加进 prompt。
- **Generation**（生成）：模型照常生成回答（03 的循环）。

## 画面布局

画面分成上、中、下三层：

- **上层 · INDEXING · offline**：建索引，提前做一次。
- **中层 · QUERY · online**：每次提问时做。
- **右上 · Vector database**：向量数据库，两个阶段都用到。
- **下层**：最终发给模型的 prompt 和模型的回答。

## 动画逐步解读

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0–3 s | Indexing: split your documents into chunks | AUTOSAR specs 被切成小块 | "文档太长，先切成段" |
| 3–7 s | Embed every chunk and store the vectors | 小块经过 Embed 变成点，落入向量库，形成三簇 | "每一段变成一个向量，意思相近的落在一起" |
| 7–9 s | Query: embed the question into the same vector space | 问题 "How does NvM handle a failed write?" 也经过 Embed | "问题用同一个模型变成向量" |
| 10–11.5 s | Retrieve the k most similar chunks | 向量库里出现红色的 query 点，落在 NvM 那一簇，圈出最近的 3 个 | "找离问题最近的几段" |
| 12–14 s | Insert the retrieved chunks into the prompt | 下方的 prompt 逐行填入 | "把这几段原文贴进 prompt" |
| 15.5–19 s | The answer is grounded in your documents, with no retraining | LLM 输出回答和来源 | "模型根据贴进去的内容回答，并注明出处" |

向量库里的三簇：**Com docs**、**Dem docs**、**NvM docs**。问题是关于 NvM 的，所以 query 点落在 NvM 那一簇里。

## 最终的 prompt

```
SYSTEM    Answer using only the context below. Cite sources.
CHUNK     #12  "If a write job fails, NvM shall retry it …"
CHUNK     #7   "When all retries fail, the job result is set …"
CHUNK     #31  "NVM_REQ_NOT_OK indicates the last job failed …"
QUESTION  How does NvM handle a failed write?
```

回答：

```
When a write fails, NvM retries it.
If all retries fail, the job result becomes NVM_REQ_NOT_OK.
Sources: chunk #12, #7
```

这里要让听众看明白：**模型没有任何变化**。变的只是 prompt 里多了三段原文。模型的"知识"来自这三段文字，而不是它的权重。

## 需要真正搞懂的概念

### 两个阶段

| | 建索引（offline） | 查询（online） |
|---|---|---|
| 什么时候做 | 提前做一次，文档更新时重做 | 每次用户提问 |
| 步骤 | 切块 → 向量化 → 存入向量库 | 问题向量化 → 找最近的 k 个 → 拼 prompt → 生成 |
| 耗时 | 可以很长 | 必须很快 |

### 为什么要切块

- 整份规范放不进上下文，或者放进去代价太高。
- 一个向量只能概括一小段的意思。段落太长，向量就变得模糊，检索不准。
- 切多大是工程上的权衡：太小会丢失上下文，太大检索不精确。相邻的块之间通常留一些重叠。

### 检索靠的是语义，不是关键词

问题里写的是 "failed write"，文档里写的可能是 "write job fails" 或 "NVM_REQ_NOT_OK"。字面不完全一样，但向量相近，所以能找到。这就是 02b 里余弦相似度的用途。画面里的标注是 "top-k = 3 · highest cosine similarity"。

### 这里的 Embed 不是 02 里的那张表

02 讲的是 LLM 内部把**一个 token** 变成向量。这里的 Embed 是一个单独的 embedding 模型，把**一整段文字**变成一个向量。思想相同，部件不同。建索引和查询必须用同一个 embedding 模型，否则两边的向量不在同一个空间里，无法比较。字幕里的 "the same vector space" 说的就是这一点。

### "Grounded" 是什么意思

回答的依据是 prompt 里的原文。好处：

- **可追溯**：回答附带出处（Sources: chunk #12, #7），可以回去核对。
- **可更新**：文档改了，重建索引即可，不需要动模型。
- **减少编造**：system 提示里写了 "Answer using only the context below"，让模型只根据给定内容回答。

### RAG 会在哪里失败

值得了解，因为听众里做过的人会问：

- **没检索到**：相关段落没进前 k 名，模型没有依据，可能答错或答"不知道"。
- **切坏了**：关键信息刚好被切在两块之间。
- **索引过期**：文档更新了，索引没更新。
- **检索到了但没用好**：贴进去的内容太多、太杂，模型抓不住重点（09 会讲）。

RAG 的质量大部分取决于**检索**这一步，而不是模型。

### RAG 和 Agent 的搜索

RAG 是"先检索、后回答"，检索只做一次，由程序决定。Agent 也可以自己搜索：它调用搜索工具，看结果，不满意就换个关键词再搜（04 的循环）。Claude Code 在代码库里找东西用的就是后一种方式（grep、读文件），而不是预先建好的向量索引。两种方式可以并存。

## 常见误解

- **"RAG 是在训练模型"**：不是。权重不变，只是 prompt 变了。
- **"用了 RAG 就不会出错"**：检索不到或检索错了，回答照样会错。
- **"向量数据库里存的是文档的理解"**：存的是每一段的向量和原文。向量只用来找，最后贴进 prompt 的是原文。

## 听众可能会问

**Q：和微调（fine-tuning）相比怎么选？**
RAG 适合知识会变、需要出处、数据量大的情况，不改模型，更新快。微调适合改变模型的风格或让它掌握某种固定任务格式，成本高、更新慢。多数"让模型了解我们的文档"的需求，RAG 就够了。

**Q：现在上下文窗口这么大，直接把文档全塞进去不行吗？**
小规模可以，而且更简单。但文档多的时候，一是放不下，二是每次都付全部的费用，三是无关内容太多反而影响效果（见 09）。

**Q：k 取多少合适？**
没有固定答案，常见是几个到十几个。太少可能漏掉，太多引入噪声。

**Q：向量数据库是什么特别的东西吗？**
它的专长是"给一个向量，快速找到最相近的若干个向量"。数据量大时用近似算法来保证速度。

## 承上启下

- **上一章**：Agent 能动手，但只知道训练数据和上下文里的内容。
- **这一页**：把你的文档接进来。
- **下一页**：文档之外，还有活的系统（Jira、Git、构建服务器）。下一页讲怎么接。
- **过渡句**："RAG 解决的是'读文档'。但很多信息不在文档里，而在系统里：某个 issue 的状态、昨天的提交记录。这些要怎么接？"

## 自测

<details>
<summary>1. RAG 的两个阶段各做什么？</summary>

建索引：切块、向量化、存入向量库。查询：把问题向量化，找最相近的 k 个块，拼进 prompt，让模型生成回答。
</details>

<details>
<summary>2. RAG 改变了模型的什么？</summary>

什么都没改。只改变了发给模型的 prompt。
</details>

<details>
<summary>3. 为什么建索引和查询必须用同一个 embedding 模型？</summary>

只有同一个模型产生的向量才在同一个空间里，相似度才有意义。
</details>
