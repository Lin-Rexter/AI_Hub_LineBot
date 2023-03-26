# LineBot模組
from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    TemplateSendMessage,
    ImageCarouselTemplate,
    ImageCarouselColumn,
    URIAction
)

# 被動發送訊息(*)
def reply_send(reply):
    return TextSendMessage(
        text=reply
    )
 
# 主動推送訊息
def push_send(messages):
    return TextSendMessage(
        text=messages
    )

# 發送圖片
def Image_Send(url):
    return ImageSendMessage(
        original_content_url = url,
        preview_image_url = url
    )

# 發送輪播圖片(*)
def Image_Carousel(Label_name, Images):
    try:
        image_columns = []

        for image in Images[1]:
            image_columns.append(
                    ImageCarouselColumn(
                        image_url=image,
                        action=URIAction(
                            label=Label_name,
                            uri=image
                        )
                    )
                )

        image_carousel_template_message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                    columns = image_columns
                )
        )
    except Exception as e:
        print("[Image_Carousel]發生錯誤: " + e)

    return image_carousel_template_message

