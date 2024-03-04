# adapted from https://nasa-gibs.github.io/gibs-api-docs/python-usage/#basic-wms-connection

from owslib.wms import WebMapService


def download_image(longitude, latitude, output_path):
    # Connect to GIBS WMS Service
    wms = WebMapService(
        "https://gibs.earthdata.nasa.gov/wms/epsg4326/best/wms.cgi?", version="1.1.1"
    )

    pixels = 1024
    distance = 1

    layer = "VIIRS_CityLights_2012"

    # Configure request
    img = wms.getmap(
        layers=[
            layer
        ],  # Layers VIIRS_Night_Lights, VIIRS_CityLights_2012, or MODIS_Terra_CorrectedReflectance_TrueColor
        srs="epsg:4326",  # Map projection
        bbox=(
            longitude - distance,
            latitude - distance,
            longitude + distance,
            latitude + distance,
        ),  # Bounds (-180,-90,180,90)
        size=(pixels, pixels),  # Image size
        # time='2021-09-21',  # Time of data
        format="image/png",  # Image format
        transparent=True,
    )  # Nodata transparency

    # Save output PNG to a file

    out = open(f"{output_path}.png", "wb")
    out.write(img.read())
    out.close()


# download_image(-71.060909, 42.358386, "image_analysis/satelite_images/boston")
