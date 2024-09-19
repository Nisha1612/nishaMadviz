import uuid
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'


class AIUseCase(models.Model):
    CATEGORY_CHOICES = [
        ('health_monitoring', 'Health Monitoring'),
        ('multi_modal_analytics', 'Multi Modal Analytics'),
        ('image_analysis', 'Image Analysis'),
        ('summarization', 'Summarization'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    example_name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    link = models.URLField(max_length=200, blank=True, null=True)  # URL field for detail page

    class Meta:
        unique_together = ('user', 'example_name')
        permissions = [
            ('can_add_aiusecase', 'Can add AI Use Case'),
        ]

    def __str__(self):
        return f"{self.get_category_display()}: {self.example_name} (by {self.user.username})"
