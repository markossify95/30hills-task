from py2neo.ogm import GraphObject, Property, Related


class Person(GraphObject):
    """
    neo4j model class, but not being used in current version because of OGM bugs.
    """
    __primarykey__ = "pid"

    def __init__(self, pid, firstName, surname, age, gender):
        self.pid = pid
        self.firstName = firstName
        self.surname = surname
        self.age = age
        self.gender = gender

    pid = Property()
    firstName = Property()
    surname = Property()
    age = Property()
    gender = Property()

    friends_with = Related("Person")
