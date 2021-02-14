import uuid
from django.db import models
import redis

redis_instance = redis.Redis(host='localhost',
                             port='6379',
                             db=0)


# Create your models here.


class User(models.Model):
    user_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4,
                               editable=False)
    point = models.FloatField(default=0, blank=True)
    display_name = models.CharField(max_length=32)
    country = models.CharField(max_length=2)
    rank = models.IntegerField(editable=False, blank=True, null=True)

    def __str__(self):
        return str(self.display_name)
