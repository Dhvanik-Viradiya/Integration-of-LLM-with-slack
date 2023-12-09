"""
title: Integrate LLM with slack  
author: Dhvanik Viradiya
"""

import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from threading import Thread
import time
import pprint
import g4f

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

database = {}

slack_event_adapter = SlackEventAdapter(
    os.environ["SIGNING_SECRET"], "/slack/events", app
)
client = slack.WebClient(token=os.environ["SLACK_TOKEN"])
bot_user_id = "U067PS2L2KB"
bot_username = "Jarvis"


def create_prompt_from_history(event):
    prompt = [
        f"SYSTEM: You are {bot_username}, an AI mediator well-versed in deep tech. "
        "Currently participating in a group chat of developers and managers, each "
        "user's message is prefixed by a unique user id. Provide a concise summary "
        "of the ongoing discussion, incorporating your own tech knowledge and "
        "actively contribute arguments and questions, ensuring fairness to all "
        "participants. Do not generate answer when think that your opinion is not "
        "required. Do not generate answer when you need more context of the "
        "conversation. Do generate response when you are explicitly asked to "
        "respond. If prompt contains the <@ID>, consider it as a user. So, reply "
        "the same way."
    ]

    history = client.conversations_history(channel=event["channel"], limit=20)
    for message in history.data["messages"][::-1]:
        user_id = message["user"]
        # user_data = client.users_info(user=user_id)
        # username = user_data.data["user"]["name"]
        text = message["text"]
        if user_id == bot_user_id:
            prompt.append("ASSISTANT: " + text)
        else:
            prompt.append(f"USER: <@{user_id}> writes {text}")
    prompt.append("ASSISTANT: ")
    prompt = "\n".join(prompt)
    prompt = prompt.replace(f"<@{bot_user_id}>", bot_username)
    print(prompt)
    return prompt


@slack_event_adapter.on("app_mention")
def app_mention(payload):
    event = payload.get("event", {})
    if event["ts"] in database or event["user"] == bot_user_id:
        return
    database[event["ts"]] = True
    prompt = create_prompt_from_history(event=event)

    response = g4f.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )
    print(f"{response=}")
    client.chat_postMessage(channel=event["channel"], text=response)
    print("-" * 50)


@slack_event_adapter.on("message")
def message(payload):
    event = payload.get("event", {})
    event = payload.get("event", {})
    if event["channel_type"] == "im" and event["user"] != bot_user_id:
        if event["ts"] in database:
            print("Old", event["ts"])
            return
        database[event["ts"]] = True
        prompt = create_prompt_from_history(event=event)

        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        client.chat_postMessage(channel=event["channel"], text=response)


if __name__ == "__main__":
    app.run(debug=True)
