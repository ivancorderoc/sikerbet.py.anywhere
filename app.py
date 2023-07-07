from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)
@app.route('/',methods=['GET'])
def home_page():
    message="Welcome to the Home Page"
    response={"message":message}
    return jsonify({"response":response}), 200

if __name__ == '__main__':
    app.run()

