from approval_engine.models import ApprovalPending, ApprovalEntity
from django.conf import settings
import requests

def get_final_status(entity_id):
    entity_list = ApprovalPending.objects.filter(approval_entity=entity_id)
    entity = ApprovalEntity.objects.get(id=entity_id)
    status = [item.status for item in entity_list]
    if 'pending' in status:
        return {
            'entity_name': entity.entity_name,
            'entity_id': entity.entity_id,
            'status': 'pending'
        }
    elif 'rejected' in status:
        return {
            'entity_name': entity.entity_name,
            'entity_id': entity.entity_id,
            'status': 'rejected'
        }
    else:
        return {
            'entity_name': entity.entity_name,
            'entity_id': entity.entity_id,
            'status': 'approved'
        }


def callback_function(final_result):
    endpoint = '{}{}'.format(
        settings.ENDPOINTS[final_result['entity_name']],
        final_result['entity_id']
        )
    response = requests.put(url=endpoint, data=final_result)
    return response.status_code