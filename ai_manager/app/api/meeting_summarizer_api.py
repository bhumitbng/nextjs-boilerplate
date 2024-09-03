from flask_appbuilder.api import BaseApi, expose
from .. import appbuilder
from ..models import db
from meeting_summarizer import MeetingSummarizer

class MeetingSummarizerApi(BaseApi):
    summarizer = MeetingSummarizer()

    @expose('/summarize', methods=['POST'])
    def summarize_meeting(self):
        if not self.request.json or 'text' not in self.request.json:
            return self.response_400('Text is required')
        text = self.request.json['text']
        summary = self.summarizer.summarize_text(text)
        key_points = self.summarizer.extract_key_points(text)
        action_items = self.summarizer.extract_action_items(text)
        return self.response(200, {
            'summary': summary,
            'key_points': key_points,
            'action_items': action_items
        })

appbuilder.add_api(MeetingSummarizerApi)