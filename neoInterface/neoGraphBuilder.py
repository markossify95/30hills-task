from neoInterface.interface import graph, insert_person, build_relationship
import json


def build_graph():
    with open('../data/data.json', 'r') as data:
        j_data = data.read()
        network = json.loads(j_data)

        try:
            for person in network:
                insert_person(person['id'], person['firstName'], person['surname'], person['age'], person['gender'])

            for person in network:
                for friend_id in person['friends']:
                    build_relationship(person['id'], friend_id)
        except Exception as e:
            print(e)


build_graph()
# print(graph.run("MATCH (a:Person) RETURN a.id, a.firstName, a.surname LIMIT 10").data())
