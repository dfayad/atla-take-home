import openai

openai.api_key = '<API_KEY>'

default_model = "gpt-3.5-turbo"

# TODO: MASSIVE CLEANUP

# Could only get mocks to work this way? 
def continue_chat(messages: list):
    resp = openai.ChatCompletion.create(
        model=default_model,
        messages=messages
    )

    # return content of top choice
    return resp['choices'][0]['message']['content']

# Originally wanted to test with this
class OpenAIClient:
    def __init__(self, client_url = "https://api.openai.com"):
        self.client_url = client_url

    @staticmethod
    def continue_chat(messages: list):
        resp = openai.ChatCompletion.create(
            model=default_model,
            messages=messages
        )

        # return content of top choice
        return resp['choices'][0]['message']['content']
