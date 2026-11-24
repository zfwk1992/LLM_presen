# 06a、06b、06c · RAG 的细节：从 PDF 到 Agent 用上它

这三页把 06 那张总览图拆开，沿用 DCM 例子里的那次规范检索（04d 的第 3 次调用 `search_spec("Dcm integration PduR ComM")`）。每页左上角标着 PART 1–3 OF 3，右上角是文档名。

![PDF to chunks](../llm_agent_animations_single_page/06a_rag_pdf_to_chunks.gif)

![Chunks to vectors](../llm_agent_animations_single_page/06b_rag_chunks_to_vectors.gif)

![How the agent uses it](../llm_agent_animations_single_page/06c_rag_agent_uses_it.gif)

> **一句话**：600 页的规范先被切成约 1,800 段文字；每段用一个专门的 embedding 模型算出一个向量，连同原文存起来；Agent 提问时，用问题的向量找出最接近的 3 段，把这 3 段的**原文**放进提示词。向量只用来找，LLM 读到的始终是文字。

## 最容易混淆的一点，先说清楚

"embedding"这个词在整场演讲里出现了两次，指的是**两个不同的东西**：

| | LLM 内部的 embedding 层 | RAG 用的 embedding 模型 |
|---|---|---|
| 在哪里讲的 | 02a–02d | 06b |
| 输入 | 一个 token | 一整段文字 |
| 怎么得到 | 查表，没有计算 | 一个完整的网络读完整段，再汇总成一个向量 |
| 输出 | 250 个 token → 250 个向量 | 250 个 token → 1 个向量 |
| 向量表示什么 | 这个 token 本身，不含上下文 | 这段话在讲什么 |
| 用来干什么 | 作为 LLM 网络的输入 | 找相似的文字 |
| 在哪里 | LLM 内部，是它的第一步 | LLM 外部，一个独立的、通常更小的模型 |
| 什么时候运行 | 每次调用 LLM 都运行 | 建索引时对每段运行一次；每次提问时对问题运行一次 |

两者的共同点只有思想：**用向量的方向表示含义，方向相近表示意思相近。**

所以要避免这样的说法："把规范 embedding 之后送进 LLM"。实际是：规范的向量**从不进入 LLM**，它们只待在向量数据库里用来检索。进入 LLM 的是检索出来的那几段**文字**，这些文字和提示词里的其他内容一样，再经过 LLM 自己的分词和 embedding 层。

## 06a · 从 PDF 到 chunk（22.0 s）

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① The specification is a 600-page PDF: far too big for the prompt | 左边是 PDF 的一页，有标题、正文、表格和图 | "600 页，大约 45 万 token，放不进提示词" |
| 3.8 s | ② Step 1: extract the plain text. Layout, headers and page breaks go | 中间出现提取出来的纯文字 | "第一步是把文字抽出来。版式、页眉、分页都不要了" |
| 7.4 s | ③ Step 2: cut the text into chunks of a few hundred tokens | 文字上出现橙色的切割线，右边出现三张 chunk 卡片 | "第二步是切成小段，每段几百个 token" |
| 11.4 s | ④ Chunks follow the section structure and overlap a little | 第二张卡片开头出现一句黄色高亮的重复内容 | "切的时候尽量沿着章节边界，相邻两段重叠一点" |
| 14.6 s | ⑤ Each chunk keeps its metadata: id, section, page | 三张卡片的标题栏亮起 | "每段都带着编号、章节和页码，之后才能注明出处" |
| 17.6 s | ⑥ Result: about 1,800 small pieces. Still text, not vectors | 出现总数和结论框 | "得到约 1,800 段。它们还是文字，不是向量" |

画面上的三个 chunk：

| 编号 | 位置 | 内容 |
|---|---|---|
| #412 | §7.2.1 · p. 212 | The Dcm receives diagnostic requests from the PduR. Reception starts with Dcm_StartOfReception; the data is copied with Dcm_CopyRxData and finished by Dcm_TpRxIndication. |
| #413 | §7.2.1 · p. 213 | The response is sent with PduR_DcmTransmit. The PduR fetches the data through Dcm_CopyTxData and confirms with Dcm_TpTxConfirmation. |
| #414 | §7.2.2 · p. 213 | While a request is processed, the Dcm keeps the channel awake by calling ComM_DCM_ActiveDiagnostic and releases it with ComM_DCM_InactiveDiagnostic. |

要讲清楚的三件事：

- **为什么要切。** 整份规范放不进提示词；而且一个向量只能概括一小段的意思，段落太长向量就模糊，检索不准。
- **为什么沿章节切、还要重叠。** 一句话如果被从中间切断，两边都读不懂。重叠保证跨边界的内容至少在一段里是完整的。画面上 #413 开头那句 "… finished by Dcm_TpRxIndication." 就是从 #412 重复过来的。
- **这一步不涉及任何 AI 模型。** 结尾的结论框写的是 *Chunking is ordinary text processing. No AI model has been used yet.*

