from approval_engine import approval_rule_set
from django.conf import settings
import json
import requests

job = {
    'id': 1,
    'program_id': 1, 
    "amount": 5000,
    "created_by": "990b0e98-0561-411e-aa65-51ad8023a3f4"
}


def get_flag_value(operator, operand1, operand2):
    """
    Function decides the flag value based on the operator and operand
    provided.
    """
    switcher = { 
        "equal": lambda operand1, operand2: True if(operand1 == operand2) else False, 
        "lessthen":lambda operand1, operand2: True if(operand1 < operand2) else False, 
        "graterthen": lambda operand1, operand2: True if(operand1 > operand2) else False 
    } 
    flag = switcher.get(operator)
    return flag(operand1, operand2)


def get_approval_value(rule_set, query_obj):
    '''
    return the list of the approval user's
    '''
    for rule in rule_set.approval_config["rules"]:
        flag = False
        for condition in rule["conditons"]:
            operand1 = ''
            operand2 = ''

            operator = condition['operator']
            if condition['column'] in query_obj:
                operand1 = query_obj[condition['column']]

            if condition['column_value_type'] == "static":
                operand2 = condition['columne_value']
                
            elif condition['column_value_type'] == 'role':
                obj = query_obj[condition['column']]
                #Need Clearification on this
                role = get_role(
                    settings.HIRARCHY_ENDPOINT,
                    program_id,
                    role_id
                    )
                operand1 = role

            if operator == 'equal':
                if operand1 == operand2:
                    flag = True
                else:
                    flag = False
            elif operator == 'lessthen':
                if operand1 < operand2:
                    flag = True
                else:
                    flag = False
            elif operator == 'graterthen':
                if operand1 > operand2:
                    flag = True
                else:
                    flag = False
            
            if not flag:
                break
        flag = True
        if flag:
            user_list = []
            for action in rule["actions"]:
                approver_value = action["value"]
                approver_level = action["level"]
                approver_type = action["type"]
                if approver_type == "static":
                    user = get_user(
                        settings.PROFILE_ENDPOINT,
                        approver_value
                        )
                    user_list.append(user.id)
                elif approver_type == 'role':
                    member_id = query_obj[approver_value]
                    # need to find the id based on the job object
                    program_id = query_obj[program_id]
                    if approver_level == 0: 
                        user = get_hirarchy(
                            settings.HIRARCHY_ENDPOINT,
                            program_id,
                            member_id
                            )
                        member_id = user['id']
                        user_list.append(member_id)
                    
                    elif approver_level > 0:
                        for level in range(approver_level):
                            if level == 0:

                                member_id = memmber_id
                            else:
                                member_id = supervisor_id

                            user = get_hirarchy(
                                settings.HIRARCHY_ENDPOINT,
                                program_id,
                                member_id
                            )
                            supervisor_id = user['supervisor_id']
                            user_list.append(supervisor_id)
            return user_list


#get_approval_value(approval_rule_set, job)

def get_user(endpoint, id):
    """
    Function to find the email based on the uuid provided.
    """
    url = '{}{}'.format(endpoint, id)
    user_obj = requests.get(url)
    return user_obj.json()['user']


def get_hirarchy(endpoint, program_id, member_id):
    """
    functions to find the list of the user with the levels provided
    """
    url = '{}programs{}/members/{}'.format(endpoint, program_id, member_id)
    hirarchy_obj = requests.get(url)
    return hirarchy_obj.json()['member']


def get_role(endpoint, program_id, role_id):
    """
    functions to find the list of the user with the levels provided
    """
    url = '{}programs{}/members/{}'.format(endpoint, program_id, role_id)
    role_obj = requests.get(url)
    return role_obj.json()['role']
