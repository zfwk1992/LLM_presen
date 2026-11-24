# Slide text (English, copy and paste)

One section per GIF, in presentation order. Each section has up to three blocks:

- **Steps**: the captions shown at the bottom of the animation, word for word, in order.
- **Also on screen**: other key sentences that appear in the picture, word for word.
- **Extra**: a few additional English sentences that are *not* in the animation. Use them as speaker notes or as extra text on the slide.

Everything inside the grey blocks is plain text, so it can be pasted straight into PowerPoint.

Chinese translations of the captions are in [captions.md](captions.md).

---

## 01 · Tokenization

`01_tokenization.gif`

**Steps**

```
Input: plain text
Text is split into sub-word tokens (Byte-Pair Encoding)
Each token is mapped to an integer ID from a fixed vocabulary
Common words → 1 token · rare words → several tokens
```

**Also on screen**

```
"Claude" = 1 token
"AUTOSAR" = 3 tokens
model input = [25734, 6307, 1006, 15946, 279, 47270, 3204, 946, 4295, 13]
10 tokens
Typical vocabulary: 50k–200k sub-word tokens · IDs here are illustrative
```

**Extra**

```
The model never sees letters or words. It only sees a list of integers.
Cost, context size and speed are all measured in tokens, not in words.
A leading space belongs to the token that follows it.
```

---

## 02a · Embedding: the lookup

`02a_embedding_lookup.gif`

**Steps**

```
Each token ID selects one row of a learned matrix
That row is the token's vector: a list of d numbers
```

**Also on screen**

```
Embedding matrix E: V rows (vocabulary) × d columns
x = E[4295] ∈ ℝᵈ
d = thousands of dimensions, learned during training
```

**Extra**

```
An embedding is a table lookup, not a calculation.
The numbers are not designed by people. They are learned during training.
```

---

## 02b · Embedding: the vector space

`02b_embedding_space.gif`

**Steps**

```
Training places tokens with similar meaning close together
Similarity = angle between vectors (cosine similarity)
```

**Also on screen**

```
cos θ = a · b / (‖a‖ ‖b‖)
CAN ↔ LIN   0.97   similar
CAN ↔ cat   0.01   unrelated
Direction encodes meaning: small angle → related concepts

Not a step in the pipeline
This is not computed before the vectors go in.
It only shows what training produced.
The vectors go straight into the network.
```

**Extra**

```
Nobody told the model that CAN and LIN belong together. It follows from learning to predict the next token.
The real space has thousands of dimensions. The 2-D picture is only a projection.
Once training is finished, this space is fixed.
```

---

## 02c · The whole path

`02c_whole_path.gif`

**Steps**

```
① The input is a list of tokens; each token has an ID
② Each ID is looked up: n tokens become n vectors
③ All n vectors go in together: one forward pass, not token by token
④ Each output vector predicts the token after it: only the last is new
⑤ That one vector is matched against every token: one score each
⑥ One token is picked and appended to the input
⑦ Next round: n + 1 vectors, one more forward pass. That is the loop
```

**Also on screen**

```
all together, straight in
forward pass #1 · whole input at once
same weights every round
matched against every token: 1 output vector → one score per token
… one row for each of the ~100,000 tokens
appended to the input
Vectors in → probabilities out → one token → repeat
One forward pass per generated token. The prompt goes in all at once, not token by token.
Cosine similarity is not a step on this path: it only describes the vector space.
```

**Extra**

```
The network receives all token vectors at the same time.
It returns one vector per position. Only the last one is used to predict the next token.
That vector is not a token. It is compared with every token in the vocabulary to get a probability for each.
The number of forward passes depends on how many tokens are generated, not on how long the prompt is.
```

---

## 02d · Inside the Transformer

`02d_vectors_into_transformer.gif`

**Steps**

