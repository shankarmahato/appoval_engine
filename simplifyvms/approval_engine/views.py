import logging
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from approval_engine.serializers import ApprovalPendingSerializer,ApprovalEntitySerializer, EntityPendingSerializer
from .models import ApprovalPending, ApprovalEntity
from django.http import Http404
from .config import get_user
from django.conf import settings
import json
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

# Create your views here.


log = logging.getLogger(__name__)


# class ApprovalView(APIView):
#     '''
#     Get the list of data based upon approval status and approvar id
#     '''

#     def get(self, request):
#         """
#         Get the list of data based upon approval status and approvar id
#         """
#         approval_status = request.GET.get('status')
#         log.info("Approval status is {}".format(approval_status))

#         approver_id = request.GET.get('approver_id')
#         log.info("Approver id  is {}".format(approver_id))

#         # Get the approvals based upon approval status and approval id 
#         if approval_status is not None and approver_id is None:
#             data = ApprovalPending.objects.filter(status=approval_status).values()
#         elif approval_status is None and approver_id is not None:
#             data = ApprovalPending.objects.filter(approver_id=approver_id).values()
#         elif approval_status is not None and approver_id is not None:
#             data = ApprovalPending.objects.filter(Q(status=approval_status) & Q(approver_id=approver_id)).values()

#         # log.info("Approval objects based on approval status and approver id are {}".format(data))

#         if data:
#             # Get the entity objects of all the approvals
#             for i in data:
#                 entity_data = ApprovalEntity.objects.get(id=i['approval_entity_id'])
#                 i['entity_type'] = entity_data.entity_name
#                 i['entity_object'] = entity_data.entity_obj
#             return Response({"Data":data}, status.HTTP_200_OK)
#         else:
#             return Response({"Message":"No data found"}, status.HTTP_204_NO_CONTENT)


# class StatusView(APIView):
    # '''
    # Display the consolidated status
    # '''

    # def get(self, request):
    #     '''
    #     Get the consolidated status based upon entity id 
    #     '''
    #     entity_id = request.GET.get('entity_id')
    #     log.info("Entity id is {}".format(entity_id))

    #     # Get all the approvals of given entity id
    #     approvals = ApprovalPending.objects.filter(approval_entity__entity_id=entity_id).values()
        
    #     status_list = []
    #     # Get the status of all approvals
    #     for i in approvals:
    #         status_list.append(i['status'])

    #     log.info("Status of approvals belogs to entity is {}".format(status_list))

    #     # Check the status if any one of status is rejected then overall status is rejected 
    #     # If any one of status is pending then overall status is pending else approved
    #     if 'rejected' in status_list:
    #         final_status = 'rejected'
    #     elif 'pending' in status_list:
    #         final_status = 'pending'
    #     elif 'approved' in status_list:
    #         final_status = 'approved'
    #     else:
    #         final_status = 'No data found'

    #     data = {}

    #     # Get the entity obejct
    #     entity_data = ApprovalEntity.objects.get(entity_id=entity_id)
    #     data['entity_type'] = entity_data.entity_name
    #     data['entity_object'] = entity_data.entity_obj
    #     data['final_status'] = final_status

    #     log.info("Accumulative status is {}".format(final_status))

    #     if final_status == 'No data found':
    #         return Response({"Message":final_status}, status.HTTP_204_NO_CONTENT) 
    #     else:
    #         return Response({"Data":data}, status.HTTP_200_OK) 

    # def put(self, request):
    #     '''
    #     Get the consolidated status based upon entity id 
    #     '''
    #     approver_id = request.GET.get('approver_id')
    #     log.info("Approver id is {}".format(approver_id))

    #     approver_status = request.GET.get('status')
    #     log.info("Approver status is {}".format(approver_status))

    #     try:
    #         data = {}
    #         # Get the approval object
    #         approver_data = ApprovalPending.objects.get(approver_id=approver_id)

    #         # Update the status
    #         approver_data.status = approver_status
    #         approver_data.save()
            
    #         # Get the entity details
    #         entity_data = ApprovalEntity.objects.get(id=approver_data.approval_entity_id)
    #         data['entity_type'] = entity_data.entity_name
    #         data['entity_object'] = entity_data.entity_obj
    #         data['message'] = 'Status Updated Successfully'

    #         log.info("Status updated successfully ")
    #         return Response({"Data":data}, status.HTTP_200_OK) 

    #     except Exception as e:
    #         log.error("Approver id not found {}".format(e))
    #         return Response({"Message":"Approver Id Not Found"},status.HTTP_204_NO_CONTENT)

class ApprovalPendingView(APIView):
    def get_object(self, id):
        try:
            return ApprovalPending.objects.filter(approver_id=id)
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        _status = request.GET.get('status')
        if _status:
            obj = self.get_object(id).filter(status=_status)
        else:
            obj = self.get_object(id)
        serializer = ApprovalPendingSerializer(obj,many=True)
        return Response({
            "data":serializer.data,
            "status": status.HTTP_200_OK 
        })

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        try:
            obj = ApprovalPending.objects.get(id=id)
            serializer = ApprovalPendingSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                # settings.LOGGER.info(
                #     "JobTitleDetailView >> put >> response: {}".format(
                #         serializer.data))
                return Response(serializer.data,
                                status=status.HTTP_202_ACCEPTED)
            else:
                error = serializer.errors
        except Exception as e:
            error = e
        # settings.LOGGER.info(
        #     "JobTitleDetailView >> put >> error: {}".format(error))
        return Response({"error": "{}".format(error)},
                        status=status.HTTP_400_BAD_REQUEST)



class EntityPendingView(APIView):
    def get(self, request, *args, **kwargs):
        entity_id = self.kwargs['entity_id']
        objs = ApprovalPending.objects.filter(approval_entity=entity_id, status='pending')
        for obj in objs:
            user_obj = get_user(settings.PROFILE_ENDPOINT, obj.approver_id)
            obj.approver_id =  user_obj
        serializer = EntityPendingSerializer(objs, many=True)
        return Response(serializer.data)