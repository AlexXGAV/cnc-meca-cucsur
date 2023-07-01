from typing import Iterable, Optional
from django.db import models

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
        verbose_name = 'compañero de equipo'
        verbose_name_plural = 'compañeros de equipo'

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: str | None = ..., update_fields: Iterable[str] | None = ...) -> None:
        return super().save(force_insert, force_update, using, update_fields)
