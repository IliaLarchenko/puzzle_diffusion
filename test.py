import json
import time
from image import generate_image
from PIL import Image

if __name__ == "__main__":
    try:
        # Load the configuration from the config.json file
        with open("config.json", "r") as file:
            config = json.load(file)
        
        # Construct the prompt using the base description and the suffix from the config
        prompt = "Astronaut riding a skateboard on the moon"
        tiles_count = 4
        tile_size = 128
        
        # Adjust the tile size if high_speed_mode is enabled
        if config.get("high_speed_mode", False):
            tile_size //= 2
        
        # Start the timer
        start_time = time.time()
        
        # Generate the image
        image = generate_image(prompt, tiles_count, tile_size, config)
        
        # Stop the timer
        end_time = time.time()
        
        # Calculate the elapsed time
        elapsed_time = end_time - start_time
        
        # Save the generated image
        image.save("test.png")
        
        print("Image generated successfully!")
        print(f"Time taken to generate the image: {elapsed_time:.2f} seconds")
        
    except Exception as e:
        print(f"Error: {e}")
