from neoInterface.interface import graph
import json
from falcon import HTTP_200


class FriendsView:
    def on_get(self, req, resp, pid):
        data = graph.run("MATCH (:Person { pid:{x} })-->(person:Person) RETURN person", x=int(pid)).data()
        me = graph.run("MATCH (me:Person { pid:{x} }) RETURN me", x=int(pid)).data()
        resp.status = HTTP_200
        final = {}
        for i, friend in enumerate(data):
            final[i] = friend['person']
        friends = {
            'profile': me[0]['me'],
            'friends': final
        }
        resp.body = json.dumps(friends)


class FriendsOfFriendsView:
    def on_get(self, req, resp, pid):
        data = graph.run("MATCH (:Person { pid:{x} })-[*2]->(person:Person) RETURN person", x=int(pid)).data()
        resp.status = HTTP_200
        resp.body = json.dumps(data)
