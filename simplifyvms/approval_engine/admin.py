from django.contrib import admin
from approval_engine.models import (
    ApprovalEntity,
    ApprovalPending)


admin.site.register(ApprovalEntity)
admin.site.register(ApprovalPending)
