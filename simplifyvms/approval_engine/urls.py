from django.urls import path
from approval_engine import views
app_name = 'approval_engine'

urlpatterns = [
    path('', views.ApprovalView.as_view(), name='approval'),
    path('status', views.StatusView.as_view(), name='status'),
        
]