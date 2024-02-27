from .models import AutoCreatedUpdatedMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import JSONField
from django.db.models import Q
import dataclasses
from inspect import getmembers
from django.utils.functional import cached_property


@dataclasses.dataclass
class DataType():

    @property
    def dict(self, notNone: bool = True):
        return {k: v for k, v in dataclasses.asdict(self).items() if notNone == False or v is not None}

    class Meta:
        pass


@dataclasses.dataclass
class EventType(DataType):

    pass


class AchieveType(EventType):
    pass
    # def query(self):
    #     return Q(key=self.__class__.__name__,data__contains=self.dict)

    # def progress(self,obj):
    #     if Achieve.objects.filter(obj.user_id).filter(self.query()).count()>0:
    #         count = len(self.__class__.nested)?len(self.__class__.nested):1
    #         return [count,count]
    #     else:
    #         query = Q()
    #         for achieve in self.__class__.nested:
    #             query |= Q(key=achieve.__class__.__name__,data__contains=achieve.dict)
    #         done = Achieve.objects.filter(obj.user_id).filter(query).count()
    #         return [,len(self.__class__.nested)]:


class Data(models.Model):
    class Meta:
        abstract = True

    class Types:
        pass

    key = models.CharField(
        verbose_name=_('key'),
        max_length=30,
        default=''
    )
    data = JSONField(default=dict, blank=True)


class Event(Data, AutoCreatedUpdatedMixin):
    class Meta:
        abstract = True

    class Types:
        pass

    user = models.ForeignKey(
        'users.User',
        verbose_name=_('user'),
        on_delete=models.CASCADE,
        null=True

    )

    @property
    def type(self):
        obj = getattr(self.Types, self.key, DataType)
        field_names = [f.name for f in dataclasses.fields(obj)]
        data = {k: v for k, v in self.data.items() if k in field_names}
        obj = obj(**data)
        result = {}
        if hasattr(obj, 'image'):
            result['image'] = obj.image
        if hasattr(obj, 'title'):
            result['title'] = obj.title
        if hasattr(obj, 'description'):
            result['description'] = obj.description
        return result
        # field_names = [f.name for f in dataclasses.fields(obj)]
        # data = {k: v for k, v in self.data.items() if k in field_names}
        # return {k: v for k, v in dict(getmembers(obj(**data)))['__dict__'].items() if k not in field_names}