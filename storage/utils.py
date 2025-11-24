"""
وظائف مساعدة للتعامل مع Supabase Storage
"""
import os
import uuid
from datetime import datetime
from django.conf import settings
from supabase import create_client, Client


def get_supabase_client() -> Client:
    """
    إنشاء وإرجاع عميل Supabase
    """
    supabase_url = settings.SUPABASE_URL
    supabase_key = settings.SUPABASE_KEY
    
    if not supabase_url or not supabase_key:
        raise ValueError("يجب تعيين SUPABASE_URL و SUPABASE_KEY في ملف .env")
    
    return create_client(supabase_url, supabase_key)


def generate_unique_filename(original_filename: str) -> str:
    """
    توليد اسم ملف فريد بناءً على الوقت الحالي و UUID
    
    Args:
        original_filename: اسم الملف الأصلي
        
    Returns:
        اسم ملف فريد مع الامتداد الأصلي
    """
    # الحصول على امتداد الملف
    _, ext = os.path.splitext(original_filename)
    
    # توليد اسم فريد
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    return f"{timestamp}_{unique_id}{ext}"


def upload_file_to_supabase(file, original_filename: str) -> dict:
    """
    رفع ملف إلى Supabase Storage
    
    Args:
        file: كائن الملف من Django
        original_filename: اسم الملف الأصلي
        
    Returns:
        قاموس يحتوي على معلومات الملف المرفوع
    """
    try:
        # إنشاء عميل Supabase
        supabase = get_supabase_client()
        
        # توليد اسم ملف فريد
        unique_filename = generate_unique_filename(original_filename)
        
        # قراءة محتوى الملف
        file_content = file.read()
        
        # رفع الملف إلى Supabase Storage
        bucket_name = settings.STORAGE_BUCKET
        storage_path = unique_filename
        
        # رفع الملف
        response = supabase.storage.from_(bucket_name).upload(
            path=storage_path,
            file=file_content,
            file_options={
                "content-type": file.content_type,
                "upsert": "false"
            }
        )
        
        # الحصول على الرابط العام للملف
        public_url = supabase.storage.from_(bucket_name).get_public_url(storage_path)
        
        return {
            'success': True,
            'storage_path': storage_path,
            'public_url': public_url,
            'file_size': len(file_content),
            'content_type': file.content_type,
            'original_filename': original_filename
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def delete_file_from_supabase(storage_path: str) -> dict:
    """
    حذف ملف من Supabase Storage
    
    Args:
        storage_path: مسار الملف في التخزين
        
    Returns:
        قاموس يحتوي على نتيجة العملية
    """
    try:
        # إنشاء عميل Supabase
        supabase = get_supabase_client()
        
        # حذف الملف
        bucket_name = settings.STORAGE_BUCKET
        response = supabase.storage.from_(bucket_name).remove([storage_path])
        
        return {
            'success': True,
            'message': 'تم حذف الملف بنجاح'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def get_file_info_from_supabase(storage_path: str) -> dict:
    """
    الحصول على معلومات ملف من Supabase Storage
    
    Args:
        storage_path: مسار الملف في التخزين
        
    Returns:
        قاموس يحتوي على معلومات الملف
    """
    try:
        # إنشاء عميل Supabase
        supabase = get_supabase_client()
        
        # الحصول على الرابط العام
        bucket_name = settings.STORAGE_BUCKET
        public_url = supabase.storage.from_(bucket_name).get_public_url(storage_path)
        
        return {
            'success': True,
            'public_url': public_url,
            'storage_path': storage_path
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def validate_file(file) -> dict:
    """
    التحقق من صحة الملف المرفوع
    
    Args:
        file: كائن الملف من Django
        
    Returns:
        قاموس يحتوي على نتيجة التحقق
    """
    # التحقق من حجم الملف
    if file.size > settings.MAX_UPLOAD_SIZE:
        max_size_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
        return {
            'valid': False,
            'error': f'حجم الملف يتجاوز الحد المسموح ({max_size_mb} MB)'
        }
    
    # التحقق من نوع الملف
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        return {
            'valid': False,
            'error': 'نوع الملف غير مسموح به'
        }
    
    return {
        'valid': True
    }
