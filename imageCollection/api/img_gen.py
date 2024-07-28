# set directory to the /imageCollection to then import the firebase object
import os.path as op
import sys
from dotenv import load_dotenv
import os
path  = op.dirname(op.dirname(op.realpath(__file__)))
sys.path.append(path)
load_dotenv()

import requests
import constants
from firebase import storage
from openai import OpenAI

import prompts 
from datetime import datetime
import time 

def get_image(names):

    # DON'T RUN THIS: COSTS $0.04 cents per image!
    client = OpenAI(api_key=os.getenv("OPENAI_API"))

    urls = []

    for index, name in enumerate(names):

        response = client.images.generate(
            model="dall-e-3",
            prompt="give me a picture of the following recipie title: ," + name + ". i need it like a professional birdseye view or some other camera shot, like in a bowl or a cover page for the dish. ",
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url
        response = requests.get(image_url)

        response = requests.get(image_url)
        path = str(index) + constants.LOCAL_FILE_DALLE

        with open(path, "wb") as file:
            file.write(response.content)
        
        # check if the file exists in the storage and delete it
        
        storage.child(path).put(path)
        url = storage.child(path).get_url(datetime.now())
        urls.append(url)

    return urls
