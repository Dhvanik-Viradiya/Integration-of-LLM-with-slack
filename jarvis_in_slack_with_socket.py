"""
title: Integrate LLM with slack  
author: Dhvanik Viradiya
"""

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv
from pathlib import Path
import pprint
from slack_sdk import WebClient
from youtube_transcript_api import YouTubeTranscriptApi
import pytube
import g4f

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_TOKEN"),
    signing_secret=os.environ.get("SIGNING_SECRET")
)
client = WebClient(token=os.environ.get("SLACK_TOKEN"))
bot_user_id = "U067PS2L2KB"
bot_username = "Jarvis"

def create_prompt_for_video(transcript):
    prompt = [
        f"SYSTEM: You are {bot_username}, an AI mediator well-versed in deep tech. "
        "You are an expert in summerization. You have given a transcript of a video."
        "You have to generate a short summery to understand about the video. Summery "
        "must be short enough to engage the people."
    ]
    prompt.append(f"TRANSCRIPT: {transcript}")
    prompt.append("SUMMERY: ")
    return "\n".join(prompt)



# Example of handling a message event
@app.event("message")
def handle_message(event, say):
    pprint.pprint(event)
    print("*"*50)
    user_id = event["user"]
    url = None
    text = event["text"]
    for block in event["blocks"]:
        for element in block["elements"]:
            for ele in element["elements"]:
                if ele["type"]=="link":
                    url = ele["url"]
                    break
            else:
                continue
            break
        else:
            continue
        break
    summary = ""
    str_transcript = ""
    if url:
        try:
            yt = pytube.YouTube(url)
            transcript_list = YouTubeTranscriptApi.list_transcripts(yt.video_id)
            for transcript in transcript_list:
                transcript = transcript.translate('en').fetch()
                for data in transcript:
                    str_transcript+=" "+data["text"]
                print(str_transcript)
                break
        except Exception as e:
            print("Error", e)
    if str_transcript:
        prompt = create_prompt_for_video(transcript=str_transcript)
        print(f"{prompt=}")

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
        if event.get("thread_ts"):
            client.chat_postMessage(channel=event["channel"], thread_ts=event.get("thread_ts"), text=response)
        else:
            client.chat_postMessage(channel=event["channel"], thread_ts=event.get("event_ts"), text=response)
    # history = client.conversations_history(channel=event["channel"], limit=10)
    # # print(history)
    # # print(dir(history))
    # for his in history.data["messages"]:
    #     pprint.pprint(his)
    #     # print(dir(his))
    #     print("-"*50)
    print("+"*50)

if __name__ == "__main__":
    # Start the app using SocketModeHandler
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()

