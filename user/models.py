from django.db import models

# Create your models here.

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True, db_index=True)
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)
    name = models.CharField(max_length=30, unique=True, db_index=True)
    password = models.CharField(max_length=64)
    jointime = models.DateTimeField()
    sp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    status = models.IntegerField(default=0)

    class Meta:
        db_table = 'user'