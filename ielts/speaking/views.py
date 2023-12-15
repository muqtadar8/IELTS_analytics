# Create your views here.
import requests
from django.shortcuts import render


def query_audio(filename):
    API_URL = "https://api-inference.huggingface.co/models/muqtadar/voice_emo"
    headers = {"Authorization": "Bearer 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"}
    with open(filename, "rb") as f:
        data = f.read()
        response = requests.post(API_URL, headers=headers, data=data)
    return response.json()



def query_audio1(filename):
    API_URL1 = "https://api-inference.huggingface.co/models/muqtadar/speech_emotion"
    headers1 = {"Authorization": "Bearer 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"}
    with open(filename, "rb") as f:
        data = f.read()
        response = requests.post(API_URL1, headers=headers1, data=data)
    return response.json()

def speak(request):
    if request.method == "POST" and request.FILES['audio']:
        uploaded_audio = request.FILES['audio']

        # Save the uploaded audio to a temporary file
        with open("static/temp_audio.mp3", "wb") as f:
            for chunk in uploaded_audio.chunks():
                f.write(chunk)

        # Perform audio analysis using your functions
        speech_emotion_result = query_audio1("static/temp_audio.mp3")
        voice_emotion_result = query_audio("static/temp_audio.mp3")

        results = [speech_emotion_result, voice_emotion_result]

        return render(request, 'results.html', {'results': results, 'audio': uploaded_audio})

    return render(request, 'speak.html')