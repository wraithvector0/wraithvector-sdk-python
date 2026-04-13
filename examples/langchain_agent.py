import os
from dotenv import load_dotenv
from wraithvector.client import WraithGuard


# cargar variables .env
load_dotenv()


guard = WraithGuard(
    api_key=os.getenv("WRAITHVECTOR_API_KEY"),
    endpoint=os.getenv("WRAITHVECTOR_ENDPOINT"),
    mode="enforce"
)


def exec_tool(command: str):

    guard.tool_request(
        tool_name="exec",
        args={"command": command}
    )

    return f"executed: {command}"


print("running tool 1")
print(exec_tool("pwd"))

print("running tool 2")
print(exec_tool("rm -rf /"))