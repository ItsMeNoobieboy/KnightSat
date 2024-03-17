# adapted from https://platform.openai.com/docs/guides/images/usage

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def request_image():
    response = client.images.generate(
    model = "dall-e-2",
    prompt = "Generate a detailed night-time satellite image of Boston from directly overhead. Highlight the city lights clearly and show the urban landscape with precision. The image should capture streets, landmarks, and buildings, emphasizing the luminosity of the city lights. The perspective should feel as if viewing Boston from above at night.",
    n=1,
    size = "1024x1024"
    )
    image_url = response.data[0].url
    
    return image_from_url(image_url)

def edit_image(original, mask):
    response = client.images.edit(
    model = "dall-e-2",
    image = original,
    mask = mask,
    prompt = "Generate a satellite image depicting a massive power outage covering the entire area, leaving it nearly pitch dark. Ensure the blackout fills the entire mask, with only faint traces of light, if any. Highlight the stark difference between the illuminated areas and the engulfing darkness to convey the extent of the outage. The ENTIRE MASK SHOULD BE BLACK.",
    n=1,
    size = "1024x1024"
    )
    image_url = response.data[0].url

    return image_from_url(image_url)


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

def image_from_url(image_url):

    response = requests.get(image_url)

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        print(f"Failed to download image. Status code: {response.status_code}")


# edit_image("image_analysis/satelite_images/city.png", "image_analysis/masks/mask.png", "image_analysis/with_outages/with_outages7")

# request_image("image_try4")
# edit_image("image_try4.png", "image_analysis/masks/mask.png", "image_try3_with_outages")
