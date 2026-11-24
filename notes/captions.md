# 每页动画底部的说明文字

动画播放时，画面底部会依次出现一条条说明。这里把每个 GIF 的说明按出现顺序全部列出来，可以直接贴到对应的 PPT 页上，这样不用等动画播到那一步也能看到全部要点。

- **英文原文**逐字取自动画，放在代码块里，方便整段复制。
- **中文**是我加的翻译，动画里没有。
- **出现时间**是这条说明在该 GIF 里开始显示的时刻。每条说明显示到下一条出现为止，最后一条停留到动画结束。

## 01 · Tokenization

`01_tokenization.gif`

```
Input: plain text
Text is split into sub-word tokens (Byte-Pair Encoding)
Each token is mapped to an integer ID from a fixed vocabulary
Common words → 1 token · rare words → several tokens
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | Input: plain text | 输入：纯文本 |
| 3.5 s | Text is split into sub-word tokens (Byte-Pair Encoding) | 文本被切分成子词 token（字节对编码） |
| 5.7 s | Each token is mapped to an integer ID from a fixed vocabulary | 每个 token 映射为固定词表中的一个整数 ID |
| 9.3 s | Common words → 1 token · rare words → several tokens | 常见词 → 1 个 token · 少见词 → 多个 token |

## 02a · Embedding（查表）

`02a_embedding_lookup.gif`

```
Each token ID selects one row of a learned matrix
That row is the token's vector: a list of d numbers
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.9 s | Each token ID selects one row of a learned matrix | 每个 token ID 从一个学习得到的矩阵中选出一行 |
| 3.5 s | That row is the token's vector: a list of d numbers | 这一行就是该 token 的向量：由 d 个数字组成 |

## 02b · Embedding（向量空间）

`02b_embedding_space.gif`

```
Training places tokens with similar meaning close together
Similarity = angle between vectors (cosine similarity)
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.5 s | Training places tokens with similar meaning close together | 训练使含义相近的 token 彼此靠近 |
| 4.8 s | Similarity = angle between vectors (cosine similarity) | 相似度 = 向量之间的夹角（余弦相似度） |

这一页在动画最后两秒，右下角还会出现一个橙色说明框（不在底部说明条里）：

```
Not a step in the pipeline
This is not computed before the vectors go in.
It only shows what training produced.
The vectors go straight into the network.
```

中文：这不是流程中的一步。向量进入网络之前并不会计算它。它只是展示训练得到的结果。向量是直接进入网络的。

## 02c · 完整路径

`02c_whole_path.gif`

```
① The input is a list of tokens; each token has an ID
② Each ID is looked up: n tokens become n vectors
③ All n vectors go in together: one forward pass, not token by token
④ Each output vector predicts the token after it: only the last is new
⑤ That one vector is matched against every token: one score each
⑥ One token is picked and appended to the input
⑦ Next round: n + 1 vectors, one more forward pass. That is the loop
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | ① The input is a list of tokens; each token has an ID | ① 输入是一串 token，每个 token 有一个 ID |
| 3.6 s | ② Each ID is looked up: n tokens become n vectors | ② 每个 ID 查表：n 个 token 变成 n 个向量 |
| 6.4 s | ③ All n vectors go in together: one forward pass, not token by token | ③ n 个向量一起进入：一次前向传播，不是逐个 token 进入 |
| 9.2 s | ④ Each output vector predicts the token after it: only the last is new | ④ 每个输出向量预测的是它后面的那个 token：只有最后一个是新的 |
| 11.8 s | ⑤ That one vector is matched against every token: one score each | ⑤ 这一个向量与每个 token 逐一匹配：每个 token 得到一个分数 |
| 14.6 s | ⑥ One token is picked and appended to the input | ⑥ 选出一个 token，追加到输入末尾 |
| 17.8 s | ⑦ Next round: n + 1 vectors, one more forward pass. That is the loop | ⑦ 下一轮：n + 1 个向量，再做一次前向传播。这就是循环 |

这一页最后在画面下方还有一个深色框和两行文字：

