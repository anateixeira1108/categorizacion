import hashlib
import random


def generate_sha1():
    hash_string = hashlib.sha1(str(random.random())).hexdigest()
    return hash_string