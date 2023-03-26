#第三方作者包裝的官方API
from revChatGPT.V3 import Chatbot

def ChatGPT_Reply(Api_Key, Model, Ask) -> str:
    chatbot = Chatbot(
        api_key = Api_Key,
        engine = Model
    )

    prev_text = ""
    for data in chatbot.ask(Ask):
        prev_text += data
        print(data, end="", flush=True)
    return prev_text