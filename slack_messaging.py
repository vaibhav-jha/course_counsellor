from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


import os


SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

client = WebClient(token=SLACK_TOKEN)

# avi: U0702SSEF47
# michael: U070398E4UC
def send_message(text):
    try:

        print("PRINTING SLACK !!! SLACK ")

        response = client.chat_postMessage(
            channel="U070EMD5GJ3",
            text=text
        )

        response = client.chat_postMessage(
            channel="U070EMD5GJ3",
            text=text
        )

        print(response)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print(e)
