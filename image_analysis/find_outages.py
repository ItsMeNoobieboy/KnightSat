from PIL import Image, ImageDraw, ImageChops
import numpy as np


def find_difference(no_outage_path, with_outage_path, output_path):

    no_outage = Image.open(no_outage_path)
    with_outage = Image.open(with_outage_path)

    no_outage = no_outage.convert("RGB")
    with_outage = with_outage.convert("RGB")

    # ImageChops.difference(no_outage, with_outage).show()

    difference = np.sum(
        np.array(ImageChops.difference(no_outage, with_outage)), axis=-1
    )

    coords = np.column_stack(np.where(difference > 250))

    draw = ImageDraw.Draw(no_outage)
    for coord in coords:
        draw.rectangle([coord[1], coord[0], coord[1] + 1, coord[0] + 1], outline="red")

    # Save the result
    no_outage.save(f"{output_path}.png")
