import os
from dotenv import load_dotenv
from wraithvector.client import WraithGuard


# cargar variables .env
load_dotenv()

print("API KEY =", os.getenv("WRAITHVECTOR_API_KEY"))
print("ENDPOINT =", os.getenv("WRAITHVECTOR_ENDPOINT"))


guard = WraithGuard(
    api_key="wv642a807c-83b8-47ba-91ca-9792d1ff5023
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