from django.shortcuts import render
from openai import OpenAI
from django.conf import settings
from django.contrib.auth.decorators import login_required




api_key = settings.OPENAI_API_KEY
class ThreadMessage:
    def __init__(self, id, assistant_id, content, created_at, file_ids, metadata, object, role, run_id, thread_id):
        self.id = id
        self.assistant_id = assistant_id
        self.content = content
        self.created_at = created_at
        self.file_ids = file_ids
        self.metadata = metadata
        self.object = object
        self.role = role
        self.run_id = run_id
        self.thread_id = thread_id
class MessageContentText:
    def __init__(self, text):
        self.text = text
def display_assessment(assessment):
    result = []
    for message in assessment:
        if message.role == 'assistant':
            content = message.content[0].text.value.replace('\n', '<br>').replace('**', '')
            bold_phrases = ['Task Response','Task Achievement', 'Coherence and Cohesion', 'Lexical Resource', 'Grammatical Range and Accuracy', 'Overall Score', 'Feedback']
            for phrase in bold_phrases:
                content = content.replace(phrase, f'<strong>{phrase}</strong>')
            result.append({
                'role': "Assistant's Feedback",
                'content': [content]
            })
    return result
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
    return display_assessment(mes)
def main(request):
    result = None
    if request.method == 'POST':
        essay_input = request.POST['essay_input']
        result = feedback(essay_input)
    return render(request, 'write.html', {'result': result})