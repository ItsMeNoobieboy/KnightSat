from get_night_lights import download_image
from create_outages import edit_image

longitude = int(input("Enter the longitude: "))
latitude = int(input("Enter the latitude: "))
output_path = f"image_analysis/satelite_images/{latitude},{longitude}"

download_image(longitude, latitude, output_path)

print(f"Image downloaded to {output_path}.png")

mask_name = input("Enter the name of the mask file (this must be a .png): ")

edit_image(
    output_path,
    f"image_analysis/masks/{mask_name}.png",
    f"image_analysis/with_outages/{latitude},{longitude}",
)

print(
    f"Image with outages created at image_analysis/with_outages/{latitude},{longitude}.png"
)
