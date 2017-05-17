from Model.dbconn import connection


def get_profile_data(id):
    friend_test_query = "SELECT * FROM `person` WHERE `id` in " \
                        "(SELECT `friend1` FROM `friends` WHERE `friend2`=%s)"
    friend_test_query2 = "SELECT * FROM `person` WHERE `id` in " \
                         "(SELECT `friend2` FROM `friends` WHERE `friend1`=%s)"

    get_me_query = "SELECT * FROM `person` WHERE `id` = %s"
    friends = []
    me = []
    with connection.cursor() as cursor:
        try:
            cursor.execute(friend_test_query, id)
            friends = cursor.fetchall()
            cursor.execute(friend_test_query2, id)
            friends += cursor.fetchall()
            cursor.execute(get_me_query, id)
            me = cursor.fetchone()
        finally:
            connection.commit()
    rs_friends = {}
    i = 0
    profile = {
        'id': me[0],
        'firstName': me[1],
        'surname': me[2],
        'age': me[3],
        'gender': me[4],
    }
    for f in friends:
        rs_friends[i] = {
            'id': f[0],
            'firstName': f[1],
            'surname': f[2],
            'age': f[3],
            'gender': f[4]
        }
        i += 1
    return profile, rs_friends


def friends_of_friends(id):
    me, friends = get_profile_data(id)
    fof = {}
    i = 0
    for f in friends.values():
        friend, his_friends = get_profile_data(f['id'])
        fof[i] = {
            'friend': friend,
            'friendsOfFriend': his_friends
        }
        i += 1
    return me, fof


def suggested_friends(id):
    me, friends_detailed = friends_of_friends(id)
    friend_dict = {}
    for friend in friends_detailed.values():
        fof_list = []
        for fof in friend['friendsOfFriend'].values():
            fof_list.append(fof['id'])
        friend_dict[friend['friend']['id']] = fof_list

    return me, friend_dict
