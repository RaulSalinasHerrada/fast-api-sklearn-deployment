import secrets
import os
n= 16
apikey = secrets.token_urlsafe(n)
phrase = "API_KEY={}\n".format(apikey)

env_path = '.env'
nl = list()
if os.path.exists(env_path):

    with open(env_path,'r') as file:
        lines = file.readlines()
        
        for line in lines:
            if line.startswith("API_KEY="):
                nl.append(phrase)
                print("NEW API KEY: ", apikey)
            else:
                nl.append(line)
    
    os.remove(env_path)

if len(nl) == 0:
    nl.append(phrase)

print(nl)

with open(env_path,"a") as file_read:
    file_read.writelines(nl)