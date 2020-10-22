import logging
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .models import ApprovalPending, ApprovalEntity
# Create your views here.


log = logging.getLogger(__name__)


class ApprovalView(APIView):
    '''
    Get the list of data based upon approval status and approvar id
    '''

    def get(self, request):
        """
        Get the list of data based upon approval status and approvar id
        """
        approval_status = request.GET.get('status')
        approver_id = request.GET.get('approver_id')
        log.info("Get the approval entities having status = {} and approver id  = {} ".format(approval_status,approver_id))
        if approval_status is not None and approver_id is None:
            data = ApprovalPending.objects.filter(status=approval_status).values()
        elif approval_status is None and approver_id is not None:
            data = ApprovalPending.objects.filter(approver_id=approver_id).values()
        elif approval_status is not None and approver_id is not None:
            data = ApprovalPending.objects.filter(Q(status=approval_status) & Q(approver_id=approver_id)).values()

        if data:
            for i in data:
                entity_data = ApprovalEntity.objects.get(id=i['approval_entity_id'])
                # import pdb;pdb.set_trace()
                print(entity_data)
                i['entity_type'] = entity_data.entity_name
                i['entity_object'] = entity_data.entity_obj
            return Response({"data":data}, status.HTTP_200_OK)
        else:
            return Response({"message":"No data found"}, status.HTTP_204_NO_CONTENT)


class StatusView(APIView):
    '''
    Display the consolidated status
    '''

    def get(self, request):
        '''
        Get the consolidated status based upon entity id 
        '''
        entity_id = request.GET.get('entity_id')
        data = ApprovalPending.objects.filter(approval_entity__entity_id=entity_id).values()

        status_list = []
        for i in data:
            status_list.append(i['status'])

        if 'rejected' in status_list:
            final_status = 'rejected'
        elif 'pending' in status_list:
            final_status = 'pending'
        elif 'approved' in status_list:
            final_status = 'approved'
        else:
            final_status = 'No data found'

        if final_status == 'No data found':
            return Response({"message":final_status}, status.HTTP_204_NO_CONTENT) 
        else:
            return Response({"data":final_status}, status.HTTP_200_OK) 

    def put(self, request):
        '''
        Get the consolidated status based upon entity id 
        '''
        approver_id = request.GET.get('approver_id')
        approver_status = request.GET.get('status')
        try:
            approver_data = ApprovalPending.objects.get(approver_id=approver_id)
            approver_data.status = approver_status
            approver_data.save()

            return Response({"Message":'Status Updated Successfully'}, status.HTTP_200_OK) 

        except Exception:
                # log.error("Configuration id not found {}".format(e))
            return Response({"message":"Approver Id Not Found"},status.HTTP_204_NO_CONTENT)



