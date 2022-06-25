import sqlite3
import os
from datetime import datetime

import requests
import json
import uuid

# create table competitions (
#   ...> id INT PRIMARY KEY,
#   ...> thing TEXT,
#   ...> start INT,
#   ...> end INT);

# create table data (
#   ...> date INT,
#   ...> id INT PRIMARY KEY,
#   ...> xp INT,
#   ...> comp INT,
#   ...> uuid TEXT,
#   ...> CONSTRAINT uuid FOREIGN KEY (uuid) REFERENCES users(uuid),
#   ...> CONSTRAINT comp FOREIGN KEY (comp) REFERENCES competitions(id));


def getUUIDlist(key):
    uuids = []

    # open the file that lists all the groups to get igns from
    with open('..\\people.json', 'r') as f:
        groups = json.load(f)

    # for each group
    for i in groups:
        # if group type is a guild
        if i['type'] == 'guild':
            for person in requests.get("https://api.hypixel.net/guild?key=" + key +
                                       "&name=" + str(i['id'])).json()['guild']['members']:
                uuids.append(person['uuid'])

        elif i['type'] == 'ign':
            uuids.append(requests.get("https://api.mojang.com/users/profiles/minecraft/" + i['id']).json()['id'])

        # if group type is uuid
        elif i['type'] == 'uuid':
            uuids.append(i['id'])

    # Return all the uuids
    return uuids


def setupComp(cur, type, length):
    # Checks for comps still on going
    for i in cur.execute('SELECT * FROM competitions WHERE end > ' + str(int(datetime.now().timestamp()))):
        raise Exception("Can not have more than one active competition")

    # Gets api key
    with open('..\\key.txt', 'r') as f:
        key = f.read()


    # Makes competition
    compid = uuid.uuid1()
    cur.execute('INSERT INTO competitions (id, thing , start, end) VALUES ("{0}", "{1}", {2}, {3});'.format(compid.int, type, int(datetime.now().timestamp()), int(datetime.now().timestamp() + length)))

    data = []
    for num, puuid in enumerate(getUUIDlist(key)):
        print(num)
        # grabs all information for each player
        data = requests.get('https://hypixel-api.senither.com/v1/profiles/' + puuid +
                             '/save', params={'key': key}).json()

        # Add player data to data table
        cur.execute('INSERT INTO data (id, date, xp, comp, uuid) VALUES ({0}, "{1}", {2}, "{3}","{4}");'
                    .format(uuid.uuid1().int,
                            int(datetime.now().timestamp()),
                            eval("data['data']"+type),
                            compid.int,
                            puuid
                            )
                    )
    cur.commit()
    print("Made and commited competition")
    print("Type: ", type)
    print("Length: ", length)


def addCompData(cur):
    # Checks for comps still on going
    for i in cur.execute('SELECT id, thing, end FROM competitions WHERE end > ' + str(int(datetime.now().timestamp()))):
        # Gets api key
        with open('..\\key.txt', 'r') as f:
            key = f.read()

        data = []
        for num, puuid in enumerate(getUUIDlist(key)):
            print(num)
            # grabs all information for each player
            data = requests.get('https://hypixel-api.senither.com/v1/profiles/' + puuid +
                                '/save', params={'key': key}).json()

            # Add player data to data table
            cur.execute('INSERT INTO data (id, date, xp, comp, uuid) VALUES ({0}, "{1}", {2}, "{3}","{4}");'
                        .format(uuid.uuid1().int,
                                int(datetime.now().timestamp()),
                                eval("data['data']" + i[1]),
                                i[0],
                                puuid
                                )
                        )
        cur.commit()
        print("Commmited new data to competition")
        print("Type: ", i[1])
        return
    raise Exception("No Active Competition")


if __name__ == '__main__':
    try:
        cur = sqlite3.connect(os.path.realpath(os.path.join(os.path.dirname(__file__), "", "data.sqlite")))
        setupComp(cur, "['skills']['foraging']['experience']", 600)
    except Exception as e:
        addCompData(cur)