from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = "xoxb-6925306004261-6971253253811-jDmH39JOcw3IUCwHmXttWLeB"

client = WebClient(token=SLACK_TOKEN)


def send_message(text):
    try:
        response = client.chat_postMessage(
            channel="U0702SSEF47",
            text=text
        )

        print(response)
    except SlackApiError as e:
        # You will get a SlackApiError if "ok" is False
        print(e)
