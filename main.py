import json;
import requests;
from config import config;
from flask import Flask, request;
from requests.auth import HTTPBasicAuth;

api = Flask(__name__);

api.config.from_object(config['production'])

def create_jira_issue():
    authentication = HTTPBasicAuth(username=api.config["AUTH_USER"], password=api.config["AUTH_PWD_TOKEN"]);

    bodyPaylaod = {
        "fields": {
            # TODO: dynamic project 
            "project": {
                "id": "11302"
            },
            "issuetype": {
                "id": "10203"
            },
            "reporter": {
                "id": "6350ed6dfc0cc7a600ad3d3d"
            },
            # TODO: dynamic summary 
            "summary": "Test",
            "components": [
                {
                    "id": "10945",
                    "name": "SOC"
                }
            ],
            "description": {
                "version": 1,
                "type": "doc",
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                # TODO: dynamic description 
                                "text": "Test automatizacin tickets"
                            }
                        ]
                    }
                ]
            },
            "priority": {
                "id": "10103",
                "name": "Baja",
                "iconUrl": "https: //fiatc.atlassian.net/images/icons/priorities/lowest.svg"
            },
            "assignee": {
                "id": "6350ed6dfc0cc7a600ad3d3d"
            },
            "customfield_10419": {
                "id": "6243fb89ed4d6b0070129d0e"
            },
            "customfield_10412": [],
            "customfield_10411": [],
            "labels": []
        },
        "update": {}
    };

    requests.post(api.config["ATLASSIAN_API_URL"], auth=authentication, json=bodyPaylaod);


@api.route("/splunk-jira-issue", methods=['POST'])
def handle_post_create_issue():
    body = request.get_json();
    print("debug", request.get_json())
    with open('db.json', 'w') as file:
        json.dump(body, file);
    
    try:
        # create_jira_issue(body)
        print("debug-2")
    except:
        return 500;

    return json.dumps({ "status": "Issue creada.", "request_body": body }), 201;

@api.route("/get-report", methods=['GET'])
def welcome_message():
    with open('db.json') as file:
        data = json.load(file);
        return json.dumps({ "info": data }), 200;

@api.route("/", methods=['GET'])
def welcome_message():
    return json.dumps({ "status": "Service running." }), 200;


if __name__ == "__main__":

    if api.config == None:
        print("Missing .env file.");
        exit(1);

    if api.config.get("ATLASSIAN_API_URL") == None or api.config.get("ATLASSIAN_API_URL") == "":
        print("Falta el campo ATLASSIAN_API_URL, en el fichero .env indicando la url de la api de Atlassian");
        exit(1);

    if api.config.get("AUTH_USER") == None or api.config.get("AUTH_PWD_TOKEN") == None:
        print("Falta alguno de los campos AUTH_PWD_TOKEN / AUTH_USER, en el fichero .env.");
        exit(1);

    api.run(debug=True);