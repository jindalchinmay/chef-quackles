import os
from astrapy import DataAPIClient
from astrapy.constants import VectorMetric
from astrapy.ids import UUID
from astrapy.exceptions import InsertManyException
import pandas as pd
import numpy as np
import re


#connect to db
client = DataAPIClient("AstraCS:tTsdbxgQOMByHTMDIatCneZl:31973df4789f92efdacb2612c8a035d62759164eb3bb7122499f9670c14c0e7d")
db = client.get_database_by_api_endpoint(
    "https://ece512b0-13c6-4ea2-9da8-65b4f99b50bd-us-east-2.apps.astra.datastax.com"
  )
print(f"Connected to Astra DB: {db.list_collection_names()}")
collection = db.get_collection("recipes_db")

  #query request
ingredientList = ["potato", "pepper", "chili", "tomato"]
query = ", ".join(ingredientList)

results = collection.find(
      sort={"$vectorize": query},
      limit=5, 
      projection={"$vectorize": True},
      include_similarity=True,
)


#print query result
print(f"Vector search results for '{query}':")
for document in results:
    print("    ", document)