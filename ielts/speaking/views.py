# views.py
from django.shortcuts import render
from django.http import HttpResponse
import requests
from tempfile import NamedTemporaryFile
import base64
import os

API_URL = "https://api-inference.huggingface.co/models/muqtadar/speech_emotion"
HEADERS = {"Authorization": "Bearer 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"}

def speak(request):
    if request.method == 'POST':
        if 'audio' in request.FILES:
            # Upload case
            audio_data = request.FILES['audio'].read()
        else:
            # Recording case
            audio_data = base64.b64decode(request.POST['audio_data'])

        # Create temporary file to hold audio data
        with NamedTemporaryFile(suffix='.wav', delete=False) as f:
            f.write(audio_data)
            audio_filename = f.name

        try:
            # Send audio data to Hugging Face API
            response = requests.post(API_URL, headers=HEADERS, files={'audio': open(audio_filename, 'rb')})
            response.raise_for_status()
            api_response = response.json()

            # Prepare data for response
            results = {
                'audio_data': audio_data,
                'api_response': api_response,
            }

            return render(request, 'results.html', context=results)

        except requests.RequestException as e:
            # Handle API request errors
            return HttpResponse(f"Error in API request: {str(e)}", status=500)

        finally:
            # Remove temporary file
            os.remove(audio_filename)

    return render(request, 'speak.html')
