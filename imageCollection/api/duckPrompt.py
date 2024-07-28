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

import pymongo

client = pymongo.MongoClient(os.getenv("MONGODB_URI"))
db = client["prompts"]
collection= db["prompts"]

def getResponseBack(prompt, ingredientList, recipes):

  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

  past_prompts = [document for document in collection.find({})]
  print(past_prompts)

  prompt = f"You are a food planning assitant that is a master chef. You are given your past prompts {past_prompts} (to remember what your client asked you) and a list of ingredients {ingredientList} that are available in the clients fridge. You are also given a list of recipes {recipes} that best uses the ingredients. Use the relavant information to answer the question your client has asked you. Do NOT make up your own recipes or ingredients. But, you need to address the client's question based on what has been privoded before. The question the client asks is: {prompt}. All the information you need is in the past prompts, ingredients, and recipes. This is a chatbot, so your answered should be very conversational and helpful to the client. moreover, don't keep it more than 1-2 sentences long and speech time should be less than 5 seconds."

  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "user",
        "content": [
          {"type": "text", "text": prompt},
        ],
      }
    ],
    max_tokens=1000,
  )


  collection.insert_one({"prompt": prompt, "response": response.choices[0].message.content, "ingredients": ingredientList, "recipes": recipes})
  print("inserted")
  return(response.choices[0].message.content + " Quack!")

if __name__ == "__main__":
  print(getResponseBack())