from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from api_v1.models import Product, Category


# @registry.register_document
# class ProudctDocument(Document):
#     class Index:
#         name = "products"

#     class Django:
#         model = Product
#         fields = [
#             'name',
#             'price',
#         ]


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = 'products'

    id = fields.KeywordField(attr='id')
    name = fields.TextField(attr='name')
    description = fields.TextField(attr='description')
    price = fields.FloatField(attr='price')
    user_id = fields.KeywordField(attr='user_id')
    # Assuming category_id is the ID of the category
    category = fields.KeywordField(attr='category_id')
    created_at = fields.DateField(attr='created_at')
    updated_at = fields.DateField(attr='updated_at')

    class Django:
        model = Product


@registry.register_document
class CategoryDocument(Document):
    class Index:
        name = 'categories'

    id = fields.KeywordField(attr='id')
    name = fields.TextField(attr='name')
    description = fields.TextField(attr='description')
    # Assuming parent_id is the ID of the parent category
    parent = fields.KeywordField(attr='parent_id')
    created_at = fields.DateField(attr='created_at')
    updated_at = fields.DateField(attr='updated_at')

    class Django:
        model = Category
