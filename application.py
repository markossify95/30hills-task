import falcon
from View.profile import FriendsView, FriendsOfFriendsView, SuggestedFriendsView
from wsgiref import simple_server

app = falcon.API()

# MySQL API

app.add_route('/api/profile/{pid}/friends', FriendsView())
app.add_route('/api/profile/{pid}/friends-of-friends', FriendsOfFriendsView())
app.add_route('/api/profile/{pid}/suggested', SuggestedFriendsView())

# neo4j API
from neoInterface import neoViews

app.add_route('/api/v2/profile/{pid}/friends', neoViews.FriendsView())
app.add_route('/api/v2/profile/{pid}/friends-of-friends', neoViews.FriendsOfFriendsView())

if __name__ == '__main__':
    srv = simple_server.make_server('localhost', 8080, app)
    srv.serve_forever()
