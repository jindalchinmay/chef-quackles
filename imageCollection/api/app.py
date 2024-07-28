# set directory to the /imageCollection to then import the firebase object
import os.path as op
import sys
from dotenv import load_dotenv
import os
path  = op.dirname(op.dirname(op.realpath(__file__)))
sys.path.append(path)
load_dotenv()

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dataprep.query import AstraDB
from api.chat_api import get_ingredients
from duckPrompt import getResponseBack
from api.img_gen import get_image
import constants
import logging
import requests

import pymongo

import cohere 
co = cohere.Client(os.getenv("COHERE_API_KEY"))

app = Flask(__name__)
astradb = AstraDB()
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def home():
    return "Hello World"

@app.route('/api/recipe', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        data = request.get_json()
        ingredientList = data.get('params')
        # app.logger.debug(f"Received params: {ingredientList}")
        if isinstance(ingredientList, list):
            results = astradb.get_query(ingredientList, 2 * constants.LIMIT)
            results = [document for document in results]
           
            app.logger.debug(f"Query results: {len(results)}")
            query = ", ".join(ingredientList)

            mapping = {document["$vectorize"]: document for document in results}
            docs = [i for i in mapping]
            
            reranked = co.rerank(query=query, documents=docs, top_n=constants.LIMIT, model="rerank-english-v3.0")
            results = [ mapping[docs[document.index]] for document in reranked.results]
            return jsonify({'message': 'success', 'data': results}), 200
        else:
            return jsonify({'message': 'error', 'error': 'Invalid data format: params should be a list'}), 400

@app.route('/api/ingredients', methods=['POST'])
def handle_post_2():
    if request.method == 'POST':

        response = requests.get(os.getenv("RASP_IP_ADDRESS") + "/take_photo")
        if response.status_code == 200:
            ingredientList = get_ingredients()
            return jsonify({'message': 'success', 'data': ingredientList}), 200
        else :
            return jsonify({'message': 'error', 'error': 'Invalid data format: params should be a list'}), 400

@app.route('/api/getImages', methods=['POST'])
def handle_post_3():

    if request.method == 'POST':
        data = request.get_json()
        ids = data.get('ids')
        app.logger.debug(f"Received params: {ids}")
        names = [astradb.get_name(id) for id in ids]
        urls = get_image(names)
        return jsonify({'message': 'success', 'data': urls}), 200

@app.route('/api/duck', methods=['POST'])
def handle_post_4():
    if request.method == 'POST':


        client2 = pymongo.MongoClient(os.getenv("MONGODB_URI"))
        db2 = client2["prompts"]
        collection2 = db2["prompts"]

        number = collection2.count_documents(filter={})


        data = request.get_json()
        message = data.get('prompt')
        app.logger.debug(f"Received params: {message}")
        if number == 0:
            response = requests.get(os.getenv("RASP_IP_ADDRESS") + "/take_photo")
            if response.status_code == 200:
                ingredientList = get_ingredients()
        else:
            ingredientList = collection2.find_one({})["ingredients"]

        client2.close()
        print(ingredientList)
        

        recipes = astradb.get_query(ingredientList, constants.LIMIT)
        recipes = [document for document in recipes]

        response_result = getResponseBack(message, ingredientList, recipes)

        return jsonify({'message': 'success', 'data': response_result}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("FLASK_PORT"), debug=True)
