import json
import pymysql

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='social_network')


def init_db():
    with open('../data/data.json', 'r') as data:
        j_data = data.read()
        network = json.loads(j_data)

        try:
            with connection.cursor() as cursor:
                # Create a new record
                query = "INSERT INTO `person` (`id`, `firstName`, `surname`, `age`, `gender`) " \
                        "VALUES (%s, %s, %s, %s, %s)"

                friendship_update_query = "INSERT INTO `friends` (`friend1`, `friend2`)" \
                                          "VALUES (%s, %s)"

                friend_test_query = "SELECT * FROM `friends` WHERE `friend1`=%s AND `friend2`=%s"

                for person in network:
                    cursor.execute(query,
                                   (person['id'], person['firstName'],
                                    person['surname'], person['age'], person['gender']))

                for person in network:
                    for friend_id in person['friends']:
                        cursor.execute(friend_test_query, (friend_id, person['id']))
                        result = cursor.fetchone()
                        if result is None:
                            cursor.execute(friendship_update_query, (person['id'], friend_id))
                            connection.commit()
        finally:
            connection.close()