```
① Each token ID is looked up: one vector per token
② Position is added, so the model knows the word order
③ Attention: each vector pulls in information from earlier tokens
④ MLP: then every vector is transformed on its own
⑤ Repeat for N layers: same shape, richer meaning
⑥ The last vector is scored against every token in the vocabulary
One forward pass, done. Next: the generation loop
```

**Also on screen**

```
5 tokens → 5 vectors
each vector is a list of d numbers (thousands)
nothing is compared yet: just a table lookup
Order matters: "ECU reads CAN" ≠ "CAN reads ECU"
Where is similarity used?
Inside attention: the weight between two tokens is a dot product of their vectors (after learned projections).
It decides how much ·CAN reads from ·ECU.
shape never changes: n vectors × d numbers
No similarity step in between: vectors go straight in.
```

**Extra**

```
Attention is where tokens exchange information. The MLP works on each token separately.
A token can only read the tokens before it, never the ones after it.
After many layers the vector for "CAN" means "the CAN in this sentence", not just the word.
```

---

## 02e · One network, copied for every token

`02e_one_network_per_token.gif`

**Steps**

```
① One token: its vector of d numbers goes through one small network
② Five tokens: the same network is used five times, at the same time
③ Attention links the copies: each token reads the ones before it
④ Attention + MLP is one layer. All columns pass layer after layer
⑤ The last column has seen everything: its output gives the next token
```

**Also on screen**

```
Width = d: the size of one vector, not the number of tokens
Attention = the links: each token reads the tokens before it; earlier tokens never read later ones
one set of weights (for this layer): stored once, used in every column
5 tokens → 5 columns, no extra weights
Layer by layer: every column passes layer 1, then every column passes layer 2, …
One set of weights. One column per token.
```

**Extra**

```
The network has no fixed number of input slots. Nothing is padded with zeros.
What is fixed is the width d and the weights. What varies is the number of columns.
More tokens mean more columns and more computation, but never more weights.
```

---

## 02f · A new token adds a column

`02f_new_token_adds_column.gif`

**Steps**

```
① The prompt: 5 tokens, 5 columns, all computed in one pass
② The last column gives the next token
③ The new token becomes column 6: only this column is new work
④ It reads the saved results of the columns before it
⑤ Every new token adds one column: more to read, same weights
⑥ Longer context costs more per step; the network never changes
```

**Also on screen**

```
This forward pass
tokens in context          5 → 6 → 7
columns computed now       5 → 1 → 1
columns read from memory   0 → 5 → 6
weights                    same

Longer context: every new column has more columns to read, so each step costs a little more
New token = new column. The weights stay the same.
```

**Extra**

```
The prompt is processed in parallel. Generated tokens are added one at a time.
Earlier columns do not change when a token is added, so their results are saved and reused.
This is why reading a long prompt is fast and writing a long answer is slow.
```

---

## 03 · Generation loop

`03_generation_loop.gif`

**Steps**

```
① The whole context goes through the network: one forward pass
② Output: a probability for every token in the vocabulary
③ Pick one token and append it to the context
Sampling: not always the most likely token (temperature T)
④ Repeat: each new token becomes part of the next input
Autoregressive: one token per step, until <end> or max_tokens
```

**Also on screen**

```
Transformer · fixed weights
Next-token probability: p = softmax(z / T)
… every other token in the vocabulary
```

**Extra**

```
The model does not plan the whole sentence. It decides one token at a time.
The weights never change while you chat. The model "remembers" only what is still in the context.
The same question can give different answers, because each token is sampled.
The answer ends when the model produces the end token.
```

---

## 04a–04e · One example in five parts

These five pages follow one request through the agent: `How do we integrate DCM into this project?`
Each page shows the request in the top right corner and "PART n OF 5" in the top left.

---

## 04a · Call 1: what the LLM receives

`04a_one_big_prompt.gif`

**Steps**

```
① You type one short message
② The harness adds the rest: system prompt, tools, CLAUDE.md, skill list
③ Everything is joined into one long token sequence
④ That whole sequence goes into the LLM at once
⑤ Skills: only the one-line descriptions are in it, not the full text
⑥ The context window is the prompt: you typed a tiny part of it
```

