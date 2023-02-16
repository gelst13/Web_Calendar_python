# $Web Calendar 3/4: store and access events
import sys
from datetime import date
from flask import Flask
from flask_restful import Api, Resource, reqparse, inputs, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)  # Create a Flask application object
api = Api(app)  # create an API object that accepts a flask application object as an argument
app.config.from_object('config')
db = SQLAlchemy(app)


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date, nullable=False)


with app.app_context():
    db.create_all()


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


resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.String
}


class TodayResource(Resource):
    """ class that extends the Resource class from the flask_restful module"""
    @marshal_with(resource_fields)
    def get(self):
        """return the list of today's events"""
        today_events = db.session.execute(
            db.select(Event.id, Event.event, Event.date).filter_by(date=date.today())).all()
        print(today_events)
        response = []
        for entry in today_events:
            response.append(Event(id=entry.id, event=entry.event, date=entry.date))

        return response


api.add_resource(TodayResource, '/event/today')


class EventResource(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        """return all the events from the database"""
        db_events = db.session.execute(db.select(Event.id, Event.event, Event.date)).all()
        response = []
        for entry in db_events:
            response.append(Event(id=entry.id, event=entry.event, date=entry.date))

        return response

    def post(self):
        """save the event to your database"""
        args = parser.parse_args()
        new_event = Event(event=args['event'], date=args['date'])
        db.session.add(new_event)
        db.session.commit()
        return args['event']


api.add_resource(EventResource, '/event')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
