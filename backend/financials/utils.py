import secrets

import bcrypt


def generate_api_secret():

    return secrets.token_hex(32)


def hash_api_secret(secret):

    return bcrypt.hashpw(

        secret.encode(),

        bcrypt.gensalt()

    ).decode()


def verify_api_secret(

    plain_secret,

    hashed_secret

):

    return bcrypt.checkpw(

        plain_secret.encode(),

        hashed_secret.encode()

    )