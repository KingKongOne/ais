from __future__ import unicode_literals

# Create your models here.
from django.db import models
from fair.models import Fair
# Model for company
class RecruitmentPeriod(models.Model):
    name = models.CharField(max_length=30)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    fair = models.ForeignKey('fair.Fair')
