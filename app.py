from flask import Flask, jsonify, request
from app_services import app_services

from connect_db import connect_db

DRIVER = connect_db()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome_page():
    return "neo4j+flask api"


@app.route("/employees", methods=['GEt'])
def get_all_employees():
    args = request.args
    with DRIVER.session() as session:
        employees = session.execute_read(
            app_services.get_all_employees, args)

    response = {"employees": employees}

    return jsonify(response)


if __name__ == '__main__':
    app.run()
