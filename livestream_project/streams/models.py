import uuid
from django.db import models


class Stream(models.Model):
    """Model to represent a live stream session."""
    
    stream_id = models.CharField(max_length=100, unique=True, editable=False)
    title = models.CharField(max_length=200, default="Live Stream")
    host_name = models.CharField(max_length=100, default="Host")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    viewer_count = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.stream_id:
            self.stream_id = str(uuid.uuid4())[:8]  # Short unique ID
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} ({self.stream_id})"
    
    class Meta:
        ordering = ['-created_at']
