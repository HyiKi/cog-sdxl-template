# Cog SDXL 模板

[English](README.md)/中文

## 简介

这是一个适用于 [Replicate](https://replicate.com/) 的 [Cog](https://github.com/replicate/cog) 模型，对我来说非常好用。

在本地使用或在推送自己的分支之前，您首先需要通过运行以下命令下载权重：`cog run scripts/download_weights.py`。

## 使用指南

1. 使用以下命令之一克隆存储库：
   - `git clone https://github.com/HyiKi/cog-sdxl-template/tree/main`
   - `gh repo clone HyiKi/cog-sdxl-template`

2. 运行以下命令安装所需的依赖项：`pip install -r requirements.txt`。

3. 根据您的需求设置 `SDXL_MODEL_CACHE` 和 `lora_model_path` 的值。

4. 运行以下命令下载权重：`cog run scripts/download_weights.py`。

5. 按照 [推送模型到 Replicate](https://replicate.com/docs/guides/push-a-model) 指南中提供的说明将您的模型推送到 Replicate。