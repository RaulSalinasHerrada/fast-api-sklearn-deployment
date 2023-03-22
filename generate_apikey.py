import secrets
apikey = secrets.token_urlsafe(64)
phrase = "API_KEY = '{}'".format(apikey)

with open('.env','w') as file:
    file.write(phrase)