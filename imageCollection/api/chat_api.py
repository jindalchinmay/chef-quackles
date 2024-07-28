# set directory to the /imageCollection to then import the firebase object
import os.path as op
import sys
from dotenv import load_dotenv
import os
path  = op.dirname(op.dirname(op.realpath(__file__)))
sys.path.append(path)
load_dotenv()

from openai import OpenAI
import constants
import prompts
from firebase import storage # local firebase object



def get_ingredients():

  url = storage.child(constants.PATH_ON_CLOUD).get_url(constants.TOKEN)
  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "user",
        "content": [
          {"type": "text", "text": prompts.GET_INGREDIENTS_PROMPT},
          {
            "type": "image_url",
            "image_url": {
              "url": url,
            },
          },
        ],
      }
    ],
    max_tokens=300,
  )

  return(response.choices[0].message.content)

if __name__ == "__main__":
  print(get_ingredients())