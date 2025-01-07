from .models import Product,Combo
from modeltranslation.translator import TranslationOptions,register

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')


@register(Combo)
class ComboTranslationOptions(TranslationOptions):
    fields = ('product_name', 'description')