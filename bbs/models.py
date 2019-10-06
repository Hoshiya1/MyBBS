from django.db import models

# Create your models here.

class Dictionary(models.Model):
    id = models.IntegerField(primary_key=True)
    mean = models.CharField(max_length=10)

class Part(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10)
    level = models.IntegerField(default=1)

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    part_id = models.ForeignKey(Part, on_delete=models.CASCADE, db_column='part_id')
    uid = models.IntegerField(db_index=True)
    time = models.DateTimeField(auto_now_add=True, db_index=True)
    title = models.CharField(max_length=100, db_index=True)
    content = models.TextField()
    hidden = models.CharField(max_length=500, null=True)

class Reply(models.Model):
    id = models.AutoField(primary_key=True)
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE, db_index=True, db_column='post_id')
    uid = models.IntegerField(db_index=True)
    reply_id = models.IntegerField(null=True)
    time = models.DateTimeField(auto_now_add=True, db_index=True)
    content = models.CharField(max_length=500)
    hidden = models.CharField(max_length=500, null=True)
