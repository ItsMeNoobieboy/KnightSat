from PIL import Image

def make_mask(mask, image):
    # Open both images
    mask = mask.convert("RGBA")
    image = image.convert("RGBA")

    # Get pixel data for both images
    pixel_data1 = mask.load()
    pixel_data2 = image.load()

    # Iterate over each pixel in the first image
    width, height = mask.size
    for y in range(min([height, image.size[1]])):
        for x in range(min([width, image.size[0]])):
            # Check if the pixel in the first image is red
            if pixel_data1[x, y] == (255, 0, 0, 255):  # Assuming pure red, adjust as needed
                # Set the corresponding pixel in the second image to transparent
                pixel_data2[x, y] = (0, 0, 0, 0)

    return image
