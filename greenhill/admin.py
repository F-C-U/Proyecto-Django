from django.contrib import admin

# Register your models here.
class AdminPersona(admin.ModelAdmin):
    list_display = []
    search_fields = []
    list_filter = []
    list_per_page = 10