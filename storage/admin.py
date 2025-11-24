from django.contrib import admin
from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    """
    إدارة الملفات المرفوعة في لوحة تحكم Django
    """
    list_display = ['id', 'original_filename', 'content_type', 'file_size_display', 'uploaded_at']
    list_filter = ['content_type', 'uploaded_at']
    search_fields = ['original_filename', 'description', 'storage_path']
    readonly_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    def file_size_display(self, obj):
        """عرض حجم الملف بشكل قابل للقراءة"""
        return obj.get_file_size_display()
    
    file_size_display.short_description = 'حجم الملف'
