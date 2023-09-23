import torch
from diffusers import ControlNetModel, StableDiffusionControlNetPipeline, UniPCMultistepScheduler
from PIL import Image, ImageDraw


def generate_pattern(tile_size=128, shape=(4, 4)):
    width, height = shape[1] * tile_size, shape[0] * tile_size
    colors = [(0, 0, 0), (255, 255, 255)]  # Black and white colors

    # Create a new image with white background
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # Draw squares
    for i in range(shape[1]):
        for j in range(shape[0]):
            color = colors[(i + j) % 2]
            x0, y0 = i * tile_size, j * tile_size
            x1, y1 = x0 + tile_size, y0 + tile_size
            draw.rectangle([x0, y0, x1, y1], fill=color)

    return img


def generate_image(prompt, tiles_count, tile_size, config):
    sd_model = config.get("sd_model", "runwayml/stable-diffusion-v1-5")
    cn_model = config.get("cn_model", "monster-labs/control_v1p_sd15_qrcode_monster")
    device = config.get("device", "cuda")
    negative_prompt = config.get("negative_prompt", "")
    
    controlnet = ControlNetModel.from_pretrained(cn_model)
    pipeline = StableDiffusionControlNetPipeline.from_pretrained(sd_model, controlnet=controlnet)
    
    if device == "mps":
        pipeline.to("mps")
        generator = None
    else:
        generator = torch.manual_seed(0)
        pipeline.scheduler = UniPCMultistepScheduler.from_config(pipeline.scheduler.config)
        pipeline.enable_model_cpu_offload()

    pattern = generate_pattern(tile_size=tile_size, shape=(tiles_count, tiles_count))
    num_inference_steps = 25 if config.get("high_speed_mode", False) else 100

    image = pipeline(
        prompt + config.get("prompt_suffix", ""),
        image=pattern,
        negative_prompt= negative_prompt,
        controlnet_conditioning_scale=0.9,
        num_inference_steps=num_inference_steps,
        guidance_scale=9,
        num_images_per_prompt=1,
        generator=generator
    ).images[0]

    return image

