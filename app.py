from flask import Flask, jsonify, request

from connectDB import connectDB

driver = connectDB()

app = Flask(__name__)


@app.route('/', methods=['GET'])
def test():
    return jsonify({'test': 'test'})


if __name__ == '__main__':
    app.run()