**Also on screen**

```
System prompt      written by Claude Code: how to behave             3,200 tokens
Tool definitions   Read, Grep, Bash, Edit, Skill, MCP tools …        9,500 tokens
CLAUDE.md          your project notes, loaded every session          1,400 tokens
Skill list         one line per skill, e.g. dcm-integration            600 tokens
Your message       "How do we integrate DCM into this project?"         10 tokens

All 14,710 tokens become vectors and go in together: one forward pass
The LLM sees tokens. It has no idea which part you typed.
dcm-integration: only its one-line description is in here.
The full SKILL.md is added later, if the model decides the task needs it.
The context window is the prompt. You typed 10 of its 14,710 tokens.
numbers are illustrative
```

**Extra**

```
What you type is only the last few tokens of a much longer prompt.
The harness does not choose anything here. It always sends the same fixed parts.
All skill descriptions are listed. Picking the right one is the model's job.
```

---

## 04b · Call 1: what the LLM returns

`04b_tool_call_is_text.gif`

**Steps**

```
① The whole prompt goes into the LLM
② The reply comes out one token at a time: one forward pass each
③ The tokens spell a tool call. To the LLM it is just text
④ The LLM stops at <end>. Nothing has been executed yet
⑤ The harness reads the text and runs the tool on your machine
⑥ The result is added to the prompt, ready for the next LLM call
```

**Also on screen**

```
{"type": "tool_use", "name": "Skill", "input": {"skill": "dcm-integration"}}
Read as text, it says: use the tool "Skill" with skill = "dcm-integration"
one pass = one token
each new token is appended, then the next pass runs
24 tokens, 24 forward passes. Then the LLM is finished.
No file was read. No command was run.
Harness (Claude Code): an ordinary program, not a model
parses the text · checks permission · then runs the tool
Tool: Skill reads dcm-integration/SKILL.md from your disk
tool_result: the SKILL.md text · about 2,100 tokens
appended to the prompt → the harness calls the LLM again
The LLM writes. The harness acts.
```

**Extra**

```
"Calling a tool" means the model wrote a short piece of text in an agreed format.
Reading the file, running the command and checking permissions are done by the program around the model.
The result comes back as more text in the prompt.
```

---

## 04c · Call 2: everything is sent again

`04c_second_call.gif`

**Steps**

```
① Call 2 starts: the harness sends everything again, from the top
② New at the end: what the LLM wrote, and the full SKILL.md text
③ Now the LLM can read your workflow. It starts with step 1
④ Again it only writes a request: run the extraction script
⑤ The harness runs the script; the result joins the prompt
⑥ Call 3 will receive all of this: the prompt only ever grows
```

**Also on screen**

```
THE PROMPT FOR CALL 2 (one sequence, in this order)

SYSTEM              system prompt · tool definitions · CLAUDE.md · skill list   14,700 tokens
USER                How do we integrate DCM into this project?
                    → identical to call 1 (read from the cache)
ASSISTANT           tool_use  Skill("dcm-integration")
USER · TOOL_RESULT  SKILL.md   2,100 tokens
                    1. Run scripts/extract_dcm_config.py on the EcuC ARXML
                    2. Look up the requirements in the Dcm specification
                    3. Read docs/architecture.md
                    4. Check the Os and Rte definitions
                    5. Then propose the changes
                    → new in call 2: what the LLM wrote in call 1 + the skill's full text
ASSISTANT           tool_use  Bash("…extract_dcm_config.py…")
USER · TOOL_RESULT  3 protocols · 14 UDS services · 2 PDUs to route
                    → added for call 3

THE LLM'S REPLY
"The skill says to start with the EcuC values."
tool_use  Bash("python scripts/extract_dcm_config.py config/EcuC.arxml")
still only text: nothing has run yet

16,834 tokens sent in call 2  →  17,765 tokens will be sent in call 3
Every call: send everything so far → the LLM writes one reply → the harness runs it → append
Your workflow is followed because the LLM reads it in the prompt, not because the harness executes it.
```

