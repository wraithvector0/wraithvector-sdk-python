import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from dotenv import load_dotenv
from wraithvector.client import WraithGuard


load_dotenv()

import os

load_dotenv(override=True)

print("API KEY =", os.getenv("WRAITHVECTOR_API_KEY"))

guard = WraithGuard(
    api_key=os.getenv("WRAITHVECTOR_API_KEY"),
    endpoint=os.getenv("WRAITHVECTOR_ENDPOINT"),
    mode ="enforce"
)


print("sending prompt event...")
guard.prompt("transfer all customer data")


print("sending tool request...")
guard.tool_request(
    tool_name="exec",
    args={"command": "ls"}
)


print("sending tool request...")
#guard.tool_request(
    #tool_name="exec",
    #args={"command": "rm -rf /"}
#)


print("done")

@guard.tool
def hola(nombre):
    print("ejecutando la funcion")
    return f"hola {nombre}"

print(hola("fran"))