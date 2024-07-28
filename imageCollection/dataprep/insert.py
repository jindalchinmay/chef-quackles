import os
from dotenv import load_dotenv
load_dotenv()
from astrapy import DataAPIClient
from astrapy.constants import VectorMetric
from astrapy.ids import UUID
from astrapy.exceptions import InsertManyException
import pandas as pd
import numpy as np
import re

#data prep
recipes = pd.read_csv("./RAW_recipes.csv")
recipesDict = recipes.to_dict()
columns = recipes.columns.to_numpy()
recipesDict["vectorized"] = {i: re.sub(r"'([^']*)'", r"\1", recipesDict["ingredients"][i][1:-1] + ", " + recipesDict["tags"][i][1:-1]) for i in range(231637)}

#connect to db
client = DataAPIClient("AstraCS:tTsdbxgQOMByHTMDIatCneZl:31973df4789f92efdacb2612c8a035d62759164eb3bb7122499f9670c14c0e7d")
db = client.get_database_by_api_endpoint(
  "https://ece512b0-13c6-4ea2-9da8-65b4f99b50bd-us-east-2.apps.astra.datastax.com"
)
print(f"Connected to Astra DB: {db.list_collection_names()}")
collection = db.get_collection("recipes_db")

#document insert
documents = []
for i in range(len(recipesDict['name'])):
    document = {
        "_id": i,
        "time":recipesDict['minutes'][i],
        "nutrition":recipesDict['nutrition'][i],
        "recipe": recipesDict['steps'][i],
        "ingredients": recipesDict['ingredients'][i],
        "tags": recipesDict['tags'][i],
        "name": recipesDict['name'][i],
        "$vectorize": recipesDict['vectorized'][i],
    }

    if len(recipesDict['steps'][i].encode('utf-8')) <= 8000:
        documents.append(document)


l = len(documents)

import math
constant = 10000
for i in range(1,math.ceil(l/constant)):
    if (constant*(i+1) < l):
        response  = collection.insert_many(documents[i*constant: constant*(i+1)])
    else:
        response = collection.insert_many(documents[i*constant: l])

    print("done, ", i/math.ceil(l/constant))