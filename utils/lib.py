
from bs4 import BeautifulSoup
import httpx
from utils.agents import run_agent

from enum import Enum


class AgentModel(Enum):
  openai = "o3-mini"
  gemini = "gemini-2.0-flash-exp"
  deepseek = "deepseek-reasoner"


def extract_text_from_html(html_string: str) -> str:
  soup = BeautifulSoup(html_string, "html.parser")
  return soup.get_text()

def is_valid_command(text: str) -> bool:
  return text.startswith('/levels') or text.startswith('/ratio')

def levels_command() -> str:
  # Process /levels command
  base_prompt = """
    You are a world-class data analyst, recognized as a leader in the industry for delivering insightful and robust competitive analyses.
    Your task is to perform a detailed competitive analysis on a given topic by the user (it starts with /levels command).
    Provide a data-driven and insightful analysis, comparing and contrasting the key competitors. Focus on identifying their key features, strengths, market value/stock and weaknesses. Where possible, quantify your analysis with comparative metrics and data points.
    Your response should be in html, enclosed within a single `<div>` tag (no additional styling is required. Plus no <table> related tag for now and no mdx syntax).
    The analysis should be comprehensive yet concise, aiming for a word count not greater than 2000 and a character count between 2000 - 25000 characters.
    Deliver a high-quality, impactful analysis befitting your world-class expertise.
  """
  return base_prompt

def ratio_command() -> str:
  # Process /ratio command
  base_prompt = """
   You are a world-class critic and comparative data analyst, renowned for delivering incisive comparative evaluations.
    Your task is to provide a detailed comparative analysis on a given topic by the user (it starts with /ratio command).
    Offer a comprehensive review that compares key competitors by highlighting their strengths, weaknesses, market positioning, and unique value propositions.
    Ensure that your analysis includes comparative metrics and quantitative data to clearly outline the differences between the competitors.
    Your response should be formatted as HTML, enclosed within a single `<div>` tag.
    The analysis should be both exhaustive and concise, targeting a word count not more than 2000 words or a character count between 2000 and 25000.
    Produce a high-quality critique that reflects deep comparative insight.
  """
  return base_prompt

def map_command_initial_prompt(text: str) -> str | None:
  commands = {
    '/levels': levels_command,
    '/ratio': ratio_command
  }

  for command, handler in commands.items():
    if text.startswith(command):
      return handler()

  return None

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
  return f'Taskcompleted. Channel ID: {channel_id}'