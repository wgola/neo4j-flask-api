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


@app.route("/employees/<int:id>", methods=['GET'])
def get_employee_by_id(id):
    with DRIVER.session() as session:
        employee = session.execute_read(
            app_services.get_employee_by_id, id)

    return jsonify(employee)


@app.route("/employees/<int:id>", methods=['PUT'])
def update_employee(id):
    employee_data = request.json

    with DRIVER.session() as session:
        if_updated = session.execute_write(
            app_services.update_employee, id, employee_data)

    if if_updated:
        return jsonify({"message": "Employee updated"}), 201

    return jsonify({"message": "Coulnd't update employee"}), 500


@app.route("/employees/<int:id>", methods=['DELETE'])
def delete_employee(id):
    with DRIVER.session() as session:
        if_deleted = session.execute_write(app_services.delete_employee, id)

    if if_deleted:
        return jsonify({"message": "Employee deleted"}), 201

    return jsonify({"message": "Coulnd't delete employee"}), 500


@app.route("/employees/<int:id>/subordinates", methods=['GET'])
def get_all_subordinates(id):
    with DRIVER.session() as session:
        if_manager = session.execute_read(app_services.check_if_manager, id)

        if if_manager:
            subordinates = session.execute_read(
                app_services.get_all_subordinates, id)

            if subordinates:
                return jsonify({"subordinates": subordinates}), 200

            return jsonify({"message": "There are no subordinates of this manager"}), 404

        return jsonify({"message": "This employee isn't manager"}), 404


@app.route("/employees/<int:id>/department", methods=['GET'])
def get_department_info(id):
    with DRIVER.session() as session:
        department_info = session.execute_read(
            app_services.get_department_info, id)

    return jsonify({"department": department_info}), 200


@app.route("/departments", methods=['GET'])
def get_departments():
    args = request.args
    with DRIVER.session() as session:
        departments = session.execute_read(
            app_services.get_all_departments, args)

    return jsonify({"departments": departments}), 200


@app.route("/departments/<int:id>", methods=['GET'])
def get_department_by_id(id):
    with DRIVER.session() as session:
        department = session.execute_read(
            app_services.get_department_by_id, id)

    if department:
        return jsonify({"department": department})

    return jsonify({"message": "There isn't department with this ID"}), 404


@app.route("/departments/<int:id>/employees")
def get_all_employees_of_department(id):
    with DRIVER.session() as session:
        employees = session.execute_read(
            app_services.get_all_employees_of_department, id)

    if employees:
        return jsonify({"employees": employees}), 200

    return jsonify({"message": "Couldn't find any employees"})


if __name__ == '__main__':
    app.run()
