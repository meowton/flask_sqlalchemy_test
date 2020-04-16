from flask import Flask, request
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

from models import People, Assignments, Users

auth = HTTPBasicAuth()
app = Flask(__name__)
api = Api(app)


@auth.verify_password
def verification(login, password):
    if not (login, password):
        return False
    return Users.query.filter_by(login=login, password=password).first()


class PeopleList(Resource):
    @auth.login_required
    def get(self):
        people = People.query.all()
        response = [{
            'id': i.id,
            'name': i.name,
            'age': i.age
        } for i in people]
        return response

    def post(self):
        body_data = request.json
        person = People(name=body_data['name'], age=body_data['age'])
        person.save()
        response = {
            'id': person.id,
            'name': person.name,
            'age': person.age
        }
        return response


class PeopleApi(Resource):
    @auth.login_required
    def get(self, person_name):
        try:
            person = People.query.filter_by(name=person_name).first()
            response = {
                'id': person.id,
                'name': person.name,
                'age': person.age
            }

        except AttributeError:
            response = {
                'status': 'Error',
                'message': 'Person not found!'
            }
        return response

    def put(self, person_name):
        person = People.query.filter_by(name=person_name).first()
        body_data = request.json
        if 'name' in body_data:
            person.name = body_data['name']
        if 'age' in body_data:
            person.age = body_data['age']
        person.save()
        response = {
            'id': person.id,
            'name': person.name,
            'age': person.age
        }
        return response

    def delete(self, person_name):
        person = People.query.filter_by(name=person_name).first()
        person.delete()
        return {
            'status': 'Success!',
            'message': f'Person {person.name} successfully deleted!'
        }


class AssignmentList(Resource):
    def get(self):
        assignment = Assignments.query.all()
        response = [{
            'id': i.id,
            'name': i.name,
            'person': i.people.name
        } for i in assignment]
        return response

    def post(self):
        body_data = request.json
        person = People.query.filter_by(name=body_data['person']).first()
        assignment = Assignments(name=body_data['name'],
                                 status=body_data['status'],
                                 people=person)
        assignment.save()
        response = {
            'id': assignment.id,
            'person': assignment.people.name,
            'name': assignment.name,
            'status': assignment.status
        }
        return response


class UserAssignment(Resource):
    def get(self, person_name):
        person = People.query.filter_by(name=person_name).first()
        assignment = Assignments.query.filter_by(people=person)
        response = [{
            'id': i.id,
            'person': i.people.name,
            'name': i.name,
            'status': i.status
        } for i in assignment]
        return response


api.add_resource(PeopleList, '/people/')
api.add_resource(PeopleApi, '/person/<string:person_name>/')
api.add_resource(AssignmentList, '/assignments/')
api.add_resource(UserAssignment, '/assigned/<string:person_name>/')

if __name__ == '__main__':
    app.run(debug=True)
