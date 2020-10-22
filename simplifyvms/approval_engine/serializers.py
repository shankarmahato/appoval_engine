from rest_framework import serializers
from approval_engine.models import ApprovalPending,ApprovalEntity


class ApprovalEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalEntity
        fields = "__all__"

class ApprovalPendingSerializer(serializers.ModelSerializer):
    # approval_pending_entity = ApprovalEntitySerializer()
    class Meta:
        model = ApprovalPending
        fields = (
            "id",
            "approval_entity",
            # "approval_pending_entity",
            "sequence_number",
            "approver_id",
            "status"
            )
        depth=1


class EntityPendingSerializer(serializers.ModelSerializer):
    approver_id = serializers.JSONField()

    class Meta:
        model = ApprovalPending
        fields = (
        "id",
        "approval_entity",
        # "approval_pending_entity",
        "sequence_number",
        "approver_id",
        "status"
        )