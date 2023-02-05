from __future__ import absolute_import
from celery import shared_task

import deepzoom


creator = deepzoom.ImageCreator(
    tile_format="png",
    image_quality=1,
    resize_filter="antialias",
)


@shared_task
def test(img, out):
    creator.create(img, out)
    return f'The tasks executed with the following parameter: {out}'
