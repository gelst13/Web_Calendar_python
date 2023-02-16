# $Web Calendar 3/4
# store and access events
import sys
from flask import Flask
from flask import request
from flask import jsonify
from flask_restful import Api, Resource, reqparse, inputs
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)  # Create a Flask application object
api = Api(app)  # create an API object that accepts a flask application object as an argument
app.config.from_object('config')

parser = reqparse.RequestParser()
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)
parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)


# class WebCalendarResource(Resource):
#     """ class that extends the Resource class from the flask_restful module"""
#     def get(self):
#         """parse a GET request to a specific endpoint"""
#         # return {"message": "Hello from the REST API!"}
#         message = jsonify({"data": "There are no events for today!"})
#         return message
# api.add_resource(WebCalendarResource, '/event/today')

class HelloWorldResource(Resource):
    def get(self):
        args = parser.parse_args()
        response = {
            "message": "The event has been added!",
            "event": args['event'],
            "date": str(args['date'].date())
        }
        return response

    def post(self):
        args = parser.parse_args()
        return args['event']


api.add_resource(HelloWorldResource, '/event')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
