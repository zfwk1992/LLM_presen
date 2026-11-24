# 07 · MCP（Model Context Protocol）

这个主题有两页。

![MCP why](../llm_agent_animations_single_page/07a_mcp_why.gif)

![MCP how](../llm_agent_animations_single_page/07b_mcp_how.gif)

> **一句话**：MCP 是一个开放协议，规定了 AI 应用和外部系统之间怎么对话。系统只需要做一次适配，所有支持 MCP 的应用都能用。

## 在演讲里的位置

05 讲了模型和 harness 之间怎么调用工具。这两页讲的是**工具从哪里来**：harness 通过 MCP 连接外部系统，把它们的能力变成模型可用的工具。第一页讲为什么需要它，第二页讲它怎么工作。

## 第一页：为什么需要（07a，6.7 s）

| 时间 | 画面 | 这时候讲什么 |
|---|---|---|
| 0–3 s | 左边 3 个应用，右边 4 个系统，红线两两相连，`3 × 4 = 12 custom integrations` | "没有标准时，每个应用要为每个系统单独写一套集成" |
| 3–5 s | 红线消失，中间出现绿色的 MCP | "中间加一层统一的协议" |
| 5–6.7 s | 绿线，`3 + 4 = 7 MCP connectors` | "每一方只需要适配一次" |

- **左边（应用）**：Claude Code、IDE assistant、Chat app
- **右边（系统）**：Jira、Confluence、Git、Build server

这是典型的 **M × N 变成 M + N** 的问题。数字小的时候差别不大（12 对 7），但规模一上来差别很大：10 个应用、50 个系统，是 500 套集成对 60 个适配。

最容易懂的类比是 **USB**：以前每种外设有自己的接口，现在设备做一个 USB 口，电脑做一个 USB 口，就都能用了。

字幕：*"MCP: one open protocol. Build a server once, use it from any client."*

## 第二页：怎么工作（07b，16.1 s）

### 画面里的角色

- **Host**（左边的大框）：Claude Code。内部有：
  - **LLM**：标注 "sees tool schemas in its context"
  - **Tools available to the model**：模型可用的工具列表，开始是空的
  - **MCP client → jira**、**MCP client → git**：每个 server 对应一个 client
- **MCP server**（右边）：Jira MCP server、Git MCP server。每个 server 提供三类东西：
  - **Tools**：`get_issue`、`search_issues` 等
  - **Resources**：files, records, schemas
  - **Prompts**：reusable templates
- **最右边**：Jira API、repo。这是 server 背后真正的系统。

### 三个步骤

| 时间 | 字幕 | 画面 | 这时候讲什么 |
|---|---|---|---|
| 0–2.5 s | ① Connect: client and server negotiate capabilities | `initialize` 标签从 client 飞向 server | "先握手，互相告知支持什么" |
| 2.5–7 s | ② Discover: tools/list puts the tool schemas into the model's context | `tools/list` 飞回，工具列表逐个填入 | "client 问 server：你有什么工具？答案进入模型的上下文" |
| 7–13.5 s | ③ Call: the model picks a tool → tools/call → the result flows back | `jira.get_issue` 高亮，`tools/call` 飞向 server，上方显示 JSON 报文，结果返回，LLM 亮起 | "模型选了一个工具，client 转发请求，结果流回来" |
| 约 14.5 s | Transport: stdio (local process) or HTTP (remote server) | — | "server 可以是本机的一个进程，也可以是远程服务" |

第 ② 步结束后，模型可用的工具列表是：

```
jira.get_issue    jira.search_issues    jira.create_issue
git.git_log       git.git_diff
```

### 报文长什么样

MCP 用的是 JSON-RPC 2.0。第 ③ 步画面上方显示的请求：

```json
{"method": "tools/call",
 "params": {"name": "get_issue",
            "arguments": {"key": "ECM-1234"}}}
```

响应：

```json
{"result": {"content": [{"type": "text",
            "text": "ECM-1234: CAN timeout…"}]}}
```

不需要让听众记住格式，只需要让他们看到：这就是普通的请求和响应，没有什么神秘的东西。

## 需要真正搞懂的概念

### Host、Client、Server

