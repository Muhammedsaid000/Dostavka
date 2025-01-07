from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin


class ContactsInline(admin.TabularInline):
    model = Contacts
    extra = 1


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    inlines = [ContactsInline]


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Combo)
class ComboAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Review)
admin.site.register(ProductsCart)
admin.site.register(ProductsItem)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(CourierReview)