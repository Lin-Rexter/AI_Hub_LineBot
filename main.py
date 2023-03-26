# coding=utf-8
import os
import sys
import re
import json
import time
from functools import reduce
from pathlib import Path

# 輸出詳細錯誤信息
import traceback

# 異常處理
from werkzeug import exceptions

# 讀取.env檔
from dotenv import load_dotenv

# Flask WSGI Web應用框架
from flask import (
    Flask,
    request,
    abort
)

# LineBot
from linebot import (
    LineBotApi,
    WebhookHandler
)

# LineBot
from linebot.exceptions import (
    InvalidSignatureError
)

# LineBot模組
from linebot.models import (
    MessageEvent,
    TextMessage
)

# LineBot API
from src.LineBot.Api import (
    reply_send,
    push_send,
    Image_Send,
    Image_Carousel
)

# OpenAI - ChatGPT(ChatGPT-3.5) AI聊天
from src.OpenAI.ChatGPT_3 import ChatGPT_Reply

# Microsoft - EdgeGPT(ChatGPT-4) AI聊天
from src.Microsoft.Bing_EdgeGPT_4 import EdgeGPT_Reply

# OpenAI - DALL-E AI生成圖像
from src.OpenAI.DALL_E import DALL_E_Reply

# Microsoft - Bing Image Creator(結合DALL-E) AI生成圖像
from src.Microsoft.Bing_Image_Creator import Image_Creator_Reply

# 翻譯器
from googletrans import Translator
translator = Translator()

# 讀取.env檔環境變量
load_dotenv('.env')

# Flask設置
app = Flask(__name__)


# 獲取Line Bot的TOKEN、 SECRET
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
line_user_id = os.getenv('USER_ID', None) # 可選


# 獲取OpenAI Api的Key
openai_api_key = os.getenv('OPENAI_API_KEY', None)

if not channel_access_token:
    print('Please set the LINE_CHANNEL_ACCESS_TOKEN environment variable in the .env file.\n請在.env檔設置LINE_CHANNEL_ACCESS_TOKEN環境變量。\n')
    sys.exit(1)

if not channel_secret:
    print('Please set the LINE_CHANNEL_SECRET environment variable in the .env file.\n請在.env檔設置LINE_CHANNEL_SECRET環境變量。\n')
    sys.exit(1)

if not openai_api_key:
    print('Please set the OPENAI_API_KEY environment variable in the .env file.\n請在.env檔設置OPENAI_API_KEY環境變量。\n')
    sys.exit(1)

# 設置Line Bot的TOKEN、 SECRET、 USER_ID
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
user_id = WebhookHandler(line_user_id)

# 設置OpenAI Api的Key
Openai_Api_Key = openai_api_key


# Flask 首頁
@app.route('/')
def welcome():
    return "<h1>AI Together應用運行中...</h1>"
    #return render_template('welcome.html')

# Line Bot Webhook
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# Line 接收、處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = (event.message.text).strip() # 使用者訊息

    useful_commands = ['/img ', '/gpt ', '/gpt4 ']  # 有效的指令
    ignore_commands = ['/help', '/new'] # 忽略的指令

    if(user_message).startswith(tuple(useful_commands)):
        result = commands(user_message)
        if(isinstance(result, list)):
            reply = Image_Carousel("Open", result)
        elif(isinstance(result, str)):
            reply = reply_send(result)
    elif(user_message).startswith(tuple(ignore_commands)):
        reply = None
        pass
    else:
        reply_text = "指令錯誤!\n\n範例:\n\r1. /img 一個大型的Cyberpunk城市 #註:AI生成圖像(Bing Image Creator),1024x1024 X4，服務剛發佈不久，不支援中文，因此使用翻譯器自動把請求翻譯成英文\n\n\r2. /gpt 幫我製作一份xxx表格\n\n\r3. /gpt4 幫我搜尋臺灣近期的新聞"
        reply = reply_send(reply_text)

    """
    line_bot_api.push_message(
        user_id,
        reply
    }
    """

    if(reply != None):
        line_bot_api.reply_message(
            event.reply_token,
            reply
        )

# 翻譯處理
def translate(texts):
    translated = translator.translate(text=texts, dest='en')
    print("\n翻譯結果: " + translated.text + "\n")
    return translated.text

# 命令對應第三方功能處理
def commands(command):
    # 指令對應功能
    commands_list = {
        '/gpt': lambda msg: ChatGPT_Reply(Openai_Api_Key, "gpt-3.5-turbo", msg),
        '/gpt4': lambda msg: EdgeGPT_Reply(msg),
        '/img': lambda msg: Image_Creator_Reply(translate(msg)),
        '/dalle': lambda msg: DALL_E_Reply(Openai_Api_Key, msg, 1, "256x256") #256x256, 512x512, 1024x1024 pixels
    }

    command_name = command.split(" ")[0].strip() # 命令名稱
    command_value = command.split(command_name)[1].strip() # 命令值

    print("\n使用者完整命令: {}".format(command)) # 使用者完整命令
    print("\n命令的值: {}".format(command_value)) # 命令的值

    reply_message = commands_list[command_name](command_value)
    print("\n命令結果: {}".format(reply_message)) # 命令結果

    return reply_message


if __name__ == "__main__":
    #app.secret_key = os.urandom(16) # Flask flash需要Session，因此需生成密鑰，防止CSRF。
    app.run(debug=True, host="127.0.0.1")