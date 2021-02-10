import uuid

from django.db import models


# Create your models here.


class User(models.Model):
    user_id = models.UUIDField(primary_key=True,
                               default=uuid.uuid4,
                               editable=False)
    display_name = models.CharField(max_length=32)
    points = models.IntegerField()
    rank = models.IntegerField()

    def __str__(self):
        return self.rank, self.user_id, self.points, self.display_name
