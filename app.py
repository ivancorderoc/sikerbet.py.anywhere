from flask import Flask, render_template, request, jsonify
import numpy as np
import os
import pickle
import subprocess

app = Flask(__name__)
root_path = "/home/sikerbet/sikerbet.py.anywhere/model/"

# Funcion para cargar el modelo y el encoder desde los archivos pickle
def load_model_and_encoder():
    model = pickle.load(open(root_path + "model.pkl", "rb"))
    encoder = pickle.load(open(root_path + "label_model.pkl", "rb"))
    return model, encoder

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/result", methods=['POST'])
def predict():
    float_features = [(x) for x in request.form.values()]

    # Cargar el modelo y el encoder
    model, encoder = load_model_and_encoder()

    # Reconvertir las tres columnas label encoded a sus representaciones originales en letras
    for i in range(-3, 0):
        encoded_value = float_features[i]
        if encoded_value in encoder.classes_:
            encoded_value = encoder.transform([encoded_value])[0]
        else:
            # Si el valor no esta; presente en el encoder, podemos manejarlo aqui;
            # Por ejemplo, podemos asignar un valor por defecto o simplemente ignorarlo
            encoded_value = 0 # Asignar un valor por defecto de ser necesario

        float_features[i] = encoded_value

    # Convertir los datos de entrada en un arreglo numpy
    final_features = np.array(float_features, dtype=float)

    # Realizar la prediccion utilizando el modelo cargado
    prediction = model.predict(final_features.reshape(1, -1))

    if prediction == 1:
        return render_template("result-1.html", prediction="THE HOME TEAM WILL WIN")
    else:
        return render_template("result-2.html", prediction="THE AWAY TEAM WILL WIN")

@app.route("/promo")
def promo():
    return render_template("promo.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/error")
def error():
    return render_template("error.html")

@app.route('/webhook', methods=['POST'])
def webhook():
    # Ruta al repositorio donde se realizará el pull
    path_repo = '/home/sikerbet/sikerbet.py.anywhere'
    servidor_web = '/var/www/sikerbet_pythonanywhere_com_wsgi.py' 

    # Comprueba si la solicitud POST contiene datos JSON
    if request.is_json:
        payload = request.json
        # Verifica si la carga útil (payload) contiene información sobre el repositorio
        if 'repository' in payload:
            # Extrae el nombre del repositorio y la URL de clonación
            repo_name = payload['repository']['name']
            clone_url = payload['repository']['clone_url']
            
            # Cambia al directorio del repositorio
            try:
                os.chdir(path_repo)
            except FileNotFoundError:
                return jsonify({'message': 'El directorio del repositorio no existe'}), 404

            # Realiza un git pull en el repositorio
            try:
                subprocess.run(['git', 'pull', clone_url], check=True)
                subprocess.run(['touch', servidor_web], check=True) # Trick to automatically reload PythonAnywhere WebServer
                return jsonify({'message': f'Se realizó un git pull en el repositorio {repo_name}'}), 200
            except subprocess.CalledProcessError:
                return jsonify({'message': f'Error al realizar git pull en el repositorio {repo_name}'}), 500
        else:
            return jsonify({'message': 'No se encontró información sobre el repositorio en la carga útil (payload)'}), 400
    else:
        return jsonify({'message': 'La solicitud no contiene datos JSON'}), 400


if __name__ == "__main__":
    app.run(port=8000)