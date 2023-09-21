from django.core.serializers.json import DjangoJSONEncoder
from ulid import ULID


class ULIDJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, ULID):
            return str(obj)
        return super().default(obj)