```
Vectors in → probabilities out → one token → repeat
One forward pass per generated token. The prompt goes in all at once, not token by token.
Cosine similarity is not a step on this path: it only describes the vector space.
```

中文：向量进 → 概率出 → 一个 token → 重复。每生成一个 token 做一次前向传播；提示词是一次性全部进入的，不是逐个 token 进入。余弦相似度不是这条路径上的一步，它只是在描述向量空间。

## 02d · 向量进入 Transformer

`02d_vectors_into_transformer.gif`

```
① Each token ID is looked up: one vector per token
② Position is added, so the model knows the word order
③ Attention: each vector pulls in information from earlier tokens
④ MLP: then every vector is transformed on its own
⑤ Repeat for N layers: same shape, richer meaning
⑥ The last vector is scored against every token in the vocabulary
One forward pass, done. Next: the generation loop
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | ① Each token ID is looked up: one vector per token | ① 每个 token ID 查表：一个 token 得到一个向量 |
| 4.6 s | ② Position is added, so the model knows the word order | ② 加入位置信息，模型才知道词序 |
| 7.6 s | ③ Attention: each vector pulls in information from earlier tokens | ③ Attention：每个向量从前面的 token 读取信息 |
| 12.0 s | ④ MLP: then every vector is transformed on its own | ④ MLP：然后每个向量各自做一次变换 |
| 14.4 s | ⑤ Repeat for N layers: same shape, richer meaning | ⑤ 重复 N 层：形状不变，含义越来越丰富 |
| 17.2 s | ⑥ The last vector is scored against every token in the vocabulary | ⑥ 最后一个向量与词表中的每个 token 逐一打分 |
| 20.6 s | One forward pass, done. Next: the generation loop | 一次前向传播完成。下一步：生成循环 |

这一页最后在右下角还有一个深色框，是全页的结论：

```
No similarity step in between: vectors go straight in.
```

中文：中间没有"计算相似度"这一步，向量直接进入网络。

## 02e · 一个网络，复制给每个 token

`02e_one_network_per_token.gif`

```
① One token: its vector of d numbers goes through one small network
② Five tokens: the same network is used five times, at the same time
③ Attention links the copies: each token reads the ones before it
④ Attention + MLP is one layer. All columns pass layer after layer
⑤ The last column has seen everything: its output gives the next token
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | ① One token: its vector of d numbers goes through one small network | ① 一个 token：它的向量（d 个数）通过一个小网络 |
| 5.0 s | ② Five tokens: the same network is used five times, at the same time | ② 五个 token：同一个网络被用五次，而且是同时 |
| 9.6 s | ③ Attention links the copies: each token reads the ones before it | ③ Attention 把这些副本连起来：每个 token 读取它前面的 token |
| 14.6 s | ④ Attention + MLP is one layer. All columns pass layer after layer | ④ Attention + MLP 是一层。所有列一层接一层地通过 |
| 18.2 s | ⑤ The last column has seen everything: its output gives the next token | ⑤ 最后一列读到了全部内容：它的输出给出下一个 token |

画面右侧还有几段说明和结尾的深色框：

```
Width = d: the size of one vector, not the number of tokens
Attention = the links: each token reads the tokens before it; earlier tokens never read later ones
one set of weights (for this layer): stored once, used in every column
5 tokens → 5 columns, no extra weights
Layer by layer: every column passes layer 1, then every column passes layer 2, …
One set of weights. One column per token.
```

中文：宽度 = d，是一个向量的大小，不是 token 的个数。Attention 就是连接：每个 token 读取它前面的 token，前面的 token 从不读取后面的。（这一层）只有一套权重：只存一份，每一列都用它。5 个 token → 5 列，不增加权重。逐层推进：所有列通过第 1 层，然后所有列通过第 2 层……一套权重，每个 token 一列。

## 02f · 新 token 加一列

`02f_new_token_adds_column.gif`

