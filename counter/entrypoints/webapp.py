from io import BytesIO

from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint

from counter import config

app = Flask(__name__)

count_action = config.get_count_action()
prediction_action = config.get_prediction_action()


@app.route('/object-count', methods=['POST'])
def object_detection():
    uploaded_file = request.files['file']
    model_name = request.form.get('model_name', "rfcn")
    threshold = float(request.form.get('threshold', 0.5))
    image = BytesIO()
    uploaded_file.save(image)
    count_response = count_action.execute(image, threshold, model_name)
    return jsonify(count_response)


@app.route("/object-predict", methods=["POST"])
def object_predict():
    uploaded_file = request.files["file"]
    threshold = float(request.form.get("threshold", 0.5))
    model_name = request.form.get('model_name', "rfcn")
    image = BytesIO()
    uploaded_file.save(image)
    prediction_response = prediction_action.execute(image, threshold, model_name)
    return jsonify(prediction_response)


@app.route("/openapi.yml")
def openapi():
    return send_from_directory("../resources", "openapi.yml")


SWAGGER_URL = ''  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/openapi.yml'  # Our API url (can of course be a local resource)


swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Test application"
    },
)

app.register_blueprint(swaggerui_blueprint)


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