画面左下角还有一句小字：*tables and figures need extra care*。规范里的表格和图用普通的文字提取会丢失结构，实际项目里这是最花功夫的部分，被问到时可以提一句。

## 06b · 从 chunk 到向量（24.0 s）

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① Each chunk goes through an embedding model: a separate network, not the LLM | chunk #412 进入一个青色的 "Embedding model" 框 | "每一段送进一个 embedding 模型。注意：它不是回答你问题的那个 LLM" |
| 3.8 s | ② Out comes one vector for the whole chunk: its meaning as about 1,000 numbers | 右边出来一条向量 | "出来的是一个向量，代表整段话的意思" |
| 6.6 s | ③ Vector, text and metadata are stored together in the vector database | 下方出现数据库表格，第一行是 #412 | "向量、原文、元数据存在同一行里" |
| 9.2 s | ④ Repeat for every chunk, once. This is the offline indexing step | 出现 #413、#414，以及 "1,840 rows" | "对每一段做一次。这是离线完成的，只做一遍" |
| 12.2 s | ⑤ Careful: this is not the embedding layer inside the LLM | 下半部分出现左右两张对比卡片 | **停一下**："这里的 embedding 和前面讲的不是一回事" |
| 15.8 s | ⑥ Inside the LLM: one vector per token. Here: one vector per passage | 对比表逐行出现 | "LLM 内部是每个 token 一个向量；这里是整段一个向量" |

下半部分的两张对比卡片是这一页的重点。左边（蓝色）画的是四个 token 各自对应一条小向量；右边（青色）画的是同样四个 token 汇入一个 "network + pooling" 再出来**一条**向量。

要讲清楚的三件事：

- **这是另一个模型。** 它专门训练来把"意思相近的文字"映射到相近的向量，通常比回答问题的 LLM 小得多。
- **数据库里向量和原文是放在一起的。** 表头写的是 *TEXT (kept next to the vector)*。检索时靠向量找到行，然后取出这一行的原文。
- **向量的大小取决于所用的模型。** 画面写的 "about 1,000 numbers" 是一个常见量级，不是固定值。

结尾的结论框：*Same idea (meaning as direction), different job: one feeds the network, the other is for searching.*

## 06c · Agent 怎么用它（23.0 s）

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0.8 s | ① In call 3 the LLM writes a tool call: search the specification | 左上角是第 3 次 LLM 调用，写出 `search_spec(...)` | "回到 DCM 的例子。第 3 次调用，模型写了一个工具调用" |
| 3.4 s | ② The harness runs the search tool. The question is embedded by the same model | 搜索工具 → embedding 模型 → 问题向量 | "harness 执行搜索工具。问题本身也被同一个模型变成向量" |
| 7.4 s | ③ The question vector is compared with all 1,840 chunk vectors | 数据库表格出现，相似度一行一行算出来 | "问题向量和库里每一行的向量比较" |
| 11.4 s | ④ The three closest chunks win. This is cosine similarity at work | #412、#413、#414 被绿色框出，其余变淡 | "最接近的三段胜出。这就是 02b 讲的余弦相似度真正被用到的地方" |
| 14.2 s | ⑤ Their text, not their vectors, goes back as the tool result | 右边出现 tool_result，里面是三段原文 | **停一下**："返回的是这三段的文字，不是向量" |
| 17.6 s | ⑥ The LLM reads 3 passages instead of 600 pages. It never sees a vector | 文字被追加到提示词；结论框 | "LLM 读到的是 3 段话，而不是 600 页" |

画面上的相似度：

| 编号 | 内容 | 相似度 |
|---|---|---|
| #97 | Dependencies to other modules: header file structure … | 0.41 |
| **#412** | The Dcm receives diagnostic requests from the PduR … | **0.91** |
| **#413** | The response is sent with PduR_DcmTransmit … | **0.88** |
| **#414** | … keeps the channel awake by calling ComM_DCM_Active… | **0.86** |
| #655 | Dcm_GetSesCtrlType returns the active session … | 0.22 |
| #1502 | Configuration container DcmDsdServiceTable … | 0.18 |

问题是 "Dcm integration PduR ComM"，得分最高的三段正好讲的是 Dcm 与 PduR、ComM 的交互。

要讲清楚的四件事：

- **检索是一次普通的工具调用。** 和读文件、跑脚本一样：模型写出请求，harness 执行，结果以文字返回。模型不知道背后用了向量。
- **问题必须用同一个 embedding 模型。** 只有同一个模型算出来的向量才在同一个空间里，相似度才有意义。
- **这是 02b 的余弦相似度真正上场的地方。** 之前说过相似度不是 LLM 推理流程中的一步，它是在这里、在 LLM 外面被计算的。
- **返回的是文字。** 画面左下的绿色框：*Vectors are only used to FIND the right pieces. What goes into the prompt is their text.*

结尾的结论框：*600 pages stay on disk. 3 passages enter the prompt. The LLM never sees a vector from this database.*

## 把整条链路连起来