```
① The prompt: 5 tokens, 5 columns, all computed in one pass
② The last column gives the next token
③ The new token becomes column 6: only this column is new work
④ It reads the saved results of the columns before it
⑤ Every new token adds one column: more to read, same weights
⑥ Longer context costs more per step; the network never changes
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | ① The prompt: 5 tokens, 5 columns, all computed in one pass | ① 提示词：5 个 token，5 列，一次全部算完 |
| 4.6 s | ② The last column gives the next token | ② 最后一列给出下一个 token |
| 7.4 s | ③ The new token becomes column 6: only this column is new work | ③ 新 token 成为第 6 列：只有这一列是新的计算 |
| 11.0 s | ④ It reads the saved results of the columns before it | ④ 它读取前面各列保存下来的结果 |
| 14.6 s | ⑤ Every new token adds one column: more to read, same weights | ⑤ 每个新 token 增加一列：要读的更多，权重不变 |
| 18.6 s | ⑥ Longer context costs more per step; the network never changes | ⑥ 上下文越长，每一步代价越高；网络本身从不改变 |

画面右侧的面板和结尾的深色框：

```
This forward pass
tokens in context          5 → 6 → 7
columns computed now       5 → 1 → 1
columns read from memory   0 → 5 → 6
weights                    same

Longer context: every new column has more columns to read, so each step costs a little more
New token = new column. The weights stay the same.
```

中文：本次前向传播。上下文中的 token 数：5 → 6 → 7。本次计算的列数：5 → 1 → 1。从保存结果中读取的列数：0 → 5 → 6。权重：不变。上下文更长：每个新列要读取的列更多，所以每一步的代价都高一点。新 token = 新的一列。权重保持不变。

## 03 · Generation Loop

`03_generation_loop.gif`

```
① The whole context goes through the network: one forward pass
② Output: a probability for every token in the vocabulary
③ Pick one token and append it to the context
Sampling: not always the most likely token (temperature T)
④ Repeat: each new token becomes part of the next input
Autoregressive: one token per step, until <end> or max_tokens
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 1.4 s | ① The whole context goes through the network: one forward pass | ① 整个上下文通过网络：一次前向传播 |
| 4.2 s | ② Output: a probability for every token in the vocabulary | ② 输出：词表中每个 token 的概率 |
| 7.1 s | ③ Pick one token and append it to the context | ③ 选出一个 token，追加到上下文末尾 |
| 9.8 s | Sampling: not always the most likely token (temperature T) | 采样：不一定选概率最高的 token（温度 T） |
| 14.8 s | ④ Repeat: each new token becomes part of the next input | ④ 重复：每个新 token 都成为下一次输入的一部分 |
| 20.9 s | Autoregressive: one token per step, until \<end\> or max_tokens | 自回归：每步一个 token，直到 \<end\> 或 max_tokens |

## 04a · LLM 实际收到了什么

`04a_one_big_prompt.gif`

