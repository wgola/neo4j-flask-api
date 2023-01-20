class app_services():
    @staticmethod
    def get_all_employees(tx, args):
        name = args.get("name")
        surname = args.get("surname")
        position = args.get("position")
        sort_by = args.get("sort_by")
        order = args.get("order", default="asc")

        final_query = "MATCH (m:Employee) RETURN m"

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
            final_query = "MATCH (m:Employee) {} RETURN m".format(match_query)

        if sort_by:
            final_query += " ORDER BY m." + \
                sort_by.strip(' " " ') + " " + order.upper()

        results = tx.run(final_query).data()
        employees = [result['m'] for result in results]

        return employees

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
