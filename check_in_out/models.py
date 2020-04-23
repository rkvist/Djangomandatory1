from django.contrib.auth.models import User
from django.db import models
from newmaterial.models import Publishmaterial
from datetime import datetime

class check_in_out(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book_id = models.ForeignKey(Publishmaterial, on_delete=models.CASCADE)
    checked_out_datetime = models.DateTimeField(default=datetime.now())
    checked_in_datetime = models.DateTimeField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.id} - {self.user}: {self.book_id}'

    @property
    def date_diff(self):
        return (self.checked_out_datetime - self.checked_in_datetime).days