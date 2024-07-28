import os
from astrapy import DataAPIClient
from astrapy.constants import VectorMetric
from astrapy.ids import UUID
from astrapy.exceptions import InsertManyException
import pandas as pd
import numpy as np
import re

class AstraDB:

  def __init__(self) -> None:
    self.client = DataAPIClient(os.getenv("DATASTAXCLIENT"))
    self.db = self.client.get_database_by_api_endpoint(
      os.getenv("DATASTAX_API_ENDPOINT")
    )
    print(f"Connected to Astra DB: {self.db.list_collection_names()}")
    self.collection = self.db.get_collection("recipes_db")

  def get_query(self, ingredientList, limit):
  #query request
    query = ", ".join(ingredientList)

    results = self.collection.find(
        sort={"$vectorize": query},
        limit=limit,
        projection={"$vectorize": True},
        include_similarity=True,
    )

    return results

  def get_name(self, id):
    return self.collection.find_one({"_id": id}, projection={"name": True})["name"]

#print query result
if __name__ == "__main__":
  db = AstraDB()
  query = db.get_query(["chicken", "rice", "soy sauce"])
  print(f"Vector search results for '{query}':")
  for document in query:
    print(document) 