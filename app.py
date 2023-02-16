# $Web Calendar 1/4
import sys
from flask import Flask
from flask import request
from flask import jsonify
from flask_restful import Api, Resource


app = Flask(__name__)  # Create a Flask application object
api = Api(app)  # create an API object that accepts a flask application object as an argument


class HelloWorldResource(Resource):
    """ class that extends the Resource class from the flask_restful module"""
    def get(self):
        """parse a GET request to a specific endpoint"""
        # return {"message": "Hello from the REST API!"}
        message = jsonify({"data": "There are no events for today!"})
        return message


# api.add_resource(HelloWorldResource, '/hello')
api.add_resource(HelloWorldResource, '/event/today')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
