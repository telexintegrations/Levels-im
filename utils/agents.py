from fastapi import types
from google import genai
from google.genai import types
import httpx
from openai import OpenAI




class Agents:
  def __init__(self, api_key: str):
    self.api_key = api_key

  def gemini(self, agent_role: str, prompt: str, model_llm: str, channel_id: str) -> str:
    client = genai.Client(api_key=self.api_key)
    try:
      response = client.models.generate_content(
        model=model_llm,
        config=types.GenerateContentConfig(
          system_instruction=agent_role),
        contents=[prompt]
      )
      return response.text
    except Exception as e:
      webhook_url = f"https://ping.telex.im/v1/webhooks/{channel_id}"
      send_webhook(webhook_url, {
        "event_name": "Levels-im",
        "message": f"Error processing request: {str(e)}",
        "status": "error",
        "username": "Levels"
      })
      raise e

  def openai(self, agent_role: str, prompt: str, model_llm: str) -> str:
    client = OpenAI(api_key=self.api_key)

    response = client.chat.completions.create(
      model=model_llm,
      reasoning_effort="medium",
      messages=[
        {
          "role": "system",
          "content": agent_role
        },
        {
          "role": "user",
          "content": prompt
        }
      ]
    )
    return response.choices[0].message.content
  
  def deepseek(self, agent_role: str, prompt: str, model_llm: str) -> str:
    client = OpenAI(api_key=self.api_key, base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
      model=model_llm,
      reasoning_effort="medium",
      messages=[
        {
          "role": "system",
          "content": agent_role
        },
        {
          "role": "user",
          "content": prompt
        }
      ]
    )
    return response.choices[0].message.content


def run_agent(agent: str, api_key: str, agent_role: str, prompt: str, model_llm: str, channel_id: str):
  match agent:
    case 'openai':
      return Agents(api_key).openai(agent_role, prompt, model_llm)
    case 'gemini':
      return Agents(api_key).gemini(agent_role, prompt, model_llm, channel_id)
    case 'deepseek':
      return Agents(api_key).deepseek(agent_role, prompt, model_llm)
    case _:
      return 

def send_webhook(url: str, data: dict) -> str:
  try:
    with httpx.Client() as client:
      res = client.post(url, json=data)
      return res.status_code
  except Exception as e:
    return f"{url} check failed: {str(e)}"
  
