# Prediction interface for Cog ⚙️
# https://github.com/replicate/cog/blob/main/docs/python.md

from cog import BasePredictor, Input, Path
from diffusers import (
    StableDiffusionXLInpaintPipeline,
    DDIMScheduler,
    DPMSolverMultistepScheduler,
    EulerAncestralDiscreteScheduler,
    EulerDiscreteScheduler,
    HeunDiscreteScheduler,
    PNDMScheduler,
)
from diffusers.utils import load_image
import torch
import os
import shutil
from safetensors.torch import load_file

SDXL_MODEL_CACHE = "sdxl-cache"


class KarrasDPM:
    def from_config(config):
        return DPMSolverMultistepScheduler.from_config(config, use_karras_sigmas=True)


SCHEDULERS = {
    "DDIM": DDIMScheduler,
    "DPMSolverMultistep": DPMSolverMultistepScheduler,
    "HeunDiscrete": HeunDiscreteScheduler,
    "KarrasDPM": KarrasDPM,
    "K_EULER_ANCESTRAL": EulerAncestralDiscreteScheduler,
    "K_EULER": EulerDiscreteScheduler,
    "PNDM": PNDMScheduler,
}


def get_image(path):
    if(path is None):
        return None
    shutil.copyfile(path, "/tmp/image.png")
    return load_image("/tmp/image.png").convert("RGB")

class Predictor(BasePredictor):
    def setup(self) -> None:
        """Load the model into memory to make running multiple predictions efficient"""
        pipeline = StableDiffusionXLInpaintPipeline.from_pretrained(
            SDXL_MODEL_CACHE,
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True,
        ).to("cuda")
        # PUT the LORA model into memory
        lora_model_path = ""
        pipeline.load_lora_weights(".", weight_name = lora_model_path)
        self.__pipe = pipeline

    @torch.inference_mode()
    def predict(
        self,
        prompt: str = Input(
            description="Input prompt",
            default="An astronaut riding a rainbow unicorn",
        ),
        negative_prompt: str = Input(
            description="Input Negative Prompt",
            default="",
        ),
        image: Path = Input(
            description="Input image for img2img or inpaint mode",
            default=None,
        ),
        num_inference_steps: int = Input(
            description="Number of denoising steps",
            ge=1,
            le=500,
            default=40
        ),
        guidance_scale: float = Input(
            description="Scale for classifier-free guidance",
            ge=1,
            le=50,
            default=7
        ),
        prompt_strength: float = Input(
            description="Prompt strength when using img2img / inpaint. 1.0 corresponds to full destruction of information in image",
            ge=0.0,
            le=1.0,
            default=0.36,
        ),
        seed: int = Input(
            description="Random seed. Leave blank to randomize the seed",
            default=None
        ),
        scheduler: str = Input(
            description="scheduler",
            choices=SCHEDULERS.keys(),
            default="DPMSolverMultistep",
        ),
        width: int = Input(
            description="Width of output image",
            default=512,
        ),
        height: int = Input(
            description="Height of output image",
            default=512,
        ),
    ) -> Path:
        """Run a single prediction on the model"""
        if seed is None:
            seed = int.from_bytes(os.urandom(2), "big")
        generator = torch.Generator("cuda").manual_seed(seed)
        print(f"Using seed: {seed}")

        self.__pipe.scheduler = SCHEDULERS[scheduler].from_config(self.__pipe.scheduler.config)
        print(f"desired height and width of the generated image: {height}x{width}")

        images = self.__pipe(
            prompt=prompt,
            negative_prompt=negative_prompt,
            image=get_image(image),
            mask_image=get_image('mask.png'),
            guidance_scale=guidance_scale,
            num_inference_steps=num_inference_steps,
            strength=prompt_strength,
            generator=generator,
            height=height,
            width=width,
        ).images

        output_path = f"/tmp/out.png"

        images[0].save(output_path)
        print(output_path)

        return Path(output_path)
