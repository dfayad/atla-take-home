from django.urls import path

from .views import chat, continue_existing_chat, start_new_chat

# TODO: actually use RESTful path patterns, this was quick and dirty workaround so routes don't overlap
urlpatterns = [
    path("chat/<id>", chat, name="chat"),
    path("chat-new", start_new_chat, name="start_new_chat"),
    path("chat-continue/<id>", continue_existing_chat, name="continue_existing_chat")
]
