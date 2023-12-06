import openai 
from django.shortcuts import render
from openai import OpenAI
from django.conf import settings

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
    complete_text = ""

    for message in assessment:
        if message.role == 'assistant':
            complete_text += "Assistant's Feedback:\n"
            complete_text += message.content[0].text.value + '\n'
        elif message.role == 'user':
            complete_text += "User's Essay:\n"
            complete_text += message.content[0].text.value + '\n' + '-'*50 + '\n'

    return complete_text


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
    print(type(mes))
    
    client.beta.threads.delete(th_id)
    
    # return display_assessment(mes)
    return mes

def clean_text(raw_text):
    # Check if the raw text is a string, if not, return an empty string
    if isinstance(raw_text, str):
        # Extract relevant part of the text
        cleaned_text = raw_text.split(':', 1)[-1].strip()
        return cleaned_text
    else:
        return ''

def main(request):
    result = None
    cleaned_result = []  # Move this line outside the if block
    if request.method == 'POST':
        essay_input = request.POST['essay_input']
        result = feedback(essay_input)

        # print("Result from feedback function:", result)  # Add this line

        # # Clean the text in the result
        # if result:
        #     for message in result:
        #         cleaned_message = {}
        #         cleaned_message['role'] = message.role
        #         cleaned_message['content'] = [
        #             text_content.text
        #             for text_content in message.content
        #         ]
        #         cleaned_result.append(cleaned_message)

    # print("Cleaned Result:", cleaned_result)  # Add this line
    return render(request, 'index.html', {'result': result})