| 角色 | 是什么 | 画面里 |
|---|---|---|
| Host | 用户直接使用的 AI 应用，里面有模型 | Claude Code |
| Client | Host 内部负责和一个 server 通信的部件，一个 server 对应一个 client | MCP client → jira / git |
| Server | 把某个系统的能力按 MCP 的格式暴露出来的程序 | Jira MCP server、Git MCP server |

### Server 提供的三类东西

| 类别 | 是什么 | 谁来决定使用 |
|---|---|---|
| Tools | 可以执行的动作（查 issue、建 issue、看 diff） | 模型 |
| Resources | 可以读取的数据（文件、记录、表结构） | 应用 |
| Prompts | 预先写好的提示模板 | 用户 |

实际使用中 Tools 最常见，动画的第 ②、③ 步讲的也都是 Tools。

### MCP 和工具调用的关系

这是最需要讲清楚的一点。把 05 和这一页拼起来，一次调用的完整路径是：

```
模型 ──tool_use──▶ Harness（Host）──tools/call──▶ MCP server ──▶ Jira API
模型 ◀─tool_result─ Harness（Host）◀───result──── MCP server ◀── Jira API
```

- **左半段**是 05 讲的：模型写出 `tool_use`，harness 执行。
- **右半段**是 MCP：harness 怎么找到工具、怎么把请求转给外部系统。

**模型本身不知道 MCP 的存在。** 对它来说，来自 MCP 的工具和内置工具没有任何区别，都是上下文里的一段工具说明。

### 两种传输方式

- **stdio**：server 是本机上的一个子进程，通过标准输入输出通信。适合访问本地资源（本地 Git 仓库、本地文件）。
- **HTTP**：server 是一个网络服务。适合多人共用的远程系统（公司的 Jira）。

### 工具太多的代价

第 ② 步的字幕说 tools/list "puts the tool schemas into the model's context"。每连一个 server，它所有工具的说明都要占用上下文。连得越多，固定开销越大，模型也越难选对工具。这是 09 的话题，也是下一页 Skills 采用按需加载的原因之一。

### 安全

MCP server 是在替你访问系统，手里拿着你的凭证。只连接可信的 server；server 返回的内容对模型来说也是文本，同样有 05 里提到的提示注入风险。

## 常见误解

- **"MCP 是一种模型能力"**：不是。它是应用和系统之间的协议，模型感知不到。
- **"MCP 是 Anthropic 专有的"**：它由 Anthropic 发起，但是开放协议，其他厂商的应用也可以实现。
- **"MCP server 就是那个系统本身"**：通常不是。它是一个适配层，背后再去调用系统原有的 API（画面最右边的 Jira API、repo）。

## 听众可能会问

**Q：我们的内部系统能接吗？**
能。给它写一个 MCP server，把需要的操作定义成工具即可。写一次，所有支持 MCP 的应用都能用。

**Q：工具名为什么是 `jira.get_issue`？**
动画里的写法是为了看清工具来自哪个 server。Claude Code 里实际显示为 `mcp__jira__get_issue` 这样的形式。

**Q：和直接调用 REST API 有什么区别？**
REST API 是给程序员用的，需要读文档写代码。MCP server 是给 AI 应用用的：它自带工具说明，应用连上之后自动知道有什么可用、怎么调用。

**Q：一个应用可以连多少个 server？**
协议上没有限制，实际受上下文开销约束。

## 承上启下

- **上一页**：RAG 接入的是静态文档。
- **这两页**：MCP 接入的是活的系统。
- **下一页**：有了知识、有了系统，还缺"怎么做事的方法"。下一页讲 Skills。
- **过渡句**："MCP 让 Agent 够得着我们的系统。但'够得着'不等于'会用'。比如按我们团队的规范检查一段 C 代码，这种做事的方法放在哪里？"

## 自测

<details>
<summary>1. MCP 解决的核心问题是什么？</summary>

M 个应用和 N 个系统原本需要 M×N 套定制集成，有了统一协议后只需要 M+N 个适配。
</details>

<details>
<summary>2. 说出 MCP 连接后的三个步骤。</summary>

Connect（`initialize`，协商能力）→ Discover（`tools/list`，获取工具说明）→ Call（`tools/call`，执行并返回结果）。
</details>

<details>
<summary>3. 模型知道某个工具来自 MCP 吗？</summary>

不知道。对模型来说所有工具都是上下文里的工具说明，调用方式完全一样。MCP 是 harness 和外部系统之间的事。
</details>
