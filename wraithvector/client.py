import os
import requests
import inspect
import uuid

class WraithGuard:

    def __init__(
        self,
        api_key=None,  #ponemos none para manterner backward compatiblility
        endpoint=None,
        mode="observe",
        agent_id=None,
        agent_role=None,
        agent_version="v1",
        session_id=None,
    ):

        self.api_key = api_key or os.getenv("WRAITHVECTOR_API_KEY")
        self.endpoint = endpoint or os.getenv("WRAITHVECTOR_ENDPOINT")

        self.mode = mode

        self.agent_id = agent_id
        self.agent_role = agent_role
        self.agent_version = agent_version
        self.session_id=session_id or str(uuid.uuid4())

    





    def send_event(self, event_payload):

        print("MODE:", self.mode)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",

            "x-agent-id": self.agent_id or "unknown-agent",
            "x-agent-role": self.agent_role or "unknown-role",
            "x-agent-version": self.agent_version or "v1",
            "x-agent-session-id": self.session_id or "unknown-session"

        }

        print("WraithVector endpoint:", self.endpoint)

        try:
            r = requests.post(
                self.endpoint,
                json=event_payload,
                headers=headers,
                timeout=5
            )

        except requests.exceptions.RequestException as e:
            if self.mode == "enforce":
                raise Exception (f"Governance unavailible: {e}")
                
            return None

        


        print("STATUS", r.status_code)
        print("RESPONSE", r.text)

        if r.status_code >= 400 and self.mode == "enforce":
            raise Exception(
                
            f"Governance failed: {r.status_code}")


        try:
            return r.json()
        except:
            return None


    def prompt(self, text):

        payload = {
            "event": "agent_prompt",
            "text": text
        }

        return self.send_event(payload)


    def tool_request(self, tool_name, args, agent_role="default"):

        payload = {
            "event": "tool_request",
            "tool_name": tool_name,
            "args": args,
            "agent_role": agent_role
        }

        return self.send_event(payload)


    def tool_result(self, tool_name, result, agent_role="default"):

        payload = {
            "event": "tool_result",
            "tool_name": tool_name,
            "result": result,
            "agent_role": agent_role
        }

        return self.send_event(payload)