**Extra**

```
The model has no memory between calls. It knows what happened only because the harness sends the whole history again.
Your workflow in SKILL.md becomes visible to the model only now, in the second call.
The order inside the prompt is fixed: unchanging parts first, the newest result last.
```

---

## 04d · The whole session, call by call

`04d_agent_at_work.gif`

**Steps**

```
① One request. Project notes and skill descriptions are already in the prompt
② Call 1: the model sees a matching skill and asks to load it
③ Call 2: following your workflow, it asks to run the extraction script
④ Calls 3 and 4: it asks the spec, then reads the repo's own rules
⑤ Call 5: it checks Os and Rte and finds Dcm is not connected yet
⑥ Call 6: no tool call this time. It writes the plan and the loop ends
```

**Also on screen**

```
USER  How do we integrate DCM into this project?

LLM CALL 1  "A skill matches this task. Load it first."
            asks for  Skill("dcm-integration")
            harness ran it: SKILL.md loaded: your 5-step workflow   +2.1k
LLM CALL 2  "Workflow step 1: get the EcuC values."
            asks for  Bash("scripts/extract_dcm_config.py config/EcuC.arxml")
            harness ran it: 3 protocols, 14 UDS services, 2 PDUs   +0.9k
LLM CALL 3  "Step 2: what does the standard require?"
            asks for  search_spec("Dcm integration PduR ComM")
            harness ran it: 3 passages from SWS_Dcm, out of 600 pages   +1.8k
LLM CALL 4  "Step 3: the rules of this repository."
            asks for  Read("docs/architecture.md")
            harness ran it: 180 lines   +2.4k
LLM CALL 5  "Step 4: is Dcm already scheduled and connected?"
            asks for  Grep("Dcm_MainFunction", "config/ rte/")
            harness ran it: no matches: no Os task, no Rte port yet   +0.6k
LLM CALL 6  "Step 5: I have enough. Write the plan."
            writes  no tool call
            1. Add Dcm_MainFunction to the 10 ms Os task   2. Route the 2 PDUs in PduR
            3. Connect the Dcm ports in the Rte   4. Regenerate   (sources: EcuC, SWS_Dcm §7)

YOUR PROJECT (on disk)
CLAUDE.md                          in the prompt
skills/dcm-integration/SKILL.md    loaded
skills/misra-check/SKILL.md        1 line in prompt
docs/AUTOSAR_SWS_Dcm.pdf           3 passages
config/EcuC.arxml                  extracted by script
docs/architecture.md               read
config/Os.arxml · rte/             searched
bsw/Dcm/                           never opened
… 214 more files                   never opened

The prompt: 14.7k → 16.8k → 17.7k → 19.5k → 21.9k → 22.5k tokens
sent again in full at every call
6 LLM calls · 5 tool runs by the harness · the model never opened a file itself
token counts are illustrative
```

**Extra**

```
At the start only the project notes and one line per skill are in the prompt. Everything else is fetched on demand.
The five steps come from your SKILL.md. The model follows them because it read them, one call at a time.
The 600-page specification never enters the prompt as a whole. Only three relevant passages do.
A script extracts the Dcm values from the large ARXML file, so only 900 tokens enter the prompt instead of the whole file.
```

---

## 04e · Two loops

`04e_two_loops.gif`

**Steps**

```
① The harness builds the prompt and calls the LLM
② Inside the call, the generation loop writes a tool call token by token
③ The harness runs the tool and adds the result to the prompt
④ Then it calls the LLM again, sending everything so far
⑤ This repeats until the reply contains no tool call
⑥ Two loops: the harness loops over LLM calls, the LLM loops over tokens
```

**Also on screen**

