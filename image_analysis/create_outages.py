# edited from https://platform.openai.com/docs/guides/images/usage

from openai import OpenAI

OPENAI_API_KEY = "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"
client = OpenAI(api_key=OPENAI_API_KEY)

def edit_image(original, mask, output_name):
    response = client.images.edit(
    model="dall-e-2",
    image=open(f"satelite_images/{original}", "rb"),
    mask=open(f"masks/{mask}", "rb"),
    prompt="fill the ENTIRE mask with a DEVASTATING, EXTREMELY, VERY LARGE POWER OUTAGE. the ENTIRE area is nearly pitch dark.",
    n=1,
    size="1024x1024"
    )
    image_url = response.data[0].url
    save_image(image_url, output_name)


# edited from chatgpt output

from PIL import Image
import requests
from io import BytesIO

def save_image(image_url, output_name):

    response = requests.get(image_url)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

        img.save(f"with_outages/{output_name}.png")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


edit_image("city.png", "mask.png", "with_outages7")