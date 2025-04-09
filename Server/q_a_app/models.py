from django.db import models
from django.utils import timezone 

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now) 

class RefreshTokens(models.Model):
    token = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class AccessTokens(models.Model):
    token = models.CharField(max_length=255, unique=True)
    refreshToken = models.ForeignKey(RefreshTokens, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class Question(models.Model):
    question = models.TextField(max_length=10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)

class Answer(models.Model):
    answer = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isActive = models.BooleanField(default=False)

class InteractionLog(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interactionType = models.CharField(max_length=10, choices=[('like', 'Like'), ('dislike', 'Dislike')])
