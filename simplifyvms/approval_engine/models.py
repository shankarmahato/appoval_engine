from django.db import models
from django_mysql.models import JSONField
import uuid

STATUS = (
    ("approved", "Approved"),
    ("rejected", "Rejected"),
    ("pending", "Pending")
)


class ApprovalEntity(models.Model):
    '''
    Keeps the record of the entity recevied from the queue
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity_name = models.CharField(max_length=100)
    entity_id = models.CharField(max_length=100, db_index=True)
    entity_obj = JSONField()

    def __str__(self):
        '''
        String Representation of the Table
        '''
        return self.entity_name.title()

    class Meta:
        '''
        Meta description for the table
        '''
        db_table = 'approval_entity'
        verbose_name = 'Approval Entity'
        verbose_name_plural = 'Approval Entitys'


class ApprovalPending(models.Model):
    '''
    Keeps the track of whether approval has been pending or not
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    approval_entity = models.ForeignKey(
        'ApprovalEntity',
        related_name='approval_pending_entity',
        on_delete=models.CASCADE
        )
    sequence_number = models.IntegerField()
    approver_id = models.CharField(max_length=100, db_index=True)
    status = models.CharField(
        max_length=100,
        choices=STATUS,
        default="pending"
        )

    def __str__(self):
        '''
        String Representation of the Table
        '''
        return '{}_{}_{}'.format(
            self.approval_entity,
            self.sequence_number,
            self.status
            )

    class Meta:
        '''
        Meta description for the table
        '''
        db_table = 'approval_pending'
        verbose_name = 'Approval Pending'
        verbose_name_plural = 'Approval Pendings'
