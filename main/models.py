from django.db import models

class FaceImage(models.Model):
    name = models.CharField(max_length=100)
    roll = models.CharField(max_length=100)
    address = models.TextField()
    image = models.ImageField(upload_to='media/face_images/')  # Storing images in media/face_images
    uploaded_at = models.DateTimeField(auto_now_add=True)

 