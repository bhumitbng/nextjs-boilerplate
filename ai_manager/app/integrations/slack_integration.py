from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slackeventsapi import SlackEventAdapter
from flask import Flask, request, Response
from .. import app, appbuilder
from ..api.meeting_summarizer_api import MeetingSummarizerApi

SLACK_SIGNING_SECRET = 'your_slack_signing_secret'
SLACK_BOT_TOKEN = 'your_slack_bot_token'

slack_event_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, '/slack/events', app)
client = WebClient(token=SLACK_BOT_TOKEN)

@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if 'summarize' in text.lower():
        # Extract the text to summarize (everything after 'summarize')
        text_to_summarize = text.lower().split('summarize', 1)[1].strip()
        
        summarizer = MeetingSummarizerApi()
        summary = summarizer.summarizer.summarize_text(text_to_summarize)

        try:
            client.chat_postMessage(channel=channel_id, text=f"Summary: {summary}")
        except SlackApiError as e:
            print(f"Error posting message: {e}")

@app.route('/slack/commands', methods=['POST'])
def slack_command():
    data = request.form
    channel_id = data.get('channel_id')
    user_id = data.get('user_id')
    command = data.get('command')
    text = data.get('text')

    if command == '/summarize':
        summarizer = MeetingSummarizerApi()
        summary = summarizer.summarizer.summarize_text(text)
        return Response(f"Summary: {summary}", content_type='text/plain')

    return Response('Invalid command', content_type='text/plain')

# Add the Slack integration to the app
appbuilder.add_api(slack_event_adapter.server)