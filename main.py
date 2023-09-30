import gradio as gr
import torch
from PIL import Image
import langchain
from prompts import teenage_gujarati, teenage_american, teenage_marathi
import numpy as np
import os

from transformers import BlipProcessor, BlipForConditionalGeneration
import requests

# Loading the Models 
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
caption_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")


# Query OpenAI
def req_ai(query: str = ""):
    llm_url = "https://api.openai.com/v1/completions"
    OPEN_AI_KEY = os.getenv('openai_key')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPEN_AI_KEY}',
    }

    json_data = {
        'model': 'gpt-3.5-turbo-instruct',
        'prompt': query,
        'max_tokens': 50,
        'temperature': 0.2,
    }

    res = requests.post('https://api.openai.com/v1/completions', headers=headers, json=json_data)
    
    if res.status_code != 200:
        return "Wait for 30 Secs"
    
    print(f"RESPONSE : {res}, {res.json()}")
    res = res.json()
    res = res['choices'][0]['text']
    return res


# GRADIO Webview Tempalte
def greet(img,img_cap):

    # print(f"IMAGE CAPTION : {img_cap}")


    text = "a image of"
    inputs = processor(img, text, return_tensors="pt").to("cuda")

    out = caption_model.generate(**inputs)
    img_text = processor.decode(out[0], skip_special_tokens=True)
    query = teenage_gujarati.format(img_text = img_text, img_caption = img_cap)
    query_2 =  teenage_american.format(img_text = img_text, img_caption = img_cap)
    query_3 =  teenage_marathi.format(img_text = img_text, img_caption = img_cap)

    # print(f"IMAGE QUERY : {query}")


    res = req_ai(query)
    res_2 = req_ai(query_2)
    res_3 = req_ai(query_3)
    print(f"RESPONSE : {res}")
    msg = f"""Jinesh: {res}\nPeterson: {res_2}\nAarav: {res_3}"""
    return msg


demo = gr.Interface(fn=greet, inputs=["image","text"], outputs="textbox")
demo.launch()  