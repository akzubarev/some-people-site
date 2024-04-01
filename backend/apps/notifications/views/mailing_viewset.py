from base64 import b64decode

from django.core.files.base import ContentFile
from rest_framework import generics
from rest_framework.response import Response

from apps.notifications.models import Notification
from apps.notifications.serializers import MailingSerializer
from apps.users.models import User


class MailingViewSet(generics.GenericAPIView):
    serializer_class = MailingSerializer

    def put(self, request):
        # if not request.user.access:
        #     raise PermissionDenied('You dont have access')
        data = request.data
        if not isinstance(data.get("text"), list):
            data["text"] = [data.get("text")]

        search = ""
        filters = []
        if "search" in data:
            search = data.pop("search")

        if "filters" in data:
            filters = data.pop("filters")

        data.update({
            "image": self.convert_image(data["image"]),
            "text": "\n".join(data["text"]),
            "locales": [request.user.locale],
            "private": True,
        })
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        mailing = serializer.save()
        targets = User.objects.filter(
            # search_query=search, filters=filters,
        )
        for target in targets:
            Notification.objects.create(user=target.user, mailing=mailing)
        return Response(serializer.data)

    def convert_image(self, image):
        if image and isinstance(image, str) and ';base64,' in image:
            image_format, img_str = image.split(';base64,')
            extension = image_format.split('/')[-1]
            return ContentFile(b64decode(img_str), f'image.{extension}')
