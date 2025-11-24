from django.db import models
from django.utils import timezone


class UploadedFile(models.Model):
    """
    نموذج لتخزين معلومات الملفات المرفوعة
    """
    # اسم الملف الأصلي
    original_filename = models.CharField(max_length=255, verbose_name="اسم الملف الأصلي")
    
    # مسار الملف في Supabase Storage
    storage_path = models.CharField(max_length=500, verbose_name="مسار التخزين")
    
    # رابط الوصول العام للملف
    public_url = models.URLField(max_length=1000, verbose_name="الرابط العام")
    
    # حجم الملف بالبايت
    file_size = models.BigIntegerField(verbose_name="حجم الملف")
    
    # نوع الملف (MIME type)
    content_type = models.CharField(max_length=100, verbose_name="نوع الملف")
    
    # تاريخ الرفع
    uploaded_at = models.DateTimeField(default=timezone.now, verbose_name="تاريخ الرفع")
    
    # وصف اختياري
    description = models.TextField(blank=True, null=True, verbose_name="الوصف")
    
    class Meta:
        verbose_name = "ملف مرفوع"
        verbose_name_plural = "ملفات مرفوعة"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.original_filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_file_size_display(self):
        """
        عرض حجم الملف بشكل قابل للقراءة
        """
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{size:.2f} TB"
