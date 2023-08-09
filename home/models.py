"""Models for the home page"""

import os
from django.db import models
from django.utils.translation import gettext_lazy as _

class Teammate(models.Model):
    first_name = models.CharField(max_length=30)
    second_name = models.CharField(max_length=30, null=True, blank=True)
    first_last_name = models.CharField(max_length=40)
    second_last_name = models.CharField(max_length=40)

    career = models.CharField(max_length=40)

    image = models.ImageField(upload_to='img/team')

    twitter_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = _("teammate")
        verbose_name_plural = _("teammates")

    def save(self, *args, **kwargs):

        if self.first_name and self.first_last_name:
            new_image_name = f"{self.first_name}_{self.first_last_name}"
            ext = os.path.splitext(self.image.name)[1]  # Get the image extension
            new_image_name_with_extension = f"{new_image_name}{ext}"
            self.image.name = new_image_name_with_extension
        
        super(Teammate, self).save(*args, **kwargs)
    
    def __str__(self):
        names = [self.first_name, self.second_name, self.first_last_name, self.second_last_name]
        full_name = " ".join(filter(None, names))
        return full_name


class Gallery(models.Model):

    class type_of_gallery(models.TextChoices):
        DEVELOPMENT = "DEV", _('development')
        RESULT = "RE", _('result')
        EXAMPLE = "EX", _('example')

    gallery = models.CharField(
        choices=type_of_gallery.choices,
        default=type_of_gallery.DEVELOPMENT,
        max_length=30
    )

    title = models.CharField(_("title"), max_length=40)

    description = models.CharField(_("description"), max_length=300)

    image = models.ImageField(_("image"), upload_to='img/gallery')

    class Meta:
        verbose_name = _('gallery')
        verbose_name_plural = _('galleries')

    def __str__(self):
        return f"{self.get_gallery_display()} - {self.title}"

    def save(self, *args, **kwargs):

        if self.title:
            new_image_name = f"{self.gallery}-{self.title.strip()}"
            ext = os.path.splitext(self.image.name)[1]  # Get the image extension
            new_image_name_with_extension = f"{new_image_name}{ext}"
            self.image.name = new_image_name_with_extension
        
        super(Gallery, self).save(*args, **kwargs)
