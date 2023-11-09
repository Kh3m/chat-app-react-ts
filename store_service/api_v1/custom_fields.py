from rest_framework import serializers


class CustomHyperlinkedRelatedField(serializers.HyperlinkedRelatedField):
    """
    This custom field extends the standard HyperlinkedRelatedField provided by
    Django REST framework, providing flexibility for handling related fields by
    allowing both URLs and primary keys (PKs) as input.
    """

    def to_internal_value(self, data):
        if data is None:
            return None
        try:
            # First, try to interpret the input data as a URL
            return super().to_internal_value(data)
        except serializers.ValidationError as e:
            # If that fails, assume it's a PK and try to convert it to an object
            try:
                return self.get_queryset().get(pk=data)
            except Exception as e:
                print(e.message)
                if '/' in data:
                    raise serializers.ValidationError(
                        "Invalid hyperlink - No URL match.")
                if '-' in data:
                    raise serializers.ValidationError(
                        f"“{data}” is not a valid UUID.")
                raise serializers.ValidationError(e)


class CustomHyperLinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    """
    A custom serializer class for handling model serialization and deserialization
    with hyperlinks for related fields.

    This serializer is an extension of the standard HyperlinkedModelSerializer
    provided by Django REST framework. It is designed to provide more flexibility
    when dealing with relationships, allowing you to accept both URLs and primary keys
    (PKs) as input for related fields.

    Attributes:
        serializer_related_field (CustomHyperlinkedRelatedField): A custom serializer
            field used for relationships. It allows accepting both URLs and PKs
            as input.

    Usage:
    1. Inherit from this serializer class when creating serializers for your Django
       model classes.

    Example:
    ```python
    class MyModelSerializer(CustomHyperLinkedModelSerializer):
        class Meta:
            model = MyModel
            fields = "__all__"
    ```
    """
    serializer_related_field = CustomHyperlinkedRelatedField
