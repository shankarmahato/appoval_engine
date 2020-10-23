# importing dependencies.
# from retrying import retry
from django_stomp.services.consumer import Payload
from django.shortcuts import get_object_or_404
# from listner.serializers import ValidationSerializer
from approval_engine.config import get_approval_value
from approval_engine import approval_rule_set 
from approval_engine.models import ApprovalPending, ApprovalEntity
from django.conf import settings
import uuid
import requests
import json

logger = settings.LOGGER

def save_to_database(approver_list, approval_entity_obj):
    '''
    save sequence_number and approver_id in the ApprovalPending Table 
    '''
    seq_no = 1
    for approver_obj in approver_list:
        ApprovalPending.objects.create(
            approval_entity=ApprovalEntity.objects.get(id=approval_entity_obj),
            sequence_number=seq_no,
            approver_id=approver_obj
        )
        seq_no = seq_no+1
    return True

def submit_to_sender(endpoint, data):
    """
    This function is used to submit motifications.
    """
    response = requests.post(settings.SENDER_ENDPOINT,
                data=json.dumps(data),
                headers={'Content-Type': 'application/json'})
    logger.info("Response from sender service: ",response)
    return response.status_code

def submit_approval(payload: Payload) -> None:
    """
    Listner function: Pick messages from the queue and work accordingly.
    """
    my_header = payload.headers
    approval_args = payload.body
    entity_name = approval_args['module'].lower()
    entity_obj = approval_args['data']
    entity_id = entity_obj['id']

    logger.info({
        "task_id": my_header['task_id'],
        "headers": my_header, "body": approval_args,
        "message": "Received Task"})
 
    user_list = get_approval_value(
        approval_rule_set,
        entity_obj
        )

    try:  
        approval_entity_obj = ApprovalEntity.objects.create(
        entity_name=entity_name, entity_id=entity_id, entity_obj=entity_obj)
        save_to_database(user_list, approval_entity_obj.id)
    except:
        logger.info({
                "task_id": my_header['task_id'],
                "message": "Error while saving"})
        payload.nack()
        return
    else:
        notification_data = {
            "program_id": entity_obj['program_id'],
            "category": entity_name,
            "event": approval_args["event"],
            "receivers": user_list
        }
        status_code = submit_to_sender(settings.SENDER_ENDPOINT, notification_data)
        if status_code == '202':
            logger.info({
                "task_id": my_header['task_id'],
                "message": "Processed Successfully"})
            payload.ack()
            return
        else:
            logger.info({
                "task_id": my_header['task_id'],
                "message": "Error sending Email"})
            payload.nack()
            return
