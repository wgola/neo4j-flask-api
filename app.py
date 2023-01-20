from flask import Flask, jsonify, request
from app_services import app_services

from connect_db import connect_db

DRIVER = connect_db()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def welcome_page():
    return "neo4j+flask api"


@app.route("/employees", methods=['GET'])
def get_all_employees():
    args = request.args
    with DRIVER.session() as session:
        employees = session.execute_read(
            app_services.get_all_employees, args)

    response = {"employees": employees}

    return jsonify(response), 200


@app.route("/employees", methods=['POST'])
def create_employee():
    try:
        employee_data = request.json
        name = employee_data["name"]
        surname = employee_data["surname"]
        position = employee_data["position"]
        department = employee_data["department"]
        type = employee_data["type"]
    except:
        return jsonify({"message": "Wrong employee data provided"}), 500

    with DRIVER.session() as session:
        if_unique = session.execute_read(
            app_services.check_if_unique_name_and_surname, name, surname)

        if not if_unique:
            return jsonify({"message": "User with that name and surname already exists"}), 500

        if_created = session.execute_write(
            app_services.create_employee, name, surname, position, department, type)

        if if_created:
            return jsonify({"message": "Employee created"}), 201

    return jsonify({"message": "Coulnd't create employee"}), 500


if __name__ == '__main__':
    app.run()