```
① You type one short message
② The harness adds the rest: system prompt, tools, CLAUDE.md, skill list
③ Everything is joined into one long token sequence
④ That whole sequence goes into the LLM at once
⑤ Skills: only the one-line descriptions are in it, not the full text
⑥ The context window is the prompt: you typed a tiny part of it
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | ① You type one short message | ① 你输入一句很短的话 |
| 3.6 s | ② The harness adds the rest: system prompt, tools, CLAUDE.md, skill list | ② harness 补上其余部分：系统提示、工具、CLAUDE.md、skill 列表 |
| 7.0 s | ③ Everything is joined into one long token sequence | ③ 所有内容被拼成一条很长的 token 序列 |
| 11.6 s | ④ That whole sequence goes into the LLM at once | ④ 这一整条序列一次性进入 LLM |
| 15.0 s | ⑤ Skills: only the one-line descriptions are in it, not the full text | ⑤ Skill：里面只有一行简介，没有全文 |
| 18.6 s | ⑥ The context window is the prompt: you typed a tiny part of it | ⑥ 上下文窗口就是提示词：你打的只是其中极小的一部分 |

画面上的其他文字：

```
The LLM sees tokens. It has no idea which part you typed.
dcm-guide: only its one-line description is in here.
The full SKILL.md is added later, if the model decides the task needs it.
The context window is the prompt. You typed 9 of its 14,709 tokens.
```

中文：LLM 看到的是 token，它不知道哪一部分是你打的。dcm-guide：这里只有它的一行简介。完整的 SKILL.md 之后才会加入，前提是模型判断任务需要它。上下文窗口就是提示词。在它的 14,709 个 token 里，你打了 9 个。

## 04b · 工具调用只是生成的文字

`04b_tool_call_is_text.gif`

```
① The whole prompt goes into the LLM
② The reply comes out one token at a time: one forward pass each
③ The tokens spell a tool call. To the LLM it is just text
④ The LLM stops at <end>. Nothing has been executed yet
⑤ The harness reads the text and runs the tool on your machine
⑥ The result is added to the prompt, ready for the next LLM call
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | ① The whole prompt goes into the LLM | ① 整个提示词进入 LLM |
| 3.2 s | ② The reply comes out one token at a time: one forward pass each | ② 回复一次出来一个 token：每个 token 一次前向传播 |
| 8.2 s | ③ The tokens spell a tool call. To the LLM it is just text | ③ 这些 token 拼出一个工具调用。对 LLM 来说它只是文字 |
| 11.2 s | ④ The LLM stops at \<end\>. Nothing has been executed yet | ④ LLM 在 \<end\> 处停止。此时什么都还没有执行 |
| 14.0 s | ⑤ The harness reads the text and runs the tool on your machine | ⑤ harness 读取这段文字，在你的机器上运行工具 |
| 18.0 s | ⑥ The result is added to the prompt, ready for the next LLM call | ⑥ 结果被加入提示词，准备下一次调用 LLM |

画面上的其他文字：

```
24 tokens, 24 forward passes. Then the LLM is finished.
No file was read. No command was run.
The LLM writes. The harness acts.
```

中文：24 个 token，24 次前向传播。然后 LLM 就结束了。没有读取任何文件，没有运行任何命令。LLM 负责写，harness 负责做。

## 04c · 两层循环

`04c_two_loops.gif`

```
① The harness builds the prompt and calls the LLM
② Inside the call, the generation loop writes a tool call token by token
③ The harness runs the tool and adds the result to the prompt
④ Then it calls the LLM again, sending everything so far
⑤ This repeats until the reply contains no tool call
⑥ Two loops: the harness loops over LLM calls, the LLM loops over tokens
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | ① The harness builds the prompt and calls the LLM | ① harness 拼好提示词，调用 LLM |
| 3.4 s | ② Inside the call, the generation loop writes a tool call token by token | ② 在这次调用内部，生成循环逐个 token 写出一个工具调用 |
| 5.6 s | ③ The harness runs the tool and adds the result to the prompt | ③ harness 运行工具，把结果加入提示词 |
| 8.0 s | ④ Then it calls the LLM again, sending everything so far | ④ 然后再次调用 LLM，把到目前为止的全部内容发过去 |
| 11.6 s | ⑤ This repeats until the reply contains no tool call | ⑤ 如此重复，直到回复里不再包含工具调用 |
| 18.4 s | ⑥ Two loops: the harness loops over LLM calls, the LLM loops over tokens | ⑥ 两层循环：harness 在 LLM 调用上循环，LLM 在 token 上循环 |

画面上的其他文字：

```
OUTER LOOP · run by the harness · 4 rounds here
INNER LOOP · inside every call · one token per forward pass
Agent = a program calling the LLM in a loop
The LLM never changes and never acts. It only receives a longer prompt each time.
```

中文：外层循环，由 harness 执行，这里是 4 轮。内层循环，在每一次调用内部，每次前向传播一个 token。Agent = 一个在循环里调用 LLM 的程序。LLM 从不改变，也从不行动，它只是每次收到一个更长的提示词。

## 04d · Agent Loop

`04d_agent_loop.gif`

**这一页底部没有说明文字。** 画面是靠左边的环、左下的伪代码和右边的上下文面板来讲的。

如果想让这一页和其他页保持一致，下面是我按画面内容拟的几条，**不是动画里的原文**：

```
Think: the LLM reads the context and decides the next step
Act: the harness runs the tool the model asked for
Observe: the tool result is appended to the context
Repeat until the model replies without a tool call
```

| 英文（我拟的） | 中文 |
|---|---|
| Think: the LLM reads the context and decides the next step | 思考：LLM 读取上下文，决定下一步 |
| Act: the harness runs the tool the model asked for | 行动：harness 执行模型请求的工具 |
| Observe: the tool result is appended to the context | 观察：工具结果追加到上下文 |
| Repeat until the model replies without a tool call | 重复，直到模型的回复不再包含工具调用 |

画面上原有的文字可以直接引用的有两处：上下文面板的标题 `CONTEXT (grows with every step)`（上下文，每一步都在增长），以及退出时的标注 `no tool call → Answer ✓`。

## 05 · Tool Calling

`05_tool_calling.gif`

```
① Tool definitions (name, description, JSON schema) sit in the context
The user asks a question
② The model answers with a structured tool_use block
③ The harness parses it and actually runs the tool
④ The result is appended to the context as a new message
⑤ The model continues, now with real data
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.9 s | ① Tool definitions (name, description, JSON schema) sit in the context | ① 工具定义（名称、说明、JSON schema）位于上下文中 |
| 4.0 s | The user asks a question | 用户提出问题 |
| 6.2 s | ② The model answers with a structured tool_use block | ② 模型用一个结构化的 tool_use 块作答 |
| 9.4 s | ③ The harness parses it and actually runs the tool | ③ harness 解析它，并真正运行工具 |
| 13.6 s | ④ The result is appended to the context as a new message | ④ 结果作为一条新消息追加到上下文 |
| 16.6 s | ⑤ The model continues, now with real data | ⑤ 模型继续回答，这次有了真实数据 |

