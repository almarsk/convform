from terbox.exp import look_in_database
import fire

def main(query='', states=False, debug=False, which=-1):
    look_in_database(query=query, states=states, debug=debug, which=which)


if __name__ == '__main__':
    fire.Fire(main)
