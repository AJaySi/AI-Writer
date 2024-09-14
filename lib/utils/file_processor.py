import os
import base64
import streamlit as st

def load_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode()
    return b64_string

def read_prompts(file_path="prompt_llm.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            prompts = file.readlines()
        return [prompt.strip() for prompt in prompts]
    return []

def write_prompts(prompts, file_path="prompt_llm.txt"):
    with open(file_path, "w") as file:
        for prompt in prompts:
            file.write(f"{prompt}\n")
