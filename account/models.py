from django.db import models
from django.conf import settings
from PIL import Image


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    created = models.DateTimeField(auto_now_add=True)



    # image thumbnail generation
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        # create 200px thumbnail
        img_200 = img.copy()
        img_200.thumbnail((200,200))
        img_200_path = self.image.path.replace('.png', '_200.png').replace('.jpg', '_200.jpg')
        img_200.save(img_200_path)

