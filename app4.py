# $Web Calendar 4/4:
# add the ability to get a list of events for a certain time interval,
# find the event info by an ID, delete events from the database
import sys
from datetime import date
from flask import Flask, abort, jsonify, request
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
        response = []
        for entry in today_events:
            response.append(Event(id=entry.id, event=entry.event, date=entry.date))

        return response


api.add_resource(TodayResource, '/event/today')


class EventResource(Resource):
    @marshal_with(resource_fields)
    def get(self, **kwargs):
        """return all the events from the database or (if specified) within range like
        start_time=2020-10-10&end_time=2020-10-20 """
        response = []
        query_params = request.args  # returns a dictionary
        if not query_params:
            events_ = db.session.execute(db.select(Event.id, Event.event, Event.date)).all()
        else:
            start_time = list(map(int, query_params.get("start_time").split('-')))
            start = date(start_time[0], start_time[1], start_time[2])
            end_time = list(map(int, query_params.get("end_time").split('-')))
            end = date(end_time[0], end_time[1], end_time[2])
            print(start, end)
            print(start < date.today() < end)
            query = db.session.query(Event.id, Event.event, Event.date)
            start_limit = Event.date > start
            end_limit = Event.date < end
            events_ = query.filter(start_limit, end_limit).all()
        for entry in events_:
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


class EventByID(Resource):

    @marshal_with(resource_fields)
    def get(self, event_id):
        """return the event with the ID in JSON format. If an event doesn't exist,
        return 404 with the message"""
        event_ = db.session.execute(
            db.select(Event.id, Event.event, Event.date).filter_by(id=event_id)).first()
        if event_ is None:
            abort(404, "The event doesn't exist!")
        return event_

    def delete(self, event_id):
        """delete the event with the given ID """
        event_ = Event.query.filter_by(id=event_id).first()
        print(event_)
        if event_ is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(event_)
        db.session.commit()
        response = jsonify({'message': 'The event has been deleted!'})

        return response


api.add_resource(EventByID, '/event/<int:event_id>')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
