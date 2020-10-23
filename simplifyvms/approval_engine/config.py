from approval_engine import approval_rule_set
from django.conf import settings
import json
import requests

logger = settings.LOGGER


def get_auth_token(username, password):
    """
    Function will return the token based on the username and
    password provided.
    """
    payload = {
        "username": username,
        "password": password
    }
    headers = {
        "Content-Type": "application/json"
    }
    auth_token_obj = requests.post(
        settings.AUTH_TOKEN_ENDPOINT,
        data=json.dumps(payload),
        headers=headers
        )
    return auth_token_obj.json()['token']


def get_flag_value(operator, operand1, operand2):
    """
    Function decides the flag value based on the operator and operand
    provided.
    """
    switcher = { 
        "equal": lambda operand1, operand2: True if(operand1 == operand2) else False,
        "lessthen": lambda operand1, operand2: True if(operand1 < operand2) else False,
        "graterthen": lambda operand1, operand2: True if(operand1 > operand2) else False
    } 
    flag = switcher.get(operator)
    return flag(operand1, operand2)


def get_user(endpoint, id):
    """
    Function to find the user based on the uuid provided.
    """
    url = '{}{}'.format(endpoint, id)
    user_obj = requests.get(url)
    return user_obj.json()['user']


def get_hirarchy_role(endpoint, program_id, member_id):
    """
    functions to find the list of the user with the levels provided
    """
    username = settings.AUTH_TOKEN_USERNAME
    password = settings.AUTH_TOKEN_PASSWORD
    token = get_auth_token(username, password)
    headers = {
        'Authorization': 'Bearer {}'.format(token),
        'User-Agent': 'PostmanRuntime/7.26.5'
        }
    url = '{}programs/{}/members/{}'.format(endpoint, program_id, member_id)
    
    hirarchy_obj = requests.get(url, headers=headers)
    return hirarchy_obj.json()['member']


def get_approval_value(rule_set, query_obj):
    '''
    return the list of the approval user's
    '''
    program_id = query_obj['program_id']
    for rule in rule_set.approval_config["rules"]:
        # flag = False
        for condition in rule["conditons"]:
            operand1 = ''
            operand2 = ''

            operator = condition['operator']
            if condition['column'] in query_obj:
                operand1 = query_obj[condition['column']]

            if condition['column_value_type'] == "static":
                logger.info("column_value_type is static")
                operand2 = condition['columne_value']
                
            elif condition['column_value_type'] == 'role':
                logger.info("column_value_type is role")
                obj_id = query_obj[condition['column']]
                try:
                    role_obj = get_hirarchy_role(
                        settings.HIRARCHY_ROLE_ENDPOINT,
                        program_id,
                        obj_id
                        )
                except:
                    logger.error("problem fetching role for ", obj_id)
                    continue
                else:
                    operand1 = role_obj['role']['name']
            flag = get_flag_value(operator, operand1, operand2)     
            if not flag:
                logger.info(
                    'No Rule set apply with the opertor {} and operands{}_{} provided'.format(
                        operator,
                        operand1,
                        operand2
                        )
                    )
                break
        if flag:
            user_list = []
            for action in rule["actions"]:
                approver_value = action["value"]
                approver_level = action["level"]
                approver_type = action["type"]
                logger.info(
                    'Rule set provides action with {}_{}_{}'.format(
                        approver_value,
                        approver_level,
                        approver_type
                        )
                    )
                if approver_type == "static":
                    logger.info("Approver Type is Static")
                    user = get_user(
                        settings.PROFILE_ENDPOINT,
                        approver_value
                        )
                    user_list.append(user['id'])
                    # Works fine till here 
                elif approver_type == 'role':
                    logger.info("Approver Type is role")
                    member_id = query_obj[approver_value] #hiring Manager_id
                    # need to find the id based on the job object
                    if approver_level == 0: 
                        try:
                            user = get_hirarchy_role(
                                settings.HIRARCHY_ROLE_ENDPOINT,
                                program_id,
                                member_id
                                )
                        except:
                            logger.error("Problem fetching User:", member_id)
                            continue
                        else:
                            member_id = user['id']
                            user_list.append(member_id)
                    
                    elif approver_level > 0:
                        for level in range(1, approver_level+1):
                            if level == 1:
                                member_id = query_obj[approver_value]
                            else:
                                member_id = supervisor_id
                            try:
                                user = get_hirarchy_role(
                                    settings.HIRARCHY_ROLE_ENDPOINT,
                                    program_id,
                                    member_id
                                )
                            except:
                                logger.error("Problem fetching User:", member_id)
                                break
                            else:                          
                                supervisor_id = user['supervisor_id']
                                user_list.append(supervisor_id)
            
            return user_list
