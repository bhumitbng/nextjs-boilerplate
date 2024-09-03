from botbuilder.core import BotFrameworkAdapterSettings, TurnContext, BotFrameworkAdapter
from botbuilder.schema import Activity, ActivityTypes
from botbuilder.integration.aiohttp import CloudAdapter, ConfigurationBotFrameworkAuthentication
from aiohttp import web
from .. import app, appbuilder
from ..api.meeting_summarizer_api import MeetingSummarizerApi

APP_ID = 'your_microsoft_app_id'
APP_PASSWORD = 'your_microsoft_app_password'

bot_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
bot_adapter = CloudAdapter(ConfigurationBotFrameworkAuthentication({}, APP_ID, APP_PASSWORD))

async def messages(req: web.Request) -> web.Response:
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return web.Response(status=415)

    activity = Activity().deserialize(body)
    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await bot_adapter.process_activity(activity, auth_header, bot_logic)
    if response:
        return web.json_response(data=response.body, status=response.status)
    return web.Response(status=201)

async def bot_logic(turn_context: TurnContext):
    if turn_context.activity.type == ActivityTypes.message:
        text = turn_context.activity.text.lower()
        if text.startswith('summarize'):
            text_to_summarize = text.split('summarize', 1)[1].strip()
            summarizer = MeetingSummarizerApi()
            summary = summarizer.summarizer.summarize_text(text_to_summarize)
            await turn_context.send_activity(f"Summary: {summary}")
        else:
            await turn_context.send_activity("I can summarize text for you. Just start your message with 'summarize'.")

# Add the Teams integration to the app
app.router.add_post("/api/messages", messages)