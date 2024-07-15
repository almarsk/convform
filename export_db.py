from app import Conversation, Flow, Project, Reply, app
from database import db
import pprint

def export():
    with app.app_context():

        all_convos = Conversation.query.all()
        all_convo_data = dict()

        for convo in all_convos:
            flow = Flow.query.filter_by(flow_name=convo.flow).first()
            if convo.flow and flow:
                if convo.flow and flow.project_id == 18:

                    if flow.flow_name not in all_convo_data:
                        flow_type = determine_type(flow.flow_name)
                        all_convo_data[flow.flow_name] = {"type": flow_type, "data": dict()}

                    all_replies = Reply.query.filter_by(user_id=convo.id).all()

                    if all_replies:

                        replies = []
                        replies_meta = []

                        for reply in all_replies:
                            if reply.reply:

                                reply_data = {
                                    "reaction_time": reply.reaction_ms,
                                    "stimuli": determine_stimuli(reply.cstatus),
                                }

                                if reply_data['stimuli'] and reply.who == 'bot':
                                    reply_data["entities"] = prompt_log = reply.cstatus["entities"]
                                if reply.who == 'bot':
                                    reply_data["prompting"] = get_prompt_logs(reply.cstatus["prompt_log"])


                                replies_meta.append(reply_data)
                                replies.append(f"{'!!!' if reply_data['stimuli'] and reply.who == 'bot' else ''} {reply.who}: {reply.reply}")

                        convo_data = {
                            "id": convo.id,
                            "nick": convo.nick,
                            "flow": flow.flow_name,
                            "abort": convo.abort,
                            "rating": convo.rating,
                            "comment": convo.comment,
                            "conversation": replies,
                            "conversation_meta": replies_meta
                        }

                        all_convo_data[flow.flow_name]["data"][convo_data["id"]] = convo_data

        # print(sum([len(all_convo_data[key]["data"]) for key in all_convo_data.keys()]))

        pprint.pp(all_convo_data, width=200)

    #with open("chatbot1.json", "w") as c:
    #    c.write(str(all_convo_data))


def determine_type(flow):
    types = {
        "AutoMarta": "relaxed shallow ",
        "Vladimatik": "inquisitive unasignable",
        "Ondroid": "inquisitive unassignable",
        "Zdendotron": "inquistive deep",
        "Robomila": "relaxed deep",
        "Elizabota": "inquisitive shallow"
    }

    if flow in types:
        return types[flow]
    else:
        return ""

def determine_stimuli(cstatus):
    state_name = "dotaz"
    return bool([state for state in cstatus["last_states"] if state == state_name])

def get_prompt_logs(prompt_log):
    prompt_log_filtered = list()
    basic_countdown = 0
    for i, log in enumerate(prompt_log):
        if log == "todo changes basic to about what call":
            continue
        if log == "an2fora" or log == "b-dynamic succesful - going back":
             basic_countdown = 4
        if log == "basic":
            basic_countdown = 3
        if log == "entity" or log == "bd2":
            basic_countdown = 2
        if basic_countdown > 0:
            basic_countdown -= 1
        else:
            prompt_log_filtered += [str(log)
                .replace("""\\\\n""", "")
                .replace("""\n""", "")
                .replace("'''", "")]

    return prompt_log_filtered

export()
