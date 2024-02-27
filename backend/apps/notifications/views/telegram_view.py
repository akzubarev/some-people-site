from rest_framework import generics
from rest_framework.response import Response

from ..models import Telegram
from ..serializers import TelegramSerializer


class TelegramView(generics.GenericAPIView):
    queryset = Telegram.objects
    serializer_class = TelegramSerializer

    @classmethod
    def get_extra_actions(cls):
        return []

    def get_object(self):
        instance = Telegram.objects.filter(user=self.request.user)
        if instance:
            return instance[0]
        else:
            from ..utils import generate_telegram_code
            code = generate_telegram_code(self.request.user.id)
            return Telegram(code=code)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = TelegramSerializer(instance=instance)
        return Response(serializer.data)
