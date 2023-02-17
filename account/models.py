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

        # create 400px thumbnail (if premium or enterprise user)
        if self.user.account_tier in ('premium', 'enterprise'):
            img_400 = img.copy()
            img_400.thumbnail((400, 400))
            img_400_path = self.image.path.replace('.png', '_400.png').replace('.jpg', '_400.jpg')


        # store thumbnail paths in database
        self.thumbnail_200_path = img_200_path
        if self.user.account_tier in ('premium', 'enterprise'):
            self.thumbnail_400_path = img_400_path
        self.save()

    class Meta:
        ordering = ('-created')