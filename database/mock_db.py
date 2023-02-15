
import json

filename = 'mock_stacks.json'


def create_new_stack(new_data):

    try:
        with open(filename, 'r') as f:
            loaded = json.load(f)
            loaded.append(new_data)

        with open(filename, 'w') as f:
            f.write(json.dumps(loaded, indent=4))

    except Exception:
        with open(filename, 'w') as f:
            f.write(json.dumps([new_data], indent=4))


def get_all_stacks():

    try:
        with open(filename, 'r') as f:
            loaded = json.load(f)
            return loaded

    except Exception:
        return []


def update_all_stacks(data):
    with open(filename, 'w') as f:
        f.write(json.dumps(data, indent=4))
