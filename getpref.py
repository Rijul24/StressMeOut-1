import json

_bot_mention = "<@!798262042669613083> "


def get_pref(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    res = prefixes.get(str(message.guild.id))
    return res, _bot_mention, "#$"
# ~universal perfix~ = #$
