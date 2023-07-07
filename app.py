from flask import Flask, request, jsonify
import pickle
import numpy as np
import git 
app = Flask(__name__)

# Route for the GitHub webhook

@app.route('/git_update', methods=['POST'])
def git_update():
    repo = git.Repo('./py.anywhere')
    origin = repo.remotes.origin
    repo.create_head('main',
                     origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
    origin.pull()
    return '', 200

@app.route('/',methods=['GET'])
def home_page():
    message="Hola mundo"
    response={"message":message}
    return jsonify({"response":response}), 200

if __name__ == '__main__':
    app.run()

