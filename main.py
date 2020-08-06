#Setup Script inital and support config changes
#Open to discussion and renewal
import json
import sys
import time
import requests


def readConfig(self):
    return None


def getTokenOfAdmin():
    docdict = {
        'grant_type': "password",
        'username': "admin",
        'password': "admin",
        'client_id': "admin-cli"
    }
    getTokenOfAdminQuery = requests.post('http://localhost:8080/auth/realms/master/protocol/openid-connect/token', data=docdict)
    token = getTokenOfAdminQuery.json()['access_token']
    return token

def createClients():
    payload = {
        'serviceAccountsEnabled': 'true'
    }
    req = requests.post("http://localhost:8080/auth/admin/realms/master/clients", data=json.dumps(payload), headers={"content-type": 'application/json', "Authorization": "Bearer " + getTokenOfAdmin()})
    print('Response: ' + str(req.status_code))


def getTokenOfRealmCreator():
    docdict = {
        'grant_type': "password",
        'username': "admin",
        'password': "admin",
        'client_id': "create-realm"
    }
    getTokenOfRealmCreatorQuery = requests.post(
        'http://localhost:8080/auth/realms/master/protocol/openid-connect/token', data=docdict)
    print(getTokenOfRealmCreatorQuery.text)

#Create opencontactdev realm RS512 email-verify false reg-allow false
def createRealm():
    payload = {
        'realm': 'realm3',
        'displayName': 'realm3'
    }
    req = requests.post("http://localhost:8080/", data=json.dumps(
        payload), headers={"content-type": 'application/json', "Authorization": "Bearer " + getTokenOfRealmCreator()})
    print('\nResponse CreateRealm: ' + str(req.status_code))
    return(req.status_code)


#testagent
#testmanager
#testadmin
def createUsers():
    #payloads
    adminPayload = {
        "email": "",
        "username": "admin",
        "enabled": True,
        "firstName": "",
        "lastName": "",
        "credentials": [{"value": "admin", "type": "password", }],
    }

    managerPayload = {
        "email": "",
        "username": "manger",
        "enabled": True,
        "firstName": "",
        "lastName": "",
        "credentials": [{"value": "manager", "type": "password", }],
    }

    agentPayload = {
        "email": "",
        "username": "agent",
        "enabled": True,
        "firstName": "",
        "lastName": "",
        "credentials": [{"value": "agent", "type": "password", }],
    }

        #make new user request
    req = requests.post("http://localhost:8080/auth/admin/realms/opencontactdev/users", data=json.dumps(adminPayload), headers=    {"content-type": 'application/json', "Authorization": "Bearer " + getTokenOfAdmin()})

    req2 = requests.post("http://localhost:8080/auth/admin/realms/opencontactdev/users", data=json.dumps(managerPayload), headers={"content-type": 'application/json', "Authorization": "Bearer " + getTokenOfAdmin()})

    req3 = requests.post("http://localhost:8080/auth/admin/realms/opencontactdev/users", data=json.dumps(
        agentPayload), headers={"content-type": 'application/json', "Authorization": "Bearer " + getTokenOfAdmin()})
    print('Response UserCreation:  ' + str(req.status_code) + ':' + str(req2.status_code) + ':' + str(req3.status_code))
    return(req.status_code, req2.status_code, req3.status_code)


def getUsername(): 
    payload = {
        'search': {
            'admin',
            'manager',
            'agent'
        }
    }
    req = requests.get("http://localhost:8080/auth/admin/realms/opencontactdev/users",
                       data=payload, headers={"Authorization": "Bearer " + getTokenOfAdmin()})
    load = json.loads(req.text)
    for i in load:
        print(i['id'])


#agents - roles
#managers
#admins
def createGroups():
    adminPayload = {
        'name': 'admin'
    }
    managerPayload = {
        'name': 'manager'
    }
    agentPayload = {
        'name': 'agent'
    }
   
    req = requests.post("http://localhost:8080/auth/admin/realms/opencontactdev/groups", data=json.dumps(adminPayload), headers={"content-type": 'application/json',"Authorization": "Bearer " + getTokenOfAdmin()})
    
    req2 = requests.post("http://localhost:8080/auth/admin/realms/opencontactdev/groups", data=json.dumps(managerPayload), headers={"content-type": 'application/json', "Authorization": "Bearer " + getTokenOfAdmin()})
    
    req3 = requests.post("http://localhost:8080/auth/admin/realms/opencontactdev/groups", data=json.dumps(agentPayload), headers={"content-type": 'application/json', "Authorization": "Bearer " + getTokenOfAdmin()})
    
    print('Response GroupCreation: ' + str(req.status_code) + ':' +
          str(req2.status_code) + ':' + str(req3.status_code))
    return(req.status_code, req2.status_code, req3.status_code)

    
#agent
#manager
#admin
def createRoles():
    payload = {}
    req = requests.post("http://localhost:8080/auth/admin/realms/master/", data=json.dumps(
        payload), headers={"content-type": 'application/json', "Authorization": "Bearer " + getTokenOfAdmin()})
    print('Response: ' + str(req.status_code))


#Agents agent
#Agents manager
#Agents admin
def addRoles():
    payload = {}
    req = requests.post("http://localhost:8080/auth/admin/realms/master/", data=json.dumps(
        payload), headers={"content-type": 'application/json', "Authorization": "Bearer " + getTokenOfAdmin()})
    print('Response: ' + str(req.status_code))


#run the functions and return whether they were success for not. 
def loadinIf():
    # if createRealm() == 201:
    #     print('\nSuccess \n')
    # else:
    #     print('Failed: 500\n')
    if createUsers() == 201:
        print('Success \n')
    else:
        print('Failed: 500\n')
    # if createGroups() == 201:
    #     print('Success \n')
    # else:
    #     print('Failed: 500\n')
    # if createRoles() == 201:
    #     print('Success \n')
    # else:
    #     print('Failed: 500')
    time.sleep(1)
    print(
r"""
                                              __             __     
  ____  ____  ___  ____     _________  ____  / /_____ ______/ /_    
 / __ \/ __ \/ _ \/ __ \   / ___/ __ \/ __ \/ __/ __ `/ ___/ __/    
/ /_/ / /_/ /  __/ / / /  / /__/ /_/ / / / / /_/ /_/ / /__/ /_      
\____/ .___/\___/_/ /_/   \___/\____/_/ /_/\__/\__,_/\___/\__/      
    /_/                                                                 
"""
    )

#working components


if __name__ == "__main__":
    getTokenOfRealmCreator()
    createUsers()
    time.sleep(.5)
    createGroups()
    getUsername()
else:
    raise ValueError('you broke it you fool')
