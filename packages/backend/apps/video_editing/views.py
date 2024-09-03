import os
import tempfile
import subprocess
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from django.conf import settings

class VideoEditingView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        video_file = request.FILES.get('video')
        if not video_file:
            return Response({"error": "No video file provided"}, status=status.HTTP_400_BAD_REQUEST)

        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)
            input_path = temp_file.name

        # Process the video using Auto-Editor
        output_path = self.process_video(input_path)

        # Save the processed video to storage
        with open(output_path, 'rb') as processed_file:
            saved_path = default_storage.save(f'processed_videos/{video_file.name}', processed_file)

        # Clean up temporary files
        os.unlink(input_path)
        os.unlink(output_path)

        # Generate URL for the processed video
        video_url = settings.MEDIA_URL + saved_path

        return Response({"message": "Video processing completed", "video_url": video_url}, status=status.HTTP_200_OK)

    def process_video(self, input_path):
        output_path = input_path.replace('.mp4', '_processed.mp4')
        command = [
            'auto-editor',
            input_path,
            '--output', output_path,
            '--silent',
            '--no-open'
        ]
        
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error processing video: {e.stderr}")
            raise Exception("Video processing failed")

        return output_path