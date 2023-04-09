def reply(user_reply, cs):
    cs.setdefault("r", 0)
    cs["r"] += 1
    return cs["r"]


