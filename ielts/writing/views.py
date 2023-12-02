import openai 
from django.shortcuts import render
from openai import OpenAI
from django.conf import settings

api_key = settings.OPENAI_API_KEY


def feedback(inp):
    # client
    client = OpenAI(api_key=api_key)
    # Retrive Assistant
    client.beta.assistants.retrieve("asst_vKBqFPhSg7yKz4B1tHtrwXDG")
    # create empty thread
    empty_thread = client.beta.threads.create()
    # thread id
    th_id = empty_thread.id
    # print(th_id)
    # Generating message (Add)
    thread_message = client.beta.threads.messages.create(
        th_id,
        role="user",
        content= inp ,
    )
    #Message Id
    mes_id = thread_message.id
    # Retrive Response
    messages = client.beta.threads.messages.retrieve(
    message_id=mes_id,
    thread_id=th_id,
    )
    #Run
    run = client.beta.threads.runs.create(
        thread_id=th_id,
        assistant_id="asst_vKBqFPhSg7yKz4B1tHtrwXDG"
    )
    run_id  = run.id

    def rec():
      run = client.beta.threads.runs.retrieve(
      thread_id=th_id,
      run_id= run_id
      )
      if run.status == 'completed' :
        return
      else :
        rec()

    rec()

    thread_messages = client.beta.threads.messages.list(th_id)
    mes = thread_messages.data
    client.beta.threads.delete(th_id)


    return mes

def main(request):
    result = None
    if request.method == 'POST':
        essay_input = request.POST['essay_input']
        result = feedback(essay_input)
    return render(request, 'index.html', {'result': result})

