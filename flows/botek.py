def reply(user_reply, cs):
    cs.setdefault("r", 0)

    cs["r"] += 1

    if cs["r"] == 4:
        return None

    return cs