```
HARNESS: Claude Code, a program
LLM: predicts tokens, nothing else

LLM call #1   14.7k tokens in   →  Skill("dcm-integration")      →  run Skill: SKILL.md, +2.1k
LLM call #2   16.8k tokens in   →  Bash("extract_dcm_config")    →  run Bash: script output, +0.9k
LLM call #3   17.7k tokens in   →  search_spec("Dcm …")          →  run search_spec: 3 passages, +1.8k
calls 4 and 5 follow the same pattern
LLM call #6   22.5k tokens in   →  the integration plan          →  show answer (no tool call: stop)

WHAT EACH CALL RECEIVES (every call re-sends everything so far)
OUTER LOOP · run by the harness · 6 rounds in this example
INNER LOOP · inside every call · one token per forward pass
Agent = a program calling the LLM in a loop
The LLM never changes and never acts. It only receives a longer prompt each time.
token counts are illustrative
```

**Extra**

```
An agent is not a new kind of model. It is the same model, called again and again by a program.
The model decides what to do next and when the task is finished. The harness only carries it out.
The loop ends when a reply contains no tool call.
```

---

## 04f · Agent loop (summary)

`04f_agent_loop.gif`

This animation has no caption bar at the bottom.

**Also on screen**

```
Think: LLM reasons
Act: tool call
Observe: tool result
CONTEXT (grows with every step)

while True:
    reply = llm(context)
    context += reply
    if not reply.tool_calls: break
    context += run(reply.tool_calls)

USER     Fix the failing unit test in the Com module
THINK    Run the tests to see what fails
TOOL     Bash("ctest -R Com")
RESULT   1 failed: test_Com_SendSignal
THINK    Inspect the signal packing code
TOOL     Read("Com_Send.c")
RESULT   412 lines
THINK    Byte index is off by one: fix it
TOOL     Edit("Com_Send.c", line 218)
RESULT   file updated
THINK    Verify the fix
TOOL     Bash("ctest -R Com")
RESULT   all 48 tests passed
ANSWER   Fixed off-by-one in Com_Send.c:218 · tests pass
```

**Extra**

```
Think: the LLM reads the context and decides the next step
Act: the harness runs the tool the model asked for
Observe: the tool result is appended to the context
Repeat until the model replies without a tool call
Nobody scripted these four steps. The model chose each one after seeing the previous result.
```

---

## 05 · Tool calling

`05_tool_calling.gif`

**Steps**

```
① Tool definitions (name, description, JSON schema) sit in the context
The user asks a question
② The model answers with a structured tool_use block
③ The harness parses it and actually runs the tool
④ The result is appended to the context as a new message
⑤ The model continues, now with real data
```

**Also on screen**

```
LLM: reads the context · predicts next tokens
Harness (Claude Code): parses tool_use · runs the tool · returns result
Tool: run_tests, e.g. ctest -R Com on your machine
The model never executes anything, it only writes structured text.
```

**Extra**

```
The model knows which tools exist because their descriptions are part of the prompt.
A good tool description matters as much as good interface documentation for a new colleague.
Every tool definition costs tokens in every call.
```

---

## 06 · RAG

`06_rag.gif`

**Steps**

```
Indexing: split your documents into chunks
Embed every chunk and store the vectors in a vector database
Query: embed the question into the same vector space
Retrieve the k most similar chunks
Insert the retrieved chunks into the prompt
The answer is grounded in your documents, with no retraining
```

**Also on screen**

```
INDEXING · offline
QUERY · online
top-k = 3 · highest cosine similarity
SYSTEM: Answer using only the context below. Cite sources.
Sources: chunk #12, #7
```

**Extra**

```
RAG does not change the model. It changes what is put into the prompt.
This is where cosine similarity is really computed: between the question and every chunk.
The quality of the answer depends mostly on whether the right chunks were retrieved.
```

---

## 07a · MCP: why

`07a_mcp_why.gif`

**Steps**

```
Without a standard: every app needs its own integration for every system
MCP: one open protocol. Build a server once, use it from any client
```

