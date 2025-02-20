import httpx


def request_to_webhook(webhook_url: str, payload: dict) -> str:
  try:
    with httpx.Client() as client:
      res = client.post(webhook_url, json=payload)
      return res.text
  except Exception as e:
    return f"{webhook_url} check failed: {str(e)}"