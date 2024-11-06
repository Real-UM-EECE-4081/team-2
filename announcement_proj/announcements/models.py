from django.db import models
from django.contrib.auth.models import User

# Model for Sections
class Section(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model for Announcements
class Announcement(models.Model):
    TOPIC_CHOICES = [
        ('General', 'General'),
        ('Urgent', 'Urgent'),
        ('Reminder', 'Reminder'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.DateTimeField(null=True, blank=True)
    sent = models.BooleanField(default=False)
    sections = models.ManyToManyField(Section)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Model for Comments/Replies
class Comment(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.announcement.title}"
