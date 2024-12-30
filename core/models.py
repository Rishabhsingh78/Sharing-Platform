from django.db import models

from django.contrib.auth.models import User

from taggit.managers import TaggableManager

class Question(models.Model):
    title = models.CharField(max_length=225)
    body = models.TextField()
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    tags = TaggableManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,related_name='answer')
    body = models.TextField()
    author  = models.ForeignKey(User,on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updates_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Answer to {self.question.title} by {self.author.username}"
    

class Reputation(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reputation = models.IntegerField(default=0)
    badges = models.JSONField(default=list)

    def __str__(self):
        return self.user.username

    
