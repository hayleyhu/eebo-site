from django.contrib import admin
from english.models import word, category, item, correction

# Register your models here.
admin.site.register(word)
admin.site.register(category)
admin.site.register(item)
admin.site.register(correction)
