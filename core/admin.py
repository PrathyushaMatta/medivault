from django.contrib import admin
from .models import User, MedicalFile

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'masked_aadhaar')
    search_fields = ('name', 'phone_number')
    exclude = ('aadhaar_number',)

@admin.register(MedicalFile)
class MedicalFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'file_name_text', 'uploaded_at')
    list_filter = ('category', 'uploaded_at')
    search_fields = ('file_name', 'user__name')
    readonly_fields = ('uploaded_at','file_name')


    def file_name_text(self, obj):
        return obj.file_name  # just show file name as text
    file_name_text.short_description = "File Name"
