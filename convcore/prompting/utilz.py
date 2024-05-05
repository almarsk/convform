import json
import os
import importlib
from registered_chains import registered_chains


def api_key():
    json_file_path = "config.json"
    field_name = "OPENAI_API_KEY"

    if not field_name in os.environ:
        try:
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)

            if field_name in json_data:
                os.environ[field_name] = json_data[field_name]
            else:
                print(f"Field '{field_name}' not found in the JSON data.")

        except FileNotFoundError:
            print(f"JSON file not found at '{json_file_path}'")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


def import_chains(registered_chains, element):
    functions = {}

    for chain_name in registered_chains[element]:
        try:
            module = importlib.import_module(f"convcore.prompting.chains.{element}.{chain_name}")
            functions[chain_name] = getattr(module, chain_name, None)
        except ImportError as e:
            print(f"Failed to import chain '{chain_name}': {e}")
    return functions


def resolve_prompt(args: dict):
    api_key()
    args["log"]([args["chain"]])
    return import_chains(registered_chains, "state")[args["chain"]](args)


# prompts, history, log
def match_prompt_intents(args: dict):
    api_key()
    matches = {}

    for intent, prompt_info in args["prompts"].items():
        print("\n\nargs", args)
        chain = prompt_info["chain"]
        args["log"](chain)

        prompts = [{
             "prompt": prompt["text"],
             "context": context if not say["emphasis"] else [],
             "log": self.add_to_prompt_log,
             "chain": say["prompt"],
         } for prompt in self.raw_say if say["prompt"]]


        result = import_chains(registered_chains, "state")[chain]({

        })
        print("matches", matches[result])

    return import_chains(registered_chains, "state")[chain](args)
