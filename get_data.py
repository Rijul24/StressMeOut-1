import json
import datetime


def import_list(guild_id):
    with open("_data.json", "r") as f:
        data = json.load(f)
    _guild = data.get(str(guild_id))
    res = []
    for i in _guild:
        res.append([i[0], i[1]])
    return res


def conv_list(guild_id):
    res = import_list(guild_id)
    current = datetime.datetime.now() + datetime.timedelta(hours=5, minutes=30)
    for i in range(len(res)):
        due = datetime.datetime.strptime(res[i][1], '%Y %m %d %H %M')
        left = due - current
        left = str(left)
        if left[0] == "-":
            res[i][1] = "over"
        else:
            res[i][1] = str(left)[0:len(left) - 10] + " Hours left"
    return res
