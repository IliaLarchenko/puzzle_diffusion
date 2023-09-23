from PIL import Image

def generate_image(prompt, tiles, tile_size):
    """Generates an image based on the prompt and tiles."""
    image = Image.open("temp_img.png")
    return image

if __name__ == "__main__":
    img = generate_image("test", (3,3), 100)
    img.save("test.png")