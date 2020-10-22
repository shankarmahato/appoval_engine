from django.urls import path
from approval_engine import views
app_name = 'approval_engine'

urlpatterns = [
    path('<uuid:id>', views.ApprovalPendingView.as_view(), name='approval'),
    # path('approval_entity', views.ApprovalEntityView.as_view(), name='status'),     
    path('entity_id/<uuid:entity_id>', views.EntityPendingView.as_view(), name='entity_pending')
]