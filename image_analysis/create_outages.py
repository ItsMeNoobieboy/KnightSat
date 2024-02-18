# adapted from https://platform.openai.com/docs/guides/images/usage

from openai import OpenAI

OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

def edit_image(original, mask, output_name):
    response = client.images.edit(
    model = "dall-e-2",
    image = open(original, "rb"),
    mask = open(mask, "rb"),
    prompt = "fill the ENTIRE mask with a DEVASTATING, EXTREMELY, VERY LARGE POWER OUTAGE. the ENTIRE area is nearly pitch dark.",
    n=1,
    size = "1024x1024"
    )
    image_url = response.data[0].url
    save_image(image_url, output_name)


# adapted from chatgpt output

from PIL import Image
import requests
from io import BytesIO

def save_image(image_url, output_name):

    response = requests.get(image_url)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

        img.save(f"{output_name}.png")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


edit_image("image_analysis/satelite_images/city.png", "image_analysis/masks/mask.png", "image_analysis/with_outages/with_outages7")