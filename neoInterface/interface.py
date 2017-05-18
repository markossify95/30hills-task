from py2neo import Graph, Node, Relationship, NodeSelector

# from Model.person import Person

graph = Graph(password='neo4j')


def insert_person(pid, firstName, surname, age, gender):
    tx = graph.begin()
    a = Node("Person", pid=pid, firstName=firstName, surname=surname, age=age, gender=gender)
    tx.create(a)
    tx.commit()

    # OGM, missing dependency injection, but good for now
    # p = Person(pid, firstName, surname, age, gender)
    # graph.create(p)
    # maybe their OGM is not good enough...or I'm not :D


def build_relationship(id1, id2):
    selector = NodeSelector(graph)
    friend1 = selector.select("Person", pid=id1).first()
    friend2 = selector.select("Person", pid=id2).first()
    tx = graph.begin()
    f12 = Relationship(friend1, "FRIENDS_WITH", friend2)
    tx.create(f12)
    tx.commit()
