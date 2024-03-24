from .cstatus import ConversationStatus

def reply(userSpeech, flow, c_status_in):
    c_status_out = ConversationStatus(userSpeech, flow, c_status_in)
    return c_status_out
