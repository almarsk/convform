#! venv/bin/python3

import terbox.exp as exp
import fire

def main(query='', states=False, debug=False, which=-2):
    exp.main(query=query, states=states, debug=debug, which=which)


if __name__ == '__main__':
    fire.Fire(main)
