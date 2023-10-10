import uuid

def get_random_code():
    namespace = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')
    name = 'example_name'

    code = str(uuid.uuid5(namespace, name))[:8].replace("-", "").lower()
    return code