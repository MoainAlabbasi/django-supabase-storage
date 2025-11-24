# 📡 توثيق API

دليل شامل لاستخدام API الخاص بنظام تخزين الملفات.

## 🌐 Base URL

```
http://localhost:8000  # للتطوير
https://your-app.railway.app  # للإنتاج
```

## 📋 نقاط النهاية (Endpoints)

### 1. قائمة جميع الملفات

احصل على قائمة بجميع الملفات المرفوعة.

**Endpoint:**
```
GET /api/files/
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "files": [
    {
      "id": 1,
      "original_filename": "example.pdf",
      "storage_path": "20241124_143022_a1b2c3d4.pdf",
      "public_url": "https://keafcuebminlcmfzuokm.supabase.co/storage/v1/object/public/uploads/20241124_143022_a1b2c3d4.pdf",
      "file_size": 1048576,
      "file_size_display": "1.00 MB",
      "content_type": "application/pdf",
      "uploaded_at": "2024-11-24T14:30:22.123456Z",
      "description": "ملف PDF تجريبي"
    },
    {
      "id": 2,
      "original_filename": "photo.jpg",
      "storage_path": "20241124_143045_e5f6g7h8.jpg",
      "public_url": "https://keafcuebminlcmfzuokm.supabase.co/storage/v1/object/public/uploads/20241124_143045_e5f6g7h8.jpg",
      "file_size": 2097152,
      "file_size_display": "2.00 MB",
      "content_type": "image/jpeg",
      "uploaded_at": "2024-11-24T14:30:45.789012Z",
      "description": "صورة تجريبية"
    }
  ]
}
```

**مثال باستخدام cURL:**
```bash
curl -X GET http://localhost:8000/api/files/
```

**مثال باستخدام Python:**
```python
import requests

response = requests.get('http://localhost:8000/api/files/')
data = response.json()

print(f"عدد الملفات: {data['count']}")
for file in data['files']:
    print(f"- {file['original_filename']} ({file['file_size_display']})")
```

---

### 2. تفاصيل ملف معين

احصل على تفاصيل ملف محدد بواسطة ID.

**Endpoint:**
```
GET /api/files/{id}/
```

**Parameters:**
- `id` (integer, required): معرّف الملف

**Response (Success):**
```json
{
  "success": true,
  "file": {
    "id": 1,
    "original_filename": "example.pdf",
    "storage_path": "20241124_143022_a1b2c3d4.pdf",
    "public_url": "https://keafcuebminlcmfzuokm.supabase.co/storage/v1/object/public/uploads/20241124_143022_a1b2c3d4.pdf",
    "file_size": 1048576,
    "file_size_display": "1.00 MB",
    "content_type": "application/pdf",
    "uploaded_at": "2024-11-24T14:30:22.123456Z",
    "description": "ملف PDF تجريبي"
  }
}
```

**Response (Error - Not Found):**
```json
{
  "success": false,
  "error": "الملف غير موجود"
}
```

**مثال باستخدام cURL:**
```bash
curl -X GET http://localhost:8000/api/files/1/
```

**مثال باستخدام Python:**
```python
import requests

file_id = 1
response = requests.get(f'http://localhost:8000/api/files/{file_id}/')
data = response.json()

if data['success']:
    file = data['file']
    print(f"الملف: {file['original_filename']}")
    print(f"الرابط: {file['public_url']}")
else:
    print(f"خطأ: {data['error']}")
```

---

### 3. رفع ملف جديد

رفع ملف جديد إلى Supabase Storage.

**Endpoint:**
```
POST /api/upload/
```

**Content-Type:** `multipart/form-data`

**Parameters:**
- `file` (file, required): الملف المراد رفعه
- `description` (string, optional): وصف الملف

**Constraints:**
- الحد الأقصى لحجم الملف: 50 MB
- الأنواع المسموحة:
  - الصور: JPEG, PNG, GIF, WebP
  - المستندات: PDF, Word, Excel
  - النصوص: TXT
  - المضغوطة: ZIP

**Response (Success):**
```json
{
  "success": true,
  "message": "تم رفع الملف بنجاح",
  "file": {
    "id": 3,
    "original_filename": "document.pdf",
    "public_url": "https://keafcuebminlcmfzuokm.supabase.co/storage/v1/object/public/uploads/20241124_150000_i9j0k1l2.pdf",
    "file_size": 524288,
    "content_type": "application/pdf"
  }
}
```

**Response (Error - Invalid File):**
```json
{
  "success": false,
  "error": "حجم الملف يتجاوز الحد المسموح (50 MB)"
}
```