```
建索引（离线，做一次）
  PDF ──提取文字──▶ 纯文本 ──切分──▶ 1,840 个 chunk ──embedding 模型──▶ 1,840 个向量
                                          │                              │
                                          └──────── 存入向量数据库（向量 + 原文 + 元数据）

提问（在线，每次检索）
  LLM 写出工具调用 ──▶ harness 运行搜索工具 ──▶ 问题 ──embedding 模型──▶ 问题向量
                                                                          │
                                         与库里每个向量算相似度 ◀─────────┘
                                                    │
                                         取最接近的 3 行的原文
                                                    │
                                         作为 tool_result 追加到提示词
                                                    │
                                         下一次 LLM 调用读到这 3 段文字
```

涉及的两个模型和它们各自处理的东西：

| | embedding 模型 | LLM |
|---|---|---|
| 处理 1,840 个 chunk | ✔（建索引时） | ✘ |
| 处理问题 | ✔（变成向量） | ✔（它写出了这个问题） |
| 看到向量数据库里的向量 | ✔（它算出来的） | ✘ |
| 看到检索出的 3 段文字 | ✘ | ✔ |
| 写出答案 | ✘ | ✔ |

## 容易想错的地方

- **"规范被 embedding 之后送进了 LLM"**：没有。向量留在数据库里，进入 LLM 的是文字。
- **"RAG 的 embedding 就是 LLM 的 embedding 层"**：不是，是另一个独立的模型，输出的是整段一个向量。
- **"向量里存着原文"**：向量只是约一千个数字，无法还原出原文。原文是另外存在同一行里的。
- **"LLM 自己去搜索向量库"**：不是。它只写出一个工具调用，搜索由 harness 运行的工具完成。
- **"检索出来的一定是对的"**：不一定。相似度高只说明主题接近。如果切分不好或问法偏了，可能取回不相关的段落，LLM 就会基于错误的材料回答。
- **"建好索引就一劳永逸"**：规范更新后必须重新建索引，否则检索到的是旧内容。

## 画面上的简化

- **文字内容是为演示改写的**，章节号、页码也是示意。里面的接口名（`Dcm_StartOfReception`、`Dcm_CopyRxData`、`Dcm_TpRxIndication`、`PduR_DcmTransmit`、`Dcm_CopyTxData`、`Dcm_TpTxConfirmation`、`ComM_DCM_ActiveDiagnostic`）是 AUTOSAR 里真实存在的。
- **相似度数值是示意的。**
- **"和每一行比较"是概念上的说法。** 数据量大时，向量数据库用近似算法只比较一部分就能找到最接近的，不会真的逐行算。
- **只画了纯向量检索。** 实际系统常常把向量检索和关键词检索结合，再用一个模型对结果重新排序。
- **`search_spec` 是虚构的工具名**，实际可以由 MCP server 提供。
- **chunk 的大小、重叠多少、向量维数**都是可调的工程参数，画面上的数字只是常见量级。

## 和其他页的关系

| 页 | 内容 |
|---|---|
| 02b | 余弦相似度是什么（当时强调它不是 LLM 流程里的一步） |
| 04d | 完整会话的第 3 次调用，就是这里展开的那次检索 |
| 06 | RAG 的总览，一页讲完 |
| **06a–06c** | 把 06 拆成三步细讲 |
| 07 | 搜索工具可以由 MCP server 提供 |
| 09 | 为什么只取 3 段而不是整本：上下文是有限的 |

时间有限时的取舍：`06` 和 `06a–06c` 内容重叠。只想点到为止就放 `06`；想讲清楚就放 `06a`、`06b`、`06c`，可以不放 `06`。如果只能放一页细节，放 `06c`，它把检索和 Agent 接上了。

## 自测

<details>
<summary>1. 从 PDF 到 chunk 这一步用到了哪个 AI 模型？</summary>

没有用到。这一步是普通的文字提取和切分。
</details>

<details>
<summary>2. 一段 250 个 token 的文字，经过 LLM 内部的 embedding 层得到几个向量？经过 RAG 的 embedding 模型呢？</summary>

前者 250 个，每个 token 一个。后者 1 个，代表整段。
</details>

<details>
<summary>3. 向量数据库的一行里存着什么？</summary>

这个 chunk 的向量、原文和元数据（编号、章节、页码）。
</details>

<details>
<summary>4. Agent 检索规范时，LLM 做了什么？harness 做了什么？</summary>

LLM 写出一个搜索的工具调用。Harness 运行搜索工具：把问题变成向量，和库里的向量比较，取出最接近的几段原文，作为工具结果返回。
</details>

<details>
<summary>5. 最终进入提示词的是向量还是文字？LLM 见过这些向量吗？</summary>

是文字。LLM 从未见过向量数据库里的向量。
</details>

<details>
<summary>6. 余弦相似度在整条链路的哪里被计算？</summary>

在检索这一步，由搜索工具在 LLM 外部计算：问题向量与每个 chunk 向量之间。
</details>
