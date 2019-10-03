import requests 
import json

base_url = 'http://127.0.0.1:8000' 

def get_auth_token(user_name,pass_word):
    print(user_name,pass_word)
    url=base_url+'/get_token/'
    # headers = {'Authorization': 'Token '+token}
    # params = {'username': user.username, 'password': user.password}
    data = {'username': user_name, 'password': pass_word}
    # data =dict (username=user_name,password=pass_word)
    # params = {'username': 'suba'}
    # r = requests.post(url, params=params)
    # r = requests.get(url, headers=headers)
    r = requests.post(url,data=data)
    print(r.text,'token1')
    reg=json.loads(r.text) 
    print(reg['token'],'token2')
    return reg['token']


def get_all_registration(req):
    # print('tokennew',request.session['authtoken'])
    token=req.session['authtoken']
    url=base_url+'/registration/'
    headers = {'Authorization': 'Token '+token}
    r = requests.get(url, headers=headers)
    reg = r.json()
    return reg

def get_auth_app(id,req):
     # print('tokennew',request.session['authtoken'])
    token=req.session['authtoken']
    url=base_url+'/app_filter?role_id='+str(id)
    headers = {'Authorization': 'Token '+token}
    r = requests.get(url, headers=headers)
    reg = json.loads(r.text)
    print(reg,'applist')
    return reg