这一页最后在右下角还有一个深色框（不在底部说明条里），是全页的结论：

```
The model never executes anything, it only writes structured text.
```

中文：模型从不执行任何东西，它只是写出结构化的文本。

## 06 · RAG

`06_rag.gif`

```
Indexing: split your documents into chunks
Embed every chunk and store the vectors in a vector database
Query: embed the question into the same vector space
Retrieve the k most similar chunks
Insert the retrieved chunks into the prompt
The answer is grounded in your documents, with no retraining
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | Indexing: split your documents into chunks | 建索引：把文档切分成块 |
| 3.4 s | Embed every chunk and store the vectors in a vector database | 把每个块向量化，存入向量数据库 |
| 6.8 s | Query: embed the question into the same vector space | 查询：把问题嵌入同一个向量空间 |
| 9.6 s | Retrieve the k most similar chunks | 检索出最相似的 k 个块 |
| 11.4 s | Insert the retrieved chunks into the prompt | 把检索到的块插入 prompt |
| 14.4 s | The answer is grounded in your documents, with no retraining | 回答以你的文档为依据，无需重新训练 |

## 07a · MCP（为什么需要）

`07a_mcp_why.gif`

```
Without a standard: every app needs its own integration for every system
MCP: one open protocol. Build a server once, use it from any client
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | Without a standard: every app needs its own integration for every system | 没有标准时：每个应用都要为每个系统单独做集成 |
| 4.2 s | MCP: one open protocol. Build a server once, use it from any client | MCP：一个开放协议。server 只需构建一次，任何 client 都能使用 |

## 07b · MCP（怎么工作）

`07b_mcp_how.gif`

