import sqlite3
import os
import requests
import json


def getUUIDlist(key):
    uuids = []

    # open the file that lists all the groups to get igns from
    with open('people.json', 'r') as f:
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


def setupComp(cur):
    for i in cur.execute('SELECT * FROM data'):
        print(i)

    with open('key.txt', 'r') as f:
        key = f.read()

    for uuid in getUUIDlist(key):
        # grabs all information for each player
        data = requests.get('https://hypixel-api.senither.com/v1/profiles/' + uuid +
                            '/save', params={'key': key}).json()


if __name__ == '__main__':
    setupComp(sqlite3.connect(os.path.realpath(os.path.join(os.path.dirname(__file__), "", "data.sqlite"))))