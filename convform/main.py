import json

from .list_items import list_items
from .edit_item import edit_item
from .remove_item import remove_item
from .copy_item import copy_item
from .rename_item import rename_item

ops = {
    "list": lambda args: list_items(args),
    "remove": lambda args: remove_item(args),
    "edit": lambda args: edit_item(args),
    "copy": lambda args: copy_item(args),
    "rename": lambda args: rename_item(args),
}

def convform(instruction):

    flow = instruction.get('flow', "")
    func = instruction.get('func', "")
    item_type = instruction.get('item_type', "")
    name = instruction.get('name', "")
    data = instruction.get('data', "")

    success = ops[func]({"flow": flow, "item_type": item_type, "name": name, "data": data})
    return success
