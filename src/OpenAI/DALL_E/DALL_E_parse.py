# 官方API
import openai

def DALL_E_Reply(Api_Key, Texts, Parameter, Size) -> list:
    openai.api_key = Api_Key

    image_list = []
    image = openai.Image.create(
        prompt = Texts,
        n = Parameter,
        size = Size
    )
    for Dict in image['data']:
        image_list.append(str(Dict['url']))

    return image_list