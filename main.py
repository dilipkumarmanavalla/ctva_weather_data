import os
import logging
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from ctva_src import utils
from ctva_src.ctva import load_data
from ctva_src.data_models import db, WeatherData, WeatherStats
from settings import load_settings

config = load_settings(os.getenv("CURRENT_ENV", 'test'))
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{config["DB_USER"]}:{config["DB_PASSWORD"]}@{config["DB_HOST"]}/{config["DB_NAME"]}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config["SQLALCHEMY_TRACK_MODIFICATIONS"]

db.init_app(app)
swagger = Swagger(app)
repo = utils.clone_repo(config)

@app.route('/load/', methods=['GET'])
def load():
    response = load_data(repo, config, db, WeatherData, WeatherStats)
    if response['status']=='error':
        return jsonify(response), 500
    return jsonify(response), 200



@app.route('/health/', methods=['GET'])
def health():
    return jsonify({'Status': 'Up and Running'}), 200

if __name__ == '__main__':
    app.run(debug=True)
