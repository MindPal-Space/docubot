import uuid
import datetime

def generate_uuid():
    # create a datetime object
    now = datetime.datetime.now()

    # generate a UUID based on the datetime object
    unique_id = uuid.uuid5(uuid.NAMESPACE_DNS, str(now))
    return str(unique_id)
