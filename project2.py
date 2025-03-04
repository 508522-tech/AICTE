import requests
import json
import time

# Define the ComfyUI API URL
COMFYUI_URL = "http://127.0.0.1:8188/prompt"

# Define the workflow (JSON request)
workflow = {
    "prompt": {
        "0": {  # Load Checkpoint (Stable Diffusion Model)
            "inputs": {
                "ckpt_name": "v1-5-pruned-emaonly.safetensors"
            },
            "class_type": "CheckpointLoaderSimple"
        },
        "1": {  # Encode Text (Positive Prompt)
            "inputs": {
                "text": "A bustling cyberpunk city at night, filled with neon lights, flying cars, and towering skyscrapers, with a futuristic market scene.",
                "clip": "0"
            },
            "class_type": "CLIPTextEncode"
        },
        "2": {  # Encode Text (Negative Prompt)
            "inputs": {
                "text": "",  # Leave empty for no negative prompt
                "clip": "0"
            },
            "class_type": "CLIPTextEncode"
        },
        "3": {  # Empty Latent Image (512x512)
            "inputs": {
                "width": 512,
                "height": 512,
                "batch_size": 1
            },
            "class_type": "EmptyLatentImage"
        },
        "4": {  # KSampler (Image Generation)
            "inputs": {
                "model": "0",
                "positive": "1",
                "negative": "2",
                "latent_image": "3",
                "seed": 123456789,
                "steps": 20,
                "cfg": 8.0,
                "sampler_name": "euler",
                "scheduler": "normal",
                "denoise": 1.0
            },
            "class_type": "KSampler"
        },
        "5": {  # VAE Decode (Convert Latent to Image)
            "inputs": {
                "samples": "4",
                "vae": "0"
            },
            "class_type": "VAEDecode"
        },
        "6": {  # Save Image
            "inputs": {
                "images": "5",
                "filename_prefix": "comfyui_output"
            },
            "class_type": "SaveImage"
        }
    }
}

# Send request to ComfyUI API
response = requests.post(COMFYUI_URL, json=workflow)

# Check response status
if response.status_code == 200:
    print("Image generation request sent successfully!")
    print("Waiting for the image to be processed...")
    
    # Wait a few seconds for the image to be generated
    time.sleep(5)
    
    print("Check your ComfyUI output folder for the generated image.")
else:
    print("Error:", response.text)

