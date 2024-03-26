import os
import json

from .proof_empty import proof_empty
from .proof_exception import ProofException
from .proof_references import proof_references

def validate_flow(flow, return_flow=False):
    issues = list()
    bot = dict()
    schema = dict()
    result = dict()

    from app import db, Flow
    flow_data = Flow.query.filter_by(flow_name=flow).first()

    # check valid data
    if flow_data is None:
        issues.append("no such bot")
        result =  {
            "success": False,
            "message": ProofException(issues).message
        }
    elif flow_data.is_archived:
        result =  {
            "success": False,
            "message": "flow archived"
        }
    else:
        bot = flow_data.flow

        proof_empty(bot, issues)
        proof_references(bot, issues)

        result = dict()

        if return_flow and not issues:
            return bot
        elif return_flow and issues:
            raise ProofException(issues)
        elif issues:
            result =  {
                "success": False,
                "message": ProofException(issues).message
            }
        else:
            result =  {
                "success": True,
                "message": f"Flow {flow} is valid."
            }


    return result
