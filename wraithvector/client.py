import os
import requests


class WraithGuard:

    def __init__(self, api_key=None, endpoint=None, mode="observe"):
        self.api_key = api_key or os.getenv("WRAITHVECTOR_API_KEY")
        self.endpoint = endpoint or os.getenv("WRAITHVECTOR_ENDPOINT")
        self.mode = mode


    def send_event(self, event_payload):

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        print("WraithVector endpoint:", self.endpoint)

        try:
            r = requests.post(
                self.endpoint,
                json=event_payload,
                headers=headers,
                timeout=0.5
            )

        except requests.exceptions.RequestException as e:
            if self.mode == "enforce":
                raise Exception (f"Governance unavailible: {e}")
                
            return None


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
