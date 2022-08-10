import base64
import uuid

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.fields import SkipField


class ImageBase64Field(serializers.ImageField):
    """
    DRF-Base64: https://bitbucket.org/levit_scs/drf_base64/src/master/
    """

    @staticmethod
    def _decode(data):
        if isinstance(data, str) and data.startswith("data:"):
            b64_format, datastr = data.split(";base64,")
            ext = b64_format.split("/")[-1]

            if ext[:3] == "svg":
                ext = "svg"

            data = ContentFile(
                base64.b64decode(datastr),
                name="{}.{}".format(uuid.uuid4(), ext),
            )

        elif isinstance(data, str) and data.startswith("http"):
            raise SkipField()

        return data

    def to_internal_value(self, data):
        data = self._decode(data)
        return super().to_internal_value(data)
