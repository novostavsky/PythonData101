import requests
import json
import os
import argparse

#Note that it uses no authorization, so it can be blocked by github!
#Please consider OAuth if you want to run this reqularly from one IP

#constants and default params
BASE_URL = 'https://api.github.com/repos/{}/{}/contributors'
DEFAULT_CHUNK_SIZE = 128

#get a dictionary contributor:avatar_url for a github project
def get_user_avatar_dict(user_login, project_name):
    user_avatar_dict = {}
    response = requests.get(BASE_URL.format(user_login, project_name))
    json_data = json.loads(response.text)

    for record in json_data:
        user_avatar_dict[record['login']] = record['avatar_url']

    return user_avatar_dict

#save avatar profiles from a project (project owner and project name)
#saving by chunks of DEFAULT_CHUNK_SIZE
def save_avatar_into_folder(owner_name, user_name, project_name, avatar_url):
    folder_name = "{}/{}".format(owner_name, project_name)
    os.makedirs(folder_name, exist_ok=True)

    response = requests.get(avatar_url, stream=True)
    file_type = response.headers['Content-Type'].split('/')[1]
    file_name = '{}/{}.{}'.format(folder_name,user_name,file_type)

    with open(file_name, 'wb') as file_im:
        for chunk in response.iter_content(chunk_size = DEFAULT_CHUNK_SIZE):
            file_im.write(chunk)

#get token from a file if you want to use authentification
def get_github_token(file_name):
    with open(file_name, 'r') as token_file:
        token = token_file.read()
    return token

####################################################################
#################### let's roll#####################################
####################################################################
parser = argparse.ArgumentParser(
    description='This is program that downloads avatars of contributors'
                'for a github project.'
)

parser.add_argument('-u', "--user", action='store')
parser.add_argument('-p', "--project", action='store')
args = parser.parse_args()

user_avatar_dict = get_user_avatar_dict(args.user, args.project)

for contributor in user_avatar_dict:
    save_avatar_into_folder(args.user, contributor, args.project, user_avatar_dict[contributor])