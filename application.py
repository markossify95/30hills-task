import falcon
from View.profile import FriendsView, FriendsOfFriendsView, SuggestedFriendsView
from wsgiref import simple_server

app = falcon.API()

app.add_route('/api/profile/{pid}/friends', FriendsView())
app.add_route('/api/profile/{pid}/friends-of-friends', FriendsOfFriendsView())
app.add_route('/api/profile/{pid}/suggested', SuggestedFriendsView())

if __name__ == '__main__':
    srv = simple_server.make_server('localhost', 8080, app)
    srv.serve_forever()