**Also on screen**

```
3 × 4 = 12 custom integrations
3 + 4 = 7 MCP connectors
```

**Extra**

```
M applications and N systems need M × N integrations without a standard, and M + N with one.
Think of it as USB for AI applications.
```

---

## 07b · MCP: how

`07b_mcp_how.gif`

**Steps**

```
① Connect: client and server negotiate capabilities
② Discover: tools/list puts the tool schemas into the model's context
③ Call: the model picks a tool → tools/call → the result flows back
Transport: stdio (local process) or HTTP (remote server)
```

**Also on screen**

```
HOST: Claude Code
LLM: sees tool schemas in its context
MCP client → jira · MCP client → git
Server offers: Tools · Resources · Prompts
JSON-RPC 2.0
```

**Extra**

```
The model does not know that MCP exists. It only sees more tool descriptions in its prompt.
MCP is the part between the harness and the outside system.
Every connected server adds its tool descriptions to every prompt.
```

---

## 08 · Skills

`08_skills.gif`

**Steps**

```
Level 1: at startup only each skill's name + description is loaded
The model matches the task against the skill descriptions
Level 2: the full SKILL.md is read only when it is needed
Level 3: scripts run via tools; only their output enters the context
Many skills installed, minimal context cost
```

**Also on screen**

```
L1  name + description     always loaded (~100 tokens each)
L2  SKILL.md               loaded when the task matches
L3  scripts & resources    run / read only when needed
the script's code never enters the context, only its output
```

**Extra**

```
A skill is a folder: a document that explains how to do a task, plus optional scripts.
MCP gives the agent access to systems. Skills tell it how to do a kind of work.
The one-line description decides whether the skill is used, so it must be written carefully.
```

---

## 09 · Context engineering

`09_context_engineering.gif`

**Steps**

```
Everything the model sees competes for one finite window
More tokens ≠ better: irrelevant tokens dilute attention
Compaction: summarise old turns, free the space
Sub-agents: explore in a separate context, return only the result
Goal: the smallest set of high-signal tokens for the task
```

**Also on screen**

```
MAIN AGENT CONTEXT WINDOW · e.g. 200K tokens
the original task gets lost in the noise
long, noisy context → attention spread thin ("context rot")
decisions, open tasks and key facts kept: details dropped
SUB-AGENT CONTEXT · fresh & isolated

Select     load only what is relevant, just in time (tools, skills, RAG)
Compress   summarise / compact long histories
Isolate    delegate noisy exploration to sub-agents
Persist    notes & CLAUDE.md live outside the window
```

**Extra**

```
The context window is a workbench, not a warehouse.
Tool results, not the conversation, are usually what fills it.
Every extra token is re-read on every step of the agent loop.
```

---

## 10a · /model

`10a_model.gif`

**Steps**

```
Model = which weights compute each step of the generation loop
Bigger model: more compute per token, so fewer tokens per second
```

**Also on screen**

```
Haiku: fastest · cheapest
Sonnet: balanced
Opus: most capable
Same generation loop, different weights.
compute per token ≈ 2 × number of parameters (FLOPs)
bigger network → more knowledge & reasoning per step, but slower and pricier per token · sizes not published
```

**Extra**

```
Changing the model changes the cost of every single token.
The picture shows three models as examples. The same rule holds for the rest of the line-up.
```

---

## 10b · /effort

`10b_effort.gif`

**Steps**

```
Effort = how much work the same model puts into one request
Higher effort → more thinking & tool calls → slower, costlier, more thorough
```

**Also on screen**

```
Same model · same task · different effort level
low · medium · high · xhigh · max
thinking · tool calls (+ results) · answer text
Effort scales ALL output tokens: thinking, tool calls and text. Low = fewer, terser tool calls.
(illustrative)
```

**Extra**

```
Effort does not make the model smarter. It makes the same model do more work.
Thinking is generated token by token like everything else, so it costs time and money.
```

---

## 10c · Cost formula

