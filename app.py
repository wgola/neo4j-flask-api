from flask import Flask, jsonify

from connect_db import connect_db

DRIVER = connect_db()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def test():
    return jsonify({'test': 'test'})


if __name__ == '__main__':
    app.run()
