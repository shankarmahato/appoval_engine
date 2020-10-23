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
    def get(self, request, *args, **kwargs):
        entity_id = self.kwargs['entity_id']
        objs = ApprovalPending.objects.filter(approval_entity=entity_id, status='pending')
        for obj in objs:
            user_obj = get_user(settings.PROFILE_ENDPOINT, obj.approver_id)
            obj.approver_id =  user_obj
        serializer = EntityPendingSerializer(objs, many=True)
        return Response(serializer.data)