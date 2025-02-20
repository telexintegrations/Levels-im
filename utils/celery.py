from celery import Celery
import httpx
import redis
from utils.agents import run_agent
from utils.lib import map_command_initial_prompt
from enum import Enum
from config import settings


class AgentModel(Enum):
  openai = "o3-mini"
  gemini = "gemini-2.0-flash-exp"
  deepseek = "deepseek-reasoner"

celery_app = Celery(
  "bg_tasks",
  broker= redis.from_url(settings.REDIS_URL),  # Redis broker URL
)

celery_app.conf.broker_connection_retry_on_startup = True

# task
@celery_app.task
def process_analysis(agent: str, api_key: str, msg: str, channel_id: str):
  agent_role = map_command_initial_prompt(msg)
  webhook_url = f"https://ping.telex.im/v1/webhooks/{channel_id}"
  model_llm = AgentModel[agent].value
  try:
      response = run_agent(agent, api_key, agent_role, msg, model_llm)
      payload = {
        "event_name": "Levels-im",
        "message": response.replace("```html", "").replace("```", ""),
        "status": "success",
        "username": "Levels"
      }
      try:
        with httpx.Client() as client:
            res = client.post(webhook_url, json=payload)
            
            # if res.status_code == 200:
            #     print(res) 
      except Exception as e:
        return f"{webhook_url} check failed: {str(e)}"
  except Exception as e:
      response = f"Error processing request: {str(e)}"
  return f'Task with id {celery_app.current_task.request.id} completed. Channel ID: {channel_id}'