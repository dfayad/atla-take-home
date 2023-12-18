from django.test import TestCase

from mock import patch

from .views import continue_existing_chat

from django.http import HttpRequest

from .chatgpt_client import OpenAIClient

from api.models import Chat, ChatMessage

from datetime import datetime

# Create your tests here.

class ChatAppTests(TestCase):

    def test_continue_existing(self):
        with patch('api.chatgpt_client.OpenAIClient.continue_chat') as client_mock, patch('api.models.Chat.collection') as db_mock:
            # mock return value
            test_resp = "Hello there, how may I assist you today?"
            client_mock.return_value = test_resp

            # mock retrival of chat
            # mock previous chat
            now = datetime.now()
            previous_chat_message = ChatMessage(
                sender="atla",
                message="test",
                timestamp=now
            )
            test_chat = Chat(
                chat_id = 1,
                user_id = 1,
                created_at = now,
                messages = [previous_chat_message]
            )
            db_mock.get.return_value = test_chat #let's say it's an empty chat to simplify

            # #build mock request
            request = HttpRequest()
            request.method = 'POST'
            request.POST.update({"user": "atla", "text": "some text"})

            # #make call to continue existing chat from views
            test_id = 1
            resp = continue_existing_chat(request, test_id)

            assert resp.data.get('response') == test_resp

    #TODO: add tests for failure cases

class MockOpenAPIRequest(TestCase):

    def test_sucessful_open_api_call(self):

        test_content = "test response"

        test_return_value = {
            "id": "chatcmpl-123",
            "object": "chat.completion",
            "created": 1677652288,
            "model": "gpt-3.5-turbo-0613",
            "system_fingerprint": "fp_44709d6fcb",
            "choices": [{
                "index": 0,
                "message": {
                "role": "assistant",
                "content": test_content,
                },
                "logprobs": None,
                "finish_reason": "stop"
            }],
            "usage": {
                "prompt_tokens": 9,
                "completion_tokens": 12,
                "total_tokens": 21
            }
        }

        #mock return value from OpenAI
        with patch('openai.ChatCompletion') as openai_mock:
            openai_mock.create.return_value = test_return_value

            now = datetime.now()
            previous_chat_message = ChatMessage(
                sender="atla",
                message="test",
                timestamp=now
            )

            resp = OpenAIClient.continue_chat(previous_chat_message)

            assert test_content == resp

    #TODO: add tests for failure cases