import json
from Model.dbconn import connection
from Model.utils import get_profile_data, friends_of_friends, suggested_friends
from falcon import HTTP_200


class FriendsView:
    def on_get(self, req, resp, pid):
        user, friends = get_profile_data(pid)
        data = {
            'profile': user,
            'friends': friends
        }
        resp.body = json.dumps(data)
        resp.status = HTTP_200


class FriendsOfFriendsView:
    def on_get(self, req, resp, pid):
        user, friends = friends_of_friends(pid)
        data = {
            'profile': user,
            'friends': friends
        }
        resp.body = json.dumps(data)
        resp.status = HTTP_200


class SuggestedFriendsView:
    def on_get(self, req, resp, pid):
        user, result_set = suggested_friends(pid)
        data = {
            'profile': user,
            'suggestedFriends': result_set
        }
        resp.body = json.dumps(data)
        resp.status = HTTP_200
