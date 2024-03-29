import datetime
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.db import models
from PIL import Image

from .tasks import test


def get_upload_path(instance, filename):
    return f"usr_{instance.maker.id}/uploads/images/{filename}"


def get_thumbnail_path(instance, filename):
    return f"usr_{instance.maker.id}/uploads/thumbnails/{filename}"


def get_deepzoom_path(instance, filename):
    directory = str(filename).replace(".dzi", "")
    return f"usr_{instance.maker.id}/uploads/dzis/{directory}/{filename}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.slug}/"


class Map(models.Model):
    category = models.ForeignKey(
        Category, related_name="maps", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=get_upload_path)
    slug = models.SlugField()
    thumbnail = models.ImageField(upload_to=get_thumbnail_path, blank=True, null=True)
    deepzoom = models.FileField(upload_to=get_deepzoom_path, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    pub_date = models.DateField(default=datetime.datetime.today)
    maker = models.ForeignKey(
        User, related_name="entries", blank=True, on_delete=models.PROTECT
    )
    last_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(
        User, related_name="entry_modifiers", blank=True, on_delete=models.PROTECT
    )

    class Meta:
        ordering = ("-date_added",)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/{self.category.slug}/{self.slug}/"

    def get_image(self):
        if self.image:
            return "http://127.0.0.1:8000" + self.image.url
        return ""

    def get_dzi_path(self):
        a = list(Path(self.image.url).parts)[2:]
        *dzi, _ = a[-1].split(".")
        dzi = ".".join(dzi)
        return str(Path(*a[:-2]) / "dzis" / dzi / f"{dzi}.dzi")

    def get_deepzoom(self):
        dzi_path = self.get_dzi_path()
        if not self.deepzoom:
            self.deepzoom.name = dzi_path
            self.save()
        return self.deepzoom.url

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:  # thi makes no sense if we are creating on save
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return self.thumbnail.url
            else:
                return ""

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img = img.convert("RGB")
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, "JPEG", quality=100)

        print("qwer", image.name)
        thumbnail = File(thumb_io, name=image.name.replace("uploads/", "thumbnails/"))

        return thumbnail

    def save(self, *args, **kwargs):
        print("HERE I AM!", self.image.name)
        super(Map, self).save(*args, **kwargs)
        if not self.deepzoom:
            dzi_path = self.get_dzi_path()
            test.delay(str(self.image.file), str(settings.MEDIA_ROOT / dzi_path))
