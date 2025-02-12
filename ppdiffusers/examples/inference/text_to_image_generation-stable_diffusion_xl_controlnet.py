# Copyright (c) 2023 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cv2
import numpy as np
import paddle
from PIL import Image

from ppdiffusers import (
    AutoencoderKL,
    ControlNetModel,
    StableDiffusionXLControlNetPipeline,
)
from ppdiffusers.utils import load_image
prompt = " anime artwork {prompt} . anime style,  a panda walk through a snowy winter landscape, traversing a bamboo forest blanketed in ice and snow."
negative_prompt = "blurry, low quality, distorted, text, watermark, extra limbs, deformed hands, overexposed, underexposed, low detail"

image = load_image(
   "/root/paddlejob/workspace/env_run/output/haoming/fork/PaddleMIX/ppdiffusers/examples/ppvctrl/examples/canny/case4/control_image.jpg"
)

controlnet_conditioning_scale = 0.85  # recommended for good generalization

controlnet = ControlNetModel.from_pretrained("diffusers/controlnet-canny-sdxl-1.0", paddle_dtype=paddle.float16)
vae = AutoencoderKL.from_pretrained("madebyollin/sdxl-vae-fp16-fix", paddle_dtype=paddle.float16)
pipe = StableDiffusionXLControlNetPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    controlnet=controlnet,
    vae=vae,
    paddle_dtype=paddle.float16,
    generator=paddle.Generator().manual_seed(42),
)

images = pipe(
    prompt,
    negative_prompt=negative_prompt,
    image=image,
    controlnet_conditioning_scale=controlnet_conditioning_scale,
).images

images[0].save("text_to_image_generation-stable_diffusion_xl_controlnet_result.png")
