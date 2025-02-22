from fastapi import BackgroundTasks, FastAPI, Request
from integrations import intergrations
from fastapi.middleware.cors import CORSMiddleware

from utils.lib import extract_text_from_html, is_valid_command, process_analysis



app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.post('/incoming-request')
async def incoming_request(request: Request, background_tasks: BackgroundTasks):
	res = await request.json()
	print(res)
	actual_text = extract_text_from_html(res.get('message'))
	settings_list = res.get('settings', [])
	if not is_valid_command(actual_text):
		return  {
			"event_name": "Levels_processing",
			"message": f'{actual_text}',
			"status": "success",
			"username": "Levels"
		}
	defaults = {"agent": "", "api_key": "", "channel_id": ""}
	values = {
		key: next((item.get("default", default)
			for item in settings_list if item.get("label") == key), default)
		for key, default in defaults.items()
	}
	agent, api_key, channel_id = values["agent"], values["api_key"], values["channel_id"]
 
	background_tasks.add_task(process_analysis, agent, api_key, actual_text, channel_id)
 
	cleaned_text = actual_text
	if actual_text.startswith('/levels '):
		cleaned_text = actual_text[8:]
	elif actual_text.startswith('/ratio '):
		cleaned_text = actual_text[7:]

	data = {
		"event_name": "Levels_processing",
		"message": f'{cleaned_text} <strong style="color: green">-- Received (app: Levels-im)</strong>',
		"status": "success",
		"username": "Levels"
	}
	return data

@app.get('/integrations.json')
async def integrations():
  return intergrations