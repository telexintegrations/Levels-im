intergrations = {
  "data": {
    "author": "rm -rf",
    "date": {
      "created_at": "2025-02-18",
      "updated_at": "2025-02-18"
    },
    "descriptions": {
      "app_description": "An AI-powered integration that performs comparative analysis. It helps in evaluating and comparing various tools to weigh their pros and cons before integrating them into your build stack. Additionally, it can conduct competitor analysis between two or more companies offering similar services to determine the best fit for your requirements.",
      "app_logo": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQjU-T2anyHEHSbVg30jSwUc2Gck1HtolOCyg&s",
      "app_name": "Levels-im",
      "app_url": "https://levels-im.vercel.app/",
      "background_color": "#f7b27b"
    },
    "integration_category": "AI & Machine Learning",
    "integration_type": "modifier",
    "is_active": True,
    "key_features": [
      "Receive messages from the designated Telex channels.",
      "Process messages based and does a detailed analysis on the subjects for analysis.",
      "Send formatted responses on analysis back to the channel.",
    ],
    "permissions": {
      "events": [
        "Receive messages from Telex channels.",
        "Send formatted responses back to the channel.",
        "Log message formatting activity for auditing purposes."
      ]
    },
    "settings": [
    {
      "label": "channel_id",
      "type": "text",
      "description": "The ID of the channel to get ratios and answer prompts about",
      "required": True
    },
    {
      "label": "agent",
      "type": "radio",
      "options": ["gemini"],
      "description": "The Ai model of choice",
      "required": True
    },
    {
      "label": "api_key",
      "type": "text",
      "description": "The api key to use for the agent.",
      "required": True
    },
  ],
    "target_url": "ttps://4cad-105-112-22-127.ngrok-free.app/incoming-request",
    "website": "ttps://4cad-105-112-22-127.ngrok-free.app"
  }
}