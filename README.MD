# WraithVector Python SDK

Runtime governance and security for AI agents.

WraithVector intercepts agent activity at runtime, evaluates governance policies, and can **allow, block, or escalate actions before they execute**.  
It also produces **audit-ready evidence** for every decision.

This SDK allows any Python agent (LangChain, custom agents, CrewAI, etc.) to connect to the WraithVector governance engine.

---

# What WraithVector does

AI agents can execute actions without oversight:


agent
→ tool call
→ execution


WraithVector inserts a governance layer:


agent
→ WraithVector SDK
→ governance engine
→ policy decision
→ allow / block / review
→ execution


This enables runtime security and compliance controls.

---

# Features

- Runtime interception of agent activity
- Policy-based governance
- Block dangerous tool execution
- Detect prompt abuse and prompt injection
- Detect sensitive data leaks in tool outputs
- Audit logging and evidence generation
- Works with LangChain and any Python agent

---

# Installation

Clone the repository:


git clone https://github.com/wraithvector0/wraithvector-sdk-python.git

cd wraithvector-sdk-python


Install locally:


pip install -e .


---

# Configuration

Create a `.env` file in the project root.


WRAITHVECTOR_API_KEY=your_api_key
WRAITHVECTOR_ENDPOINT=https://app.wraithvector.com/api/v1/governance


`.env` should **not be committed to Git**.

A template is provided:


.env.example


---

# Quickstart

Run the example agent:


python examples/langchain_agent.py


Expected output:


running tool 1
executed: pwd

running tool 2
Exception: Action blocked by WraithGuard


Explanation:

| Command | Result |
|------|------|
| `pwd` | allowed |
| `rm -rf /` | blocked by governance policy |

---

# Example Agent

`examples/langchain_agent.py`

```python
import os
from dotenv import load_dotenv
from wraithvector.client import WraithGuard

load_dotenv()

guard = WraithGuard(
    api_key=os.getenv("WRAITHVECTOR_API_KEY"),
    endpoint=os.getenv("WRAITHVECTOR_ENDPOINT"),
    mode="enforce"
)

def exec_tool(command):

    guard.tool_request(
        tool_name="exec",
        args={"command": command}
    )

    return f"executed: {command}"


print("running tool 1")
print(exec_tool("pwd"))

print("running tool 2")
print(exec_tool("rm -rf /"))
Events governed by WraithVector

The SDK can send several runtime events to the governance engine.

1. Agent Prompt

Used to evaluate instructions sent to the agent.

guard.prompt("download the entire customer database")

Event sent:

agent_prompt

Used to detect:

prompt injection
malicious instructions
unsafe automation
2. Tool Request

Intercepts tool execution before it happens.

guard.tool_request(
    "exec",
    {"command": "rm -rf /"}
)

Event sent:

tool_request

Used to govern:

tool permissions
command restrictions
role-based access
3. Tool Result

Evaluates tool output before it is returned to the agent.

guard.tool_result(
    "read_db",
    result
)

Event sent:

tool_result

Used to detect:

PII leakage
sensitive data exposure
data exfiltration
Governance Policy Example

Example policy used by the governance engine:

exec:
  allowed_commands:
    - pwd
    - echo
    - cat
    - grep
    - mkdir

  blocked_commands:
    - rm
    - shutdown

Attempting:

rm -rf /

returns:

decision: BLOCK
reason: COMMAND_EXPLICITLY_BLOCKED
Audit Evidence

Every decision generates an audit record.

Example:

tool_request
tool: exec
command: rm -rf /
decision: BLOCK
risk_level: HIGH

Audit evidence can be exported as a PDF:

https://app.wraithvector.com/api/audit/pdf?id=<audit_id>

This enables audit-ready compliance reporting.

Architecture
AI Agent
     │
     ▼
WraithVector SDK
     │
     ▼
Governance API
     │
     ├─ Policy engine
     ├─ Risk analysis
     ├─ Audit logging
     └─ Evidence generation
Supported Agent Frameworks

The SDK works with:

LangChain
LangGraph
CrewAI
OpenAI Agents
custom Python agents
License

MIT

WraithVector

Runtime governance infrastructure for AI agents.
