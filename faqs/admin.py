from django.contrib import admin
import faqs.models

# Register your models here.
# Register your models here.
class QADataAdmin(admin.ModelAdmin):
    list_display = ('qid','question','date')

admin.site.register(faqs.models.QAData,QADataAdmin)