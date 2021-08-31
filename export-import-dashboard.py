#!/usr/bin/env python
import json
import requests
import os

HOST = "***"
API_KEY = "****"
DASH_PATH="./"

# Function to download dashoard json file and clean up id, uid, version to ignore duplication error while importing
def export_dash():
    headers = {'Authorization': 'Bearer %s' %(API_KEY,)}
    response = requests.get('%s/api/search?query=&' % (HOST,), headers=headers)
    dashboards = response.json()
    for dashboard in dashboards:
                dash_res = requests.get('%s/api/dashboards/uid/%s' % (HOST, dashboard["uid"]), headers=headers)
                dash_json = dash_res.json()['dashboard']
                dash_json['id'] = None
                dash_json['uid'] = None
                dash_json['version'] = 0
                print("going to save {}".format(dashboard["title"]))
                with open(DASH_PATH + dashboard["title"] + ".json", 'w', encoding='utf-8') as f:
                    json.dump(dash_json, f, ensure_ascii=False, indent=4)

# Function to import grafana dashboard from given path (DASH_PATH)
def import_dash():
    headers = {'Authorization': 'Bearer %s' %(API_KEY,)}
    for file in os.listdir(DASH_PATH):
        if not file.endswith('.json'):
            continue

        print ("going to import this file {}".format(file))
        f = open(DASH_PATH + file, 'r')
        dash = json.load(f)
        f.close()
        # folderId and folderUid need to be given if you want to import to any specific folder
        #data = {"dashboard": dash, "folderUid": "****","folderId": *** ,"overwrite": True}
        data = {"dashboard": dash ,"overwrite": True}
        r = requests.post('%s/api/dashboards/db' % (HOST,), json=data, headers=headers)
        if r.status_code != 200:
            print (r.status_code, r.content)
            exit(1)


if __name__ == '__main__':
    export_dash()
    #import_dash()
    
