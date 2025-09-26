from django.db import models
from django.contrib.auth import get_user_model
User=get_user_model()
class Repository(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='repos')
    name=models.CharField(max_length=200)
    description=models.TextField(blank=True)
    is_private=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('owner','name')
    def __str__(self): return f"{self.owner.username}/{self.name}"
class PullRequest(models.Model):
    repository=models.ForeignKey(Repository,on_delete=models.CASCADE,related_name='prs')
    title=models.CharField(max_length=255)
    body=models.TextField(blank=True)
    source_branch=models.CharField(max_length=200)
    target_branch=models.CharField(max_length=200,default='main')
    opened_by=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    is_merged=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
