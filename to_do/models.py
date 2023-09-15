from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_description = models.CharField(max_length=200)
    date_added = models.DateTimeField("date added")
    parent_task = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="subtask")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.task_description