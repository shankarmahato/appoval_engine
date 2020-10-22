# importing dependencies.
# from retrying import retry
from django_stomp.services.consumer import Payload

# from listner.serializers import ValidationSerializer
from approval_engine.config import get_approval_value
from approval_engine import approval_rule_set
from approval_engine.models import ApprovalPending, ApprovalEntity
from django.conf import settings

logger = settings.LOGGER

def save_to_database(approver_list):
    '''
    save sequence_number and approver_id in the ApprovalPending Table 
    '''
    seq_no = 1
    for approver_obj in approver_list:
       
        ApprovalPending.objects.create(
            approval_entity=ApprovalEntity.objects.get(id='78f8d29c-2586-4618-9c61-394dbc14eb67'),
            sequence_number=seq_no,
            approver_id=approver_obj
        )
        seq_no = seq_no+1
    return True


def submit_approval(payload: Payload) -> None:
    """
    Listner function: Pick messages from the queue and work accordingly.
    """
    my_header = payload.headers
    approval_args = payload.body
    logger.info({
        "task_id": my_header['task_id'],
        "headers": my_header, "body": approval_args,
        "message": "Received Task"})
    # user_list = get_approval_value(
    #     approval_rule_set['approval_config'],
    #     approval_args['data']
    #     )
    user_list = [1,2,3]
    result = save_to_database([user_list])
    if result:
        payload.ack()
    else:
        payload.nack()
