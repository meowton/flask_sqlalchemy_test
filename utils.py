from models import People, Users


def insert_person():
    person = People(name='Nep', age=99)
    person.save()
    print(person)


def query_person():
    people = People.query.all()
    print(people)
    # person = People.query.filter_by(name='Nep').first()
    # print(person.name, person.age)


def update_person():
    person = People.query.filter_by(name='Nep').first()
    person.age = 99
    person.save()


def delete_person():
    person = People.query.filter_by(name='Nep').first()
    person.delete()


def insert_user(login, password):
    user = Users(login=login, password=password)
    user.save()


def query_users():
    users = Users.query.all()
    print(users)


if __name__ == '__main__':
    # insert_person()
    # update_person()
    # delete_person()
    # query_person()
    insert_user('meow', '123')
    insert_user('nep', '321')
    query_users()
