from django.db import models

# Create your models here.
class Inimg(models.Model):
    name = models.CharField(max_length=50)
    main_input_img = models.ImageField(upload_to='images/')