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


def get_suggested_by_id(my_id, friends_of_friend):
    suggested_ids = []
    for i, i_friends in enumerate(friends_of_friend):
        for j, j_friends in enumerate(friends_of_friend):
            if i is not j:
                mutual_friends = [val for val in i_friends if val in j_friends and val is not my_id]
                suggested_ids += mutual_friends

    final_ids = []
    for fid in suggested_ids:
        if fid not in final_ids and suggested_ids.count(fid) >= 2:
            final_ids.append(fid)

    return final_ids


def get_profile_only(id):  # correct to get profiles for all suggested friends!!!
    get_me_query = "SELECT * FROM `person` WHERE `id` = %s"
    with connection.cursor() as cursor:
        try:
            cursor.execute(get_me_query, id)
            me = cursor.fetchone()
        finally:
            connection.commit()
    profile = {
        'id': me[0],
        'firstName': me[1],
        'surname': me[2],
        'age': me[3],
        'gender': me[4],
    }
    return profile


def suggested_friends(id):
    me, friends_detailed = friends_of_friends(id)
    friend_dict = {}
    for friend in friends_detailed.values():
        fof_list = []
        for fof in friend['friendsOfFriend'].values():
            fof_list.append(fof['id'])
        friend_dict[friend['friend']['id']] = fof_list

    suggested_ids = get_suggested_by_id(me['id'], friend_dict.values())
    final_suggestions = {}
    i = 0
    for sug_id in suggested_ids:
        final_suggestions[i] = get_profile_only(sug_id)
        i += 1

    return me, final_suggestions
