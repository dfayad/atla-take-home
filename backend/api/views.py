from api.models import Chat, ChatMessage
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from api.chatgpt_client import OpenAIClient, continue_chat
from datetime import datetime


@api_view(["POST"])
def chat(request: Request, id: str) -> Response:
    chat = Chat.collection.get("ca1hnzvWSH8g8Cn1O0rc")
    return Response({"user_message1": chat.messages[-1].message})


@api_view(["POST"])
def start_new_chat(request: Request) -> Response:
    # chat = Chat.collection.get("ca1hnzvWSH8g8Cn1O0rc")
    return Response({"started new chat": "new chat"})


@api_view(["POST"])
def continue_existing_chat(request: Request, id: str) -> Response:

    # TODO: error handling: no existing chat, empty messages, empty text, etc.
    # get existing messages for chat id
    chat = Chat.collection.get(id)
    messages_from_existing_chat = chat.messages.copy() #deep copy

    # format new chat message
    data = request.POST
    new_text = data.get("text")
    user = data.get("user", "atla") #default to atla if none is passed (ideally we extract user from headers)
    now = datetime.now()
    new_message = ChatMessage(
        sender=user, 
        message=new_text, 
        timestamp=now
    )

    # add to message list
    messages = messages_from_existing_chat.append(new_message)

    # make call to openAI api
    response = OpenAIClient.continue_chat(messages)

    return Response({"response": response})