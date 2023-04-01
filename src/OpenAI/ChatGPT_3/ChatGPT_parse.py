import os
from pathlib import Path
# 讀取.env檔
from dotenv import load_dotenv
#第三方作者包裝的官方API
from revChatGPT.V3 import Chatbot

# 讀取.env檔環境變量
env_path = Path(__file__).resolve().parents[3] / '.env'
load_dotenv(env_path)

# 獲取OpenAI Api的Key
Openai_Api_Key = os.getenv('OPENAI_API_KEY', None)
ChatGPT_Model= os.getenv('CHATGPT_MODEL', None)

chatbot = Chatbot(
    api_key = Openai_Api_Key,
    engine = ChatGPT_Model,
    top_p = 1, # 0.0 ~ 1.0 # 數值越高
    temperature = 0.5, # 0.0 ~ 2.0，數值越高越多樣化
    presence_penalty = 0.0, # -2.0 ~ 2.0
    frequency_penalty = 0.0, # -2.0 ~ 2.0
    reply_count = 1
)

def ChatGPT_Reply(Ask) -> str:
    prev_text = ""
    for data in chatbot.ask(Ask):
        prev_text += data
        print(data, end="", flush=True)
    return prev_text