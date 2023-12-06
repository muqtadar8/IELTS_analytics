from django.shortcuts import render

# Create your views here.

def listen(request):

 return render(request, 'listen.html')