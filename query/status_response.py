from django.db import models

from django.contrib.auth.models import User


# StatusResponse model holds data from queries;
# contains info for all all responses
class StatusResponse(models.Model):
  owner = models.ForeignKey(User, related_name="owners_query")
  #owner = models.OneToOneField(User)
  query_id = models.IntegerField() 
  file = models.CharField(max_length=108, default="n/a")
  cpu = models.IntegerField()
  completed = models.IntegerField()
  used = models.IntegerField()
  available = models.IntegerField()

##############################################
# create an instance of StatusResponse, then #
# create an object of one of the following:  #
##############################################

# QueryResponsesObject
class QueryResponsesObject:
  def __init__(self, query_id, file):
    self.query_id = query_id
    self.file = file

# AnalysisResponsesObject
class AnalysisResponsesObject:
  def __init__(self, query_id, file):
    self.query_id = query_id
    self.file = file

# StatusResponseObject
class StatusResponsesObject:
  def __init__(self, query_id, cpu, completed, used, available):
    self.query_id = query_id
    self.cpu = cpu
    self.completed = completed
    self.used = used
    self.available = available
  