**Response (Error - No File):**
```json
{
  "success": false,
  "error": "لم يتم إرسال أي ملف"
}
```

**مثال باستخدام cURL:**
```bash
curl -X POST http://localhost:8000/api/upload/ \
  -F "file=@/path/to/your/file.pdf" \
  -F "description=وصف الملف"
```

**مثال باستخدام Python:**
```python
import requests

url = 'http://localhost:8000/api/upload/'
files = {'file': open('document.pdf', 'rb')}
data = {'description': 'ملف مهم'}

response = requests.post(url, files=files, data=data)
result = response.json()

if result['success']:
    print(f"تم رفع الملف: {result['file']['original_filename']}")
    print(f"الرابط: {result['file']['public_url']}")
else:
    print(f"خطأ: {result['error']}")
```

**مثال باستخدام JavaScript (Fetch API):**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('description', 'وصف الملف');

fetch('http://localhost:8000/api/upload/', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  if (data.success) {
    console.log('تم رفع الملف:', data.file.public_url);
  } else {
    console.error('خطأ:', data.error);
  }
});
```

---

### 4. حذف ملف

حذف ملف من Supabase Storage وقاعدة البيانات.

**Endpoint:**
```
DELETE /api/files/{id}/delete/
POST /api/files/{id}/delete/  # بديل
```

**Parameters:**
- `id` (integer, required): معرّف الملف

**Response (Success):**
```json
{
  "success": true,
  "message": "تم حذف الملف بنجاح"
}
```

**Response (Error - Not Found):**
```json
{
  "success": false,
  "error": "الملف غير موجود"
}
```

**مثال باستخدام cURL (DELETE):**
```bash
curl -X DELETE http://localhost:8000/api/files/1/delete/
```

**مثال باستخدام cURL (POST):**
```bash
curl -X POST http://localhost:8000/api/files/1/delete/
```

**مثال باستخدام Python:**
```python
import requests

file_id = 1
response = requests.delete(f'http://localhost:8000/api/files/{file_id}/delete/')
result = response.json()

if result['success']:
    print(result['message'])
else:
    print(f"خطأ: {result['error']}")
```

---

## 🔐 الأمان والمصادقة

حالياً، API لا يتطلب مصادقة (Authentication). لإضافة مصادقة في المستقبل:

1. استخدم Django REST Framework مع Token Authentication
2. أو استخدم JWT (JSON Web Tokens)
3. أو استخدم OAuth2

**مثال إضافة Token Authentication:**
```python
# في settings.py
INSTALLED_APPS += ['rest_framework', 'rest_framework.authtoken']

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

---

## 📊 أكواد الحالة (Status Codes)

| الكود | المعنى | الوصف |
|------|--------|-------|
| 200 | OK | الطلب نجح |
| 400 | Bad Request | خطأ في البيانات المرسلة |
| 404 | Not Found | الملف غير موجود |
| 500 | Internal Server Error | خطأ في الخادم |

---

## 🧪 اختبار API

### استخدام Postman

1. افتح Postman
2. أنشئ Collection جديد
3. أضف Requests للنقاط المختلفة
4. اختبر كل endpoint

### استخدام Python Script

```python
import requests

BASE_URL = 'http://localhost:8000'

# 1. رفع ملف
with open('test.pdf', 'rb') as f:
    files = {'file': f}
    data = {'description': 'ملف تجريبي'}
    response = requests.post(f'{BASE_URL}/api/upload/', files=files, data=data)
    upload_result = response.json()
    file_id = upload_result['file']['id']
    print(f"✅ تم رفع الملف: ID={file_id}")

# 2. الحصول على قائمة الملفات
response = requests.get(f'{BASE_URL}/api/files/')
files_list = response.json()
print(f"✅ عدد الملفات: {files_list['count']}")

# 3. الحصول على تفاصيل الملف
response = requests.get(f'{BASE_URL}/api/files/{file_id}/')
file_detail = response.json()
print(f"✅ الملف: {file_detail['file']['original_filename']}")

# 4. حذف الملف
response = requests.delete(f'{BASE_URL}/api/files/{file_id}/delete/')
delete_result = response.json()
print(f"✅ {delete_result['message']}")
```

---

## 💡 نصائح

1. **استخدم HTTPS في الإنتاج** لحماية البيانات المنقولة
2. **تحقق من حجم الملف** قبل الرفع لتجنب الأخطاء
3. **احفظ الروابط العامة** للملفات للوصول السريع
4. **استخدم معالجة الأخطاء** في التطبيقات الخاصة بك

---

✅ **تم إنشاء هذا التوثيق بواسطة Manus AI**
