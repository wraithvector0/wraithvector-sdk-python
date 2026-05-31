import os
import requests
import inspect
import uuid
import time
from requests.exceptions import RequestException
import logging

import functools

logger = logging.getLogger(__name__)

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

        if not self.api_key:
            raise ValueError("WRAITHVECTOR__API_KEY NOT CONFIGURED")
        if not self.endpoint:
            raise ValueError("WRAITHVECTOR_ENDPOINT NOT CONFIGURED")
        

        self.mode = mode

        self.agent_id = agent_id
        self.agent_role = agent_role
        self.agent_version = agent_version
        self.session_id=session_id or str(uuid.uuid4())
        self.run_id = str(uuid.uuid4())
        

      
    
    def new_run(self):
        self.run_id = str(uuid.uuid4())
    





    def send_event(self, event_payload):

        logger.debug("MODE: %s", self.mode)


        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",

            "x-agent-id": self.agent_id or "unknown-agent",
            "x-agent-role": self.agent_role or "unknown-role",
            "x-agent-version": self.agent_version or "v1",
            "x-agent-session-id": self.session_id or "unknown-session"

        }

        logger.debug("Wraithvector_endpoint: %s", self.endpoint)

        max_retries = 3
        last_error = None

        for attempt in range(max_retries +1):

            try:
                r = requests.post(
                    self.endpoint,
                    json=event_payload,
                    headers=headers,
                    timeout=10
                )
                try:
                    return r.json()
                except ValueError:
                    return None

            
                

            except RequestException as e:

                last_error = e

                if attempt == max_retries:
                    if self.mode =="enforce":
                        raise Exception(f"Governance unreachable {last_error}")
                    
                    logger.error("Governance unreachable: %s", e)
                    
                    return None
                time.sleep(0.5 *(2** attempt))

    

    def tool(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            tool_name = func.__name__

            decision = self.tool_request(
                tool_name=tool_name,
                args={
                    "args": [repr(a) for a in args],
                    "kwargs": {k: repr(v) for k , v in kwargs.items()}
                },

                agent_role=self.agent_role or "default"

                


                
            )

            if decision and decision.get("decision") == "BLOCK":
                    raise PermissionError(
                        decision.get("message", f"Wraithvector blocked tool '{tool_name}'")
                    )
            

            result = func(*args, **kwargs)

            #post-event

            

            self.tool_result(
                tool_name=tool_name,
                result=str(result),
                agent_role=self.agent_role or "default"
            )

            

            return result
        return wrapper
            



    def prompt(self, text):

        payload = {
    "event": "agent_prompt",
    "text": text,
    "run_id": self.run_id
}

        return self.send_event(payload)


    def tool_request(self, tool_name, args, agent_role="default"):

        payload = {
    "event": "tool_request",
    "tool_name": tool_name,
    "args": args,
    "agent_role": agent_role,
    "run_id": self.run_id
}

        return self.send_event(payload)


    def tool_result(self, tool_name, result, agent_role="default"):

        payload = {
    "event": "tool_result",
    "tool_name": tool_name,
    "output": result,
    "agent_role": agent_role,
    "run_id": self.run_id
}

        return self.send_event(payload)
