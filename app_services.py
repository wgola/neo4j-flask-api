class app_services():
    @staticmethod
    def get_all_employees(tx, args):
        name = args.get("name")
        surname = args.get("surname")
        position = args.get("position")
        sort_by = args.get("sort_by")
        order = args.get("order", default="asc")

        final_query = "MATCH (m:Employee) RETURN m, ID(m)"

        queries = []
        if name:
            name_query = "m.name = {}".format(name)
            queries.append(name_query)

        if surname:
            surname_query = "m.surname = {}".format(surname)
            queries.append(surname_query)

        if position:
            position_query = "m.position = {}".format(position)
            queries.append(position_query)

        match_query = ""
        if queries:
            match_query = "WHERE {}".format(queries[0])
            for i in range(1, len(queries)):
                match_query += ", {}".format(queries[i])

        if match_query:
            final_query = "MATCH (m:Employee) {} RETURN m, ID(m)".format(
                match_query)

        if sort_by:
            final_query += " ORDER BY m." + \
                sort_by.strip(' " " ') + " " + order.upper()

        results = tx.run(final_query).data()
        employees = [{"id": result['ID(m)'], **result['m']}
                     for result in results]

        return employees

    @staticmethod
    def get_employee_by_id(tx, id):
        query = "MATCH (m:Employee) WHERE ID(m) = {} RETURN m, ID(m)".format(
            id)
        result = tx.run(query).data()

        if result:
            return {"id": result[0]['ID(m)'], **result[0]['m']}

        return {}

    @staticmethod
    def check_if_unique_name_and_surname(tx, name, surname):
        query = "MATCH (m:Employee) WHERE m.name = '{}' AND m.surname = '{}' RETURN m".format(
            name, surname)
        result = tx.run(query).data()

        return len(result) == 0

    @staticmethod
    def create_employee(tx, name, surname, position, department, type):
        employee_data = "{ " + "name: '{}', surname: '{}', position: '{}'".format(
            name, surname, position) + " }"

        relationship = ""
        if type == "manager":
            relationship = "-[r:MANAGES]->"
        else:
            relationship = "-[r:WORKS_INT]->"

        query = "MATCH (m:Department WHERE m.name = '{}') CREATE (n:Employee {}){}(m)".format(
            department, employee_data, relationship)

        result = tx.run(query).consume()

        if result['nodes_created'] == 1:
            return True

        return False

    @staticmethod
    def update_employee(tx, id, employe_data):
        name = employe_data.get("name")
        surname = employe_data.get("surname")
        position = employe_data.get("position")
        department = employe_data.get("department")
        type = employe_data.get("type")

        queries = []
        if name:
            name_query = "m.name = '{}'".format(name)
            queries.append(name_query)

        if surname:
            surname_query = "m.surname = '{}'".format(surname)
            queries.append(surname_query)

        if position:
            position_query = "m.position = '{}'".format(position)
            queries.append(position_query)

        set_query = ""
        if queries:
            set_query = "SET {}".format(queries[0])
            for i in range(1, len(queries)):
                set_query += ", {}".format(queries[i])

        update_data_query = ""
        if set_query:
            update_data_query = "MATCH (m:Employee) WHERE ID(m) = {} {}".format(
                id, set_query)

        delete_relationship_query = ""
        create_relationship_query = ""
        if department and type:
            relationship = ""
            if type == "manages":
                relationship = "-[r:MANAGES]->"
            else:
                relationship = "-[r:WORKS_IN]->"

            delete_relationship_query = "MATCH (m:Employee)-[r]->(n) WHERE ID(m) = {} DELETE r"
            create_relationship_query = "MATCH (m:Employee WHERE ID(m) = {}), (n: Department WHERE n.name = {}) CREATE (m){}(n)".format(
                id, department, relationship)

        result = []
        if update_data_query:
            result.append(tx.run(update_data_query).consume())

        if delete_relationship_query and create_relationship_query:
            tx.run(delete_relationship_query)
            result.append(tx.run(create_relationship_query).consume())

        if result:
            return True

        return False
