from PIL import Image
from openai import CLIP

import io

clip = CLIP() # Create a CLIP object, which will be used to generate the random images.

def generate_random_image():
    image_data = clip.generate(
        model="image-alpha-001",
        size=10,
        input_type="random"
    )

    # Create a file-like object from the image data
    image_file = io.BytesIO(image_data)

    # Use the file-like object with the Image.open() method
    image = Image.open(image_file)

    return image

def combine_images(images):
    width = 10 * len(images)  # <-- add this line
    height = 10
    combined_image = Image.new("RGB", (width, height))
    x_offset = 0
    for image in images:
        combined_image.paste(image, (x_offset, 0))
        x_offset += 10
    return combined_image



panel_images = [generate_random_image() for _ in range(10)] # Generate 10 random images.
panel = combine_images(panel_images) # Combine the images into a panel.
panel.save("panel.png") # Save the panel image to a file.
