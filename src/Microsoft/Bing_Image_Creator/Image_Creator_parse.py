import json
from ImageGen import ImageGen


def Image_Creator_Reply(prompt, cookie_file='./src/Microsoft/Bing_Image_Creator/cookies.json', Output_dir=None):
    # Get auth cookie
    U = None
    with open(cookie_file, encoding="utf-8") as file:
        cookie_json = json.load(file)
        for cookie in cookie_json:
            if cookie.get("name") == "_U":
                U = cookie.get("value")
                break

    if U is None:
        raise Exception("Could not find auth cookie")

    try:
        # Create image generator
        image_generator = ImageGen(U)
        images_list = image_generator.get_images(prompt)
    except:
        images_list = []

    # 移除圖片大小限制
    # normal_image_links = [link.split("?w=")[0] for link in images_list]
    return [prompt, images_list]
    """
    image_generator.save_images(
        image_generator.get_images(prompt),
        output_dir=Output_dir,
    )
    """

#Image_Creator_Reply("fuzzy creature wearing sunglasses, digital art", ".\cookies.json", ".\Images")