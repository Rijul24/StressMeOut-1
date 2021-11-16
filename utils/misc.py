import datetime


def change_timeformat(inp: str):
    try:
        due = datetime.datetime.strptime(inp, '%d.%m.%Y %H:%M')
    except ValueError:
        return False
    return due


def is_user_authorized(unique_id: int) -> bool:
    # TODO: work on it lol
    return unique_id in {428956244238270475, 556140685858963458, 786851962833862676, 782940990801051715}


def ordinal(n: int) -> str:
    return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])
    # https://codegolf.stackexchange.com/a/4712