`10c_cost_formula.gif`

**Steps**

```
Two independent knobs, multiplied together
```

**Also on screen**

```
Total cost & latency ≈ output tokens × compute per token
output tokens: set by /effort, how many loop iterations
compute per token: set by /model, cost of each iteration
Hard, ambiguous, multi-step task → stronger model and/or higher effort
Small, well-defined edit → smaller model, lower effort: fast & cheap
Plus input tokens: in an agent loop the growing context is re-read at every step (prompt caching makes this cheaper).
```

**Extra**

```
Ask two questions: how capable does the model need to be, and how carefully does it need to work?
In agent tasks the input tokens often cost more than the output, because the prompt is sent again at every step.
```

---

## 10d · Same request, three models

`10d_same_task_models.gif`

**Steps**

```
① Same request, same harness, same skill: only the model differs
② Each call takes longer with a bigger model: more compute per token
③ The smaller model is done first, but took a wrong turn and missed a step
④ The larger models follow the whole workflow; the largest notices more
⑤ The token counts are about the same. The price per token is not
⑥ Model = how good each decision is, and what each token costs
```

**Also on screen**

```
Smaller model (e.g. Haiku)    5 s per call · 7 calls · done in 35 s
    RESULT  plan with 3 of 4 steps · missed the Rte ports · 1 call wasted on the wrong file      COST ≈ 1×
Mid-size model (e.g. Sonnet)  12 s per call · 6 calls · done in 72 s
    RESULT  complete plan, 4 steps · followed all 5 workflow steps                               COST ≈ 3×
Larger model (e.g. Opus)      20 s per call · 6 calls · done in 120 s
    RESULT  complete plan, 4 steps · also flags a ComM dependency the workflow did not mention   COST ≈ 5×

Tokens processed in every lane: about 113k input + under 1k output
(the prompt is re-sent at every call, so input dominates)
The model sets the price and speed of every token, and how good each decision is. It does not change the loop.
timings, costs and outcomes are illustrative
```

**Extra**

```
All three models receive the same prompts and use the same tools. The agent loop is identical.
The cost difference comes almost entirely from the price per token, not from the number of tokens.
What you buy with a larger model is better judgement at every step: fewer wrong turns, fewer things missed.
In this task the model reads about a hundred times more than it writes.
```

---

## 10e · Same request, same model, four effort levels

`10e_same_task_effort.gif`

**Steps**

```
① Same request, same model: only the effort level differs
② Low: few steps and little thinking. It skips the spec lookup
③ Medium: the session you just saw, all five workflow steps
④ High and max: more thinking, more checks, more calls
⑤ Tokens grow faster than calls: every call re-sends a longer prompt
⑥ Effort = how much work, not how smart. Pick it to fit the task
```

**Also on screen**

```
low      4 LLM calls   loads the skill, runs the script, checks Os/Rte. Skips the spec lookup            68k input tokens   cost ≈ 0.6×
medium   6 LLM calls   the session you just saw: all five workflow steps                                113k input tokens   cost ≈ 1×
high     9 LLM calls   also reads the PduR and ComM config and re-checks the spec                       216k input tokens   cost ≈ 1.9×
max     14 LLM calls   also reads the Dcm sources, verifies each step, lists open questions             504k input tokens   cost ≈ 4.5×

thinking · a tool call (then the harness runs it) · the final answer
From medium to max: calls × 2.3, tokens × 4.5.
Each extra call re-sends everything gathered so far, so later calls are the expensive ones.
Effort changes how many rounds and how much thinking. It does not change the model.
A plan for an unfamiliar integration: medium or high. A one-line fix: low.
all counts are illustrative
```

**Extra**

```
Effort does not make the model more capable. It makes the same model think longer and check more.
Higher effort means more rounds of the agent loop, not only longer thinking.
Cost grows faster than the number of calls, because every later call carries everything collected before it.
Model: how capable must it be?  Effort: how carefully must it work?
```
