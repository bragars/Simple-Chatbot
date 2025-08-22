from flask import Flask, Blueprint, jsonify, request 
from flask_cors import CORS
from pymongo import MongoClient
from chatbot.chatbot import predict_class, get_response, intents, db
import os

from auth.auth import auth
from middleware_token import token_required
from bson.objectid import ObjectId
from database import db

# app.register_blueprint(auth)

app = Flask(__name__)
CORS(app)

SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret'
app.config['SECRET_KEY'] = SECRET_KEY

# Initialize MongoDB
# client = MongoClient(uri)  # or your Atlas URL
# app.config['DB'] = client["flask_db"]

# Register blueprints
from auth.auth import auth
app.register_blueprint(auth)

@app.route('/message', methods=['POST'])
@token_required
def post_data(current_user):
  content = request.json
  users = db.user
  messages = current_user['messages']

  data = { 'sender':'bot', 'content': 'teste de resposta' }
  messages.append({'sender': str(current_user['_id']), 'content': content['message']})
  messages.append(data)
  update = {"$set":{"messages": messages}}
  filterDb = {"_id": current_user["_id"]}
  users.update_one(filterDb, update)

  return jsonify(data)


@app.route('/chat', methods=['POST'])
def chat():
  data = request.get_json()
  message = data['message']
  print("message", message)
  ints = predict_class(message)
  print("ints", ints)
  res = get_response(ints, intents, message)

  return jsonify({'content': res, 'sender': 'bot'})

if __name__ == "__main__":
  app.run(debug = True)