```
① Connect: client and server negotiate capabilities
② Discover: tools/list puts the tool schemas into the model's context
③ Call: the model picks a tool → tools/call → the result flows back
Transport: stdio (local process) or HTTP (remote server)
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.7 s | ① Connect: client and server negotiate capabilities | ① 连接：client 与 server 协商各自的能力 |
| 3.4 s | ② Discover: tools/list puts the tool schemas into the model's context | ② 发现：tools/list 把工具的 schema 放进模型的上下文 |
| 7.0 s | ③ Call: the model picks a tool → tools/call → the result flows back | ③ 调用：模型选择工具 → tools/call → 结果返回 |
| 13.1 s | Transport: stdio (local process) or HTTP (remote server) | 传输方式：stdio（本地进程）或 HTTP（远程服务器） |

## 08 · Skills

`08_skills.gif`

```
Level 1: at startup only each skill's name + description is loaded
The model matches the task against the skill descriptions
Level 2: the full SKILL.md is read only when it is needed
Level 3: scripts run via tools; only their output enters the context
Many skills installed, minimal context cost
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | Level 1: at startup only each skill's name + description is loaded | 第 1 级：启动时只加载每个 skill 的名称和简介 |
| 4.8 s | The model matches the task against the skill descriptions | 模型把任务与各个 skill 的简介进行匹配 |
| 7.7 s | Level 2: the full SKILL.md is read only when it is needed | 第 2 级：只有需要时才读取完整的 SKILL.md |
| 10.2 s | Level 3: scripts run via tools; only their output enters the context | 第 3 级：脚本通过工具运行，只有输出进入上下文 |
| 15.3 s | Many skills installed, minimal context cost | 安装很多 skill，上下文开销却很小 |

## 09 · Context Engineering

`09_context_engineering.gif`

```
Everything the model sees competes for one finite window
More tokens ≠ better: irrelevant tokens dilute attention
Compaction: summarise old turns, free the space
Sub-agents: explore in a separate context, return only the result
Goal: the smallest set of high-signal tokens for the task
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.9 s | Everything the model sees competes for one finite window | 模型看到的一切都在争夺同一个有限的窗口 |
| 7.5 s | More tokens ≠ better: irrelevant tokens dilute attention | token 更多 ≠ 更好：无关的 token 会稀释注意力 |
| 10.3 s | Compaction: summarise old turns, free the space | 压缩：总结旧的对话轮次，释放空间 |
| 13.8 s | Sub-agents: explore in a separate context, return only the result | 子 Agent：在独立的上下文中探索，只返回结果 |
| 19.4 s | Goal: the smallest set of high-signal tokens for the task | 目标：为任务提供数量最少、信息量最高的 token |

## 10a · /model

`10a_model.gif`

```
Model = which weights compute each step of the generation loop
Bigger model: more compute per token, so fewer tokens per second
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.8 s | Model = which weights compute each step of the generation loop | 模型 = 由哪一套权重来计算生成循环的每一步 |
| 5.3 s | Bigger model: more compute per token, so fewer tokens per second | 模型越大：每个 token 的计算量越多，每秒生成的 token 越少 |

## 10b · /effort

`10b_effort.gif`

```
Effort = how much work the same model puts into one request
Higher effort → more thinking & tool calls → slower, costlier, more thorough
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 1.2 s | Effort = how much work the same model puts into one request | Effort = 同一个模型在一次请求中投入多少工作量 |
| 5.7 s | Higher effort → more thinking & tool calls → slower, costlier, more thorough | effort 越高 → 思考和工具调用越多 → 更慢、更贵、更彻底 |

## 10c · 成本公式

`10c_cost_formula.gif`

```
Two independent knobs, multiplied together
```

| 出现时间 | 英文原文 | 中文 |
|---|---|---|
| 0.4 s | Two independent knobs, multiplied together | 两个独立的旋钮，效果相乘 |

## 汇总

| GIF | 说明条数 |
|---|---|
| 01_tokenization | 4 |
| 02a_embedding_lookup | 2 |
| 02b_embedding_space | 2 |
| 02c_whole_path | 7 |
| 02d_vectors_into_transformer | 7 |
| 02e_one_network_per_token | 5 |
| 02f_new_token_adds_column | 6 |
| 03_generation_loop | 6 |
| 04a_one_big_prompt | 6 |
| 04b_tool_call_is_text | 6 |
| 04c_two_loops | 6 |
| 04d_agent_loop | 0（底部无说明） |
| 05_tool_calling | 6 |
| 06_rag | 6 |
| 07a_mcp_why | 2 |
| 07b_mcp_how | 4 |
| 08_skills | 5 |
| 09_context_engineering | 5 |
| 10a_model | 2 |
| 10b_effort | 2 |
| 10c_cost_formula | 1 |
| **合计** | **90** |
