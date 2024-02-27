
class SerializerByActionViewSet:

    def get_serializer_class(self):

        if hasattr(self, 'serializer_class_by_action'):
            return self.serializer_class_by_action.get(self.action, self.serializer_class_by_action.get('default', self.serializer_class))

        return super().get_serializer_class()


class SerializerContextViewsSet:

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


class PermissionsByActionViewSet:
    def get_permissions(self):
        try:
            self.permission_classes_by_action.get(self.action, self.permission_classes_by_action['default'])
        except (KeyError, AttributeError):
            return super().get_permissions()


class UUIDLookupViewSet:
    lookup_field = "uuid"
    lookup_value_regex = "[0-9a-z]{8}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{4}-[0-9a-z]{12}"