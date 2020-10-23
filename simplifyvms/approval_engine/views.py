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
from .utils import get_final_status, callback_function
# Create your views here.


log = logging.getLogger(__name__)

class ApprovalPendingView(APIView):
    '''
    This view help us to get all the pending approvals
    and update the pending approval
    '''
    def get_object(self, id):
        '''
        Return list of approvals of given id
        Parameters: id
        '''
        try:
            return ApprovalPending.objects.filter(approver_id=id)
        except:
            raise Http404

    def get(self, request, *args, **kwargs):
        '''
        Return the list of approvals based on given status
        Parameters: status, id
        '''
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
        '''
        Update the status of approval
        Parameters: id
        '''
        id = self.kwargs['id']
        try:
            obj = ApprovalPending.objects.get(id=id)
            serializer = ApprovalPendingSerializer(obj, data=request.data)
            if serializer.is_valid():
                serializer.save()
                final_status = get_final_status(obj.approval_entity.id)
                if final_status['status'] != 'pending':
                    response = callback_function(final_status)
                return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
            else:
                error = serializer.errors
        except Exception as e:
            error = e
        return Response({"error": "{}".format(error)},
                        status=status.HTTP_400_BAD_REQUEST)


class EntityPendingView(APIView):
    '''
    This view help us to get the entity object having 'pending' status
    '''
    def get(self, request, *args, **kwargs):
        '''
        Return the entity object having status 'pending'
        Parameters: entity_id
        '''
        entity_id = self.kwargs['entity_id']
        try:
            objs = ApprovalPending.objects.filter(
                approval_entity=entity_id,
                status='pending')
            for obj in objs:
                user_obj = get_user(settings.PROFILE_ENDPOINT, obj.approver_id)
                obj.approver_id = user_obj
            serializer = EntityPendingSerializer(objs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "{}".format(error)},
                            status=status.HTTP_400_BAD_REQUEST)



class EntityStatusView(APIView):
    '''
    This view help us to get the overall status of any entity
    '''
    def get(self, request, *args, **kwargs):
        '''
        Get overall status of the entity.
        if any one approval is pending then return pending
        if any one approval is rejected then return rejected
        Parameters: entity_id
        '''
        entity_id = self.kwargs['entity_id']
        try:
            objs = ApprovalPending.objects.filter(approval_entity=entity_id)
            status_list = []
            # Get the status of all approvals
            for obj in objs:
                status_list.append(obj.status)

            log.info(
                "Status of approvals belongs to entity is {}"
                .format(status_list))

            # Get the accumulative status
            if 'rejected' in status_list:
                final_status = 'rejected'
            elif 'pending' in status_list:
                final_status = 'pending'
            elif 'approved' in status_list:
                final_status = 'approved'
            else:
                final_status = 'No data found'
            entity_data = ApprovalEntity.objects.get(id=entity_id)
            serializer = ApprovalEntitySerializer(entity_data)
            data = {'status': final_status}
            data.update(serializer.data)

            return Response(data, status=status.HTTP_200_OK)
        except Exception as error:
            return Response({"error": "{}".format(error)},
                            status=status.HTTP_400_BAD_REQUEST)
