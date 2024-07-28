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
from firebase import storage # local firebase object


# for url
url = storage.child(constants.PATH_ON_CLOUD).get_url(constants.TOKEN)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "What’s are the raw ingredients in this image? I need you to put these in a string format. think through it and make sure that all of the items you identify are what they are. not just based on their labels or company names. "},
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

print(response.choices[0].message.content)
