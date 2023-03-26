import asyncio
from EdgeGPT import Chatbot, ConversationStyle

bot = Chatbot(cookiePath='./src/Microsoft/Bing_EdgeGPT_4/cookies.json')

async def main(text):
    reply_dict = await bot.ask(prompt=text, conversation_style=ConversationStyle.creative)
    reply_text = reply_dict["item"]["messages"][1]["text"]
    #await bot.close()
    #print(reply_text)
    return reply_text


def EdgeGPT_Reply(text):
    return asyncio.run(main(text))