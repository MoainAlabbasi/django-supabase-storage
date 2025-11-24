"""
Views للتعامل مع رفع واسترجاع الملفات
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
import json

from .models import UploadedFile
from .utils import upload_file_to_supabase, delete_file_from_supabase, validate_file


def index(request):
    """
    الصفحة الرئيسية - عرض جميع الملفات المرفوعة
    """
    files = UploadedFile.objects.all()
    
    # Pagination
    paginator = Paginator(files, 10)  # 10 ملفات في كل صفحة
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'total_files': files.count()
    }
    
    return render(request, 'storage/index.html', context)


def upload_file(request):
    """
    صفحة رفع الملفات
    """
    if request.method == 'POST':
        # التحقق من وجود ملف
        if 'file' not in request.FILES:
            messages.error(request, 'لم يتم اختيار أي ملف')
            return redirect('upload_file')
        
        file = request.FILES['file']
        description = request.POST.get('description', '')
        
        # التحقق من صحة الملف
        validation = validate_file(file)
        if not validation['valid']:
            messages.error(request, validation['error'])
            return redirect('upload_file')
        
        # رفع الملف إلى Supabase
        result = upload_file_to_supabase(file, file.name)
        
        if result['success']:
            # حفظ معلومات الملف في قاعدة البيانات
            uploaded_file = UploadedFile.objects.create(
                original_filename=result['original_filename'],
                storage_path=result['storage_path'],
                public_url=result['public_url'],
                file_size=result['file_size'],
                content_type=result['content_type'],
                description=description
            )
            
            messages.success(request, 'تم رفع الملف بنجاح!')
            return redirect('file_detail', pk=uploaded_file.pk)
        else:
            messages.error(request, f'فشل رفع الملف: {result["error"]}')
            return redirect('upload_file')
    
    return render(request, 'storage/upload.html')


def file_detail(request, pk):
    """
    عرض تفاصيل ملف معين
    """
    file = get_object_or_404(UploadedFile, pk=pk)
    
    context = {
        'file': file
    }
    
    return render(request, 'storage/detail.html', context)


def delete_file(request, pk):
    """
    حذف ملف
    """
    if request.method == 'POST':
        file = get_object_or_404(UploadedFile, pk=pk)
        
        # حذف الملف من Supabase Storage
        result = delete_file_from_supabase(file.storage_path)
        
        if result['success']:
            # حذف السجل من قاعدة البيانات
            file.delete()
            messages.success(request, 'تم حذف الملف بنجاح!')
        else:
            messages.error(request, f'فشل حذف الملف: {result["error"]}')
        
        return redirect('index')
    
    return redirect('index')


# API Endpoints

@csrf_exempt
@require_http_methods(["GET"])
def api_list_files(request):
    """
    API: قائمة جميع الملفات
    """
    files = UploadedFile.objects.all()
    
    data = [{
        'id': file.id,
        'original_filename': file.original_filename,
        'storage_path': file.storage_path,
        'public_url': file.public_url,
        'file_size': file.file_size,
        'file_size_display': file.get_file_size_display(),
        'content_type': file.content_type,
        'uploaded_at': file.uploaded_at.isoformat(),
        'description': file.description
    } for file in files]
    
    return JsonResponse({
        'success': True,
        'count': len(data),
        'files': data
    })


@csrf_exempt
@require_http_methods(["GET"])
def api_file_detail(request, pk):
    """
    API: تفاصيل ملف معين
    """
    try:
        file = UploadedFile.objects.get(pk=pk)
        
        data = {
            'id': file.id,
            'original_filename': file.original_filename,
            'storage_path': file.storage_path,
            'public_url': file.public_url,
            'file_size': file.file_size,
            'file_size_display': file.get_file_size_display(),
            'content_type': file.content_type,
            'uploaded_at': file.uploaded_at.isoformat(),
            'description': file.description
        }
        
        return JsonResponse({
            'success': True,
            'file': data
        })
    except UploadedFile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'الملف غير موجود'
        }, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def api_upload_file(request):
    """
    API: رفع ملف جديد
    """
    try:
        # التحقق من وجود ملف
        if 'file' not in request.FILES:
            return JsonResponse({
                'success': False,
                'error': 'لم يتم إرسال أي ملف'
            }, status=400)
        
        file = request.FILES['file']
        description = request.POST.get('description', '')
        
        # التحقق من صحة الملف
        validation = validate_file(file)
        if not validation['valid']:
            return JsonResponse({
                'success': False,
                'error': validation['error']
            }, status=400)
        
        # رفع الملف إلى Supabase
        result = upload_file_to_supabase(file, file.name)
        
        if result['success']:
            # حفظ معلومات الملف في قاعدة البيانات
            uploaded_file = UploadedFile.objects.create(
                original_filename=result['original_filename'],
                storage_path=result['storage_path'],
                public_url=result['public_url'],
                file_size=result['file_size'],
                content_type=result['content_type'],
                description=description
            )
            
            return JsonResponse({
                'success': True,
                'message': 'تم رفع الملف بنجاح',
                'file': {
                    'id': uploaded_file.id,
                    'original_filename': uploaded_file.original_filename,
                    'public_url': uploaded_file.public_url,
                    'file_size': uploaded_file.file_size,
                    'content_type': uploaded_file.content_type
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result['error']
            }, status=500)
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def api_delete_file(request, pk):
    """
    API: حذف ملف
    """
    try:
        file = UploadedFile.objects.get(pk=pk)
        
        # حذف الملف من Supabase Storage
        result = delete_file_from_supabase(file.storage_path)
        
        if result['success']:
            # حذف السجل من قاعدة البيانات
            file.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'تم حذف الملف بنجاح'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result['error']
            }, status=500)
            
    except UploadedFile.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'الملف غير موجود'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
