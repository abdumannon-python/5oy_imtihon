from django.db import models

from User.models import Users
from product.models import Products


class Comment(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='comments')
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='comments')
    created_at=models.DateTimeField(auto_now_add=True)
    desc=models.TextField()

    def __str__(self):
        return f"{self.user.username} izohi {self.desc}"
class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    users = models.ForeignKey(Users, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class Message(models.Model):
    sender=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='sent_messages')
    receiver=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='receiver_messages')
    product=models.ForeignKey(Products,on_delete=models.SET_NULL,null=True,blank=True)
    desc=models.TextField(blank=True)
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='messages/', null=True, blank=True)

    def __str__(self):
        return f"{self.sender.username} ---> {self.receiver.username}"

    class Meta:
        ordering = ['created_at']

