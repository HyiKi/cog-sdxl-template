# Cog SDXL Template

English/[中文](README_ZH.md)

## Introduction

This is a [Cog](https://github.com/replicate/cog) model for [Replicate](https://replicate.com/) which works great for me.

To use it locally or before pushing your own fork you first have to download the weights by running the following command: `cog run scripts/download_weights.py`.

## GUIDE

1. Clone the repository using either of the following commands:
   - `git clone https://github.com/HyiKi/cog-sdxl-template/tree/main`
   - `gh repo clone HyiKi/cog-sdxl-template`

2. Install the required dependencies by running the command: `pip install -r requirements.txt`.

3. Set the values for `SDXL_MODEL_CACHE` and `lora_model_path` according to your requirements.

4. Download the weights by running the command: `cog run scripts/download_weights.py`.

5. Follow the instructions provided in the [Push a model to Replicate](https://replicate.com/docs/guides/push-a-model) guide to push your model to Replicate.
