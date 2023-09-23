# Puzzle Diffusion - Generative Image Puzzle Game

## Description

This is just a simple game inspired by [this tweet](https://twitter.com/outofai/status/1703175389676179947). All kudos for the idea go to the author of the tweet and many people who have recently shared their ControlNet image experiments.

The game is built using the Stable Diffusion and ControlNet models, which are used to generate images from a description provided by the player. Each image is randomly generated but follows a chessboard pattern. The generated image is then divided into tiles along the pattern lines and shuffled to create a puzzle. The player can then solve the puzzle by rearranging the tiles to form the original image.

[Demo](https://github.com/IliaLarchenko/puzzle_diffusion/assets/41329713/ca89a1d3-ea53-4177-85b6-86d6d3616a25)

## Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/IliaLarchenko/puzzle_diffusion.git
   cd puzzle_diffusion
   ```

2. **Configure Settings**

   Before running the setup script, you may need to configure the game settings in `config.json`. 
   Make sure to set the `device` parameter according to the availability of CUDA or MPS on your system.

   - `device`: The device to be used: "cuda" for NVIDIA GPUs, "mps" for Apple GPUs. You will not be able to generate images on a CPU.
   - `high_speed_mode`: A boolean value indicating whether to use high-speed mode. In this mode the image generation will be significantly faster, but the generated image will have much lower quality.
   - `use_saved_image`: If you don't want to generate image in real time but want to play the puzzle using existing image, set this parameter to `true`. You will also need to specify the path to the saved image in the next parameter.
   - `saved_image_path`: The path to the saved image if `use_saved_image` is true.


3. **Run Setup Script**

   ```sh
   ./setup.sh
   ```

   This script will create a virtual environment, install the necessary dependencies, and run a test to ensure everything is set up correctly.
   Make sure this step doesn't throw any errors, otherwise the game will not run.
   It will also tell you the time taken for image generation on your system for reference.

4. **Start the Game**

   ```sh
   source .venv/bin/activate
   python game.py
   deactivate
   ```

## How to Play

1. **Start the Game**: After running `game.py`, you will be prompted to enter a description of the image and the number of tiles (width and height).

2. **Solve the Puzzle**: The generated image will be divided into shuffled tiles. Your task is to rearrange the tiles by clicking and swapping them to form the complete image. The selected tile will be highlighted.

3. **Complete the Game**: Upon completing the puzzle, a congratulatory message will be displayed along with options to play again with the same or a new image, or to exit the game.

## Configuration Parameters

- `sd_model`: Specifies the stable diffusion model to be used for image generation. You can use either HuggingFace or local paths to the model.
- `cn_model`: Specifies the control net model to be used along with the stable diffusion model. You can use either HuggingFace or local paths to the model.
- `device`: Sets the device for computation ("cuda" for NVIDIA GPUs, "mps" for Apple GPUs, CPU is not supported).
- `prompt_suffix`: A suffix string to be added to the image prompt for more details.
- `negative_prompt`: A string containing negative prompts to avoid certain characteristics in the generated image.
- `high_speed_mode`: Boolean, if true, reduces the inference steps making image generation faster but significantly reducing the quality of the image. Not recommended for use.
- `use_saved_image`: Boolean, if true, the game will use a saved image from `saved_image_path` instead of generating a new one.
- `saved_image_path`: Specifies the path to the saved image to be used if `use_saved_image` is true.

## Project Files

- `game.py`: The main script to run the game.
- `image.py`: Contains functions for generating the images.
- `config.json`: Configuration file for the game.
- `setup.sh`: Setup script for creating a virtual environment and installing dependencies.
- `requirements.txt`: List of dependencies for the project.
- `test.py`: Script to test the image generation functionality and measure the time taken.

## Acknowledgements

The code for this project was developed with the assistance of Copilot and ChatGPT from OpenAI.

## Additional Notes

Ensure that your system meets the requirements for the chosen device in the configuration. If you're using "cuda", make sure that NVIDIA CUDA is installed. If you're using "mps", ensure that you're on macOS and have the necessary dependencies for MPS.

Feel free to contribute to this project or raise issues if you encounter any problems. Enjoy the game!
