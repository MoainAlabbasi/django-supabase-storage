# 🚀 دليل النشر على Railway

هذا الدليل يشرح خطوات نشر المشروع على Railway بالتفصيل.

## 📋 المتطلبات

- حساب GitHub (تم ✅)
- حساب Supabase (تم ✅)
- حساب Railway ([اشترك مجاناً](https://railway.app/))

## 🔧 خطوات النشر

### 1️⃣ إنشاء مشروع على Railway

1. اذهب إلى [Railway](https://railway.app/)
2. سجل الدخول باستخدام حساب GitHub
3. اضغط على **"New Project"**
4. اختر **"Deploy from GitHub repo"**
5. ابحث عن المستودع: `django-supabase-storage`
6. اضغط على **"Deploy Now"**

### 2️⃣ إضافة متغيرات البيئة

بعد إنشاء المشروع، اذهب إلى **Settings** → **Variables** وأضف المتغيرات التالية:

#### متغيرات Supabase

```
SUPABASE_URL=https://keafcuebminlcmfzuokm.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtlYWZjdWVibWlubGNtZnp1b2ttIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM5NDYxODEsImV4cCI6MjA3OTUyMjE4MX0.-_A7D7dAhNQ89zoQrH2MG1zJGWTGdP0MOlrk6rWhcQM
```

#### متغيرات قاعدة البيانات

```
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=Ab8877@mo
DB_HOST=db.keafcuebminlcmfzuokm.supabase.co
DB_PORT=5432
```

#### متغيرات Django

```
SECRET_KEY=django-production-secret-key-change-this-123456789
DEBUG=False
ALLOWED_HOSTS=.railway.app
```

#### متغيرات التخزين

```
STORAGE_BUCKET=uploads
```

### 3️⃣ تطبيق Migrations

بعد نشر المشروع، افتح **Terminal** في Railway وقم بتشغيل:

```bash
python manage.py migrate
```

### 4️⃣ إنشاء حساب مدير (اختياري)

لإنشاء حساب للوصول إلى لوحة الإدارة:

```bash
python manage.py createsuperuser
```

### 5️⃣ الوصول إلى التطبيق

بعد اكتمال النشر، ستحصل على رابط مثل:

```
https://django-supabase-storage-production.up.railway.app
```

## 🔒 ملاحظات الأمان

### ⚠️ مهم جداً

1. **غيّر SECRET_KEY**: استخدم مفتاح سري قوي وفريد في الإنتاج
   
   يمكنك توليد مفتاح جديد باستخدام:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

2. **DEBUG=False**: تأكد من تعطيل وضع التطوير في الإنتاج

3. **ALLOWED_HOSTS**: أضف نطاقك الخاص إذا كنت تستخدم نطاق مخصص

4. **كلمة مرور قاعدة البيانات**: غيّر كلمة المرور الافتراضية في Supabase

## 🧪 اختبار التطبيق

بعد النشر، جرّب:

1. **الصفحة الرئيسية**: افتح الرابط الرئيسي
2. **رفع ملف**: اذهب إلى `/upload/` وارفع ملف تجريبي
3. **API**: جرّب `GET /api/files/` للحصول على قائمة الملفات
4. **لوحة الإدارة**: اذهب إلى `/admin/` وسجل الدخول

## 🔄 التحديثات التلقائية

Railway سيقوم بنشر التحديثات تلقائياً عند كل push إلى GitHub:

```bash
git add .
git commit -m "تحديث المشروع"
git push origin master
```

## 📊 مراقبة الأداء

في لوحة تحكم Railway يمكنك:

- مراقبة استخدام الموارد
- عرض السجلات (Logs)
- إعادة تشغيل التطبيق
- تغيير متغيرات البيئة

## 🆘 حل المشاكل الشائعة

### المشكلة: "Application Error"

**الحل**: تحقق من السجلات في Railway وتأكد من:
- جميع متغيرات البيئة مضافة بشكل صحيح
- تم تشغيل `python manage.py migrate`
- لا توجد أخطاء في الكود

### المشكلة: "Database connection error"

**الحل**: تحقق من:
- بيانات الاتصال بقاعدة البيانات صحيحة
- Supabase Database يعمل بشكل صحيح
- IP الخاص بـ Railway مسموح في Supabase (عادة غير مطلوب)

### المشكلة: "Static files not loading"

**الحل**: تأكد من:
- `whitenoise` مثبت في `requirements.txt`
- `STATIC_ROOT` محدد في `settings.py`
- تم تشغيل `python manage.py collectstatic`

## 📞 الدعم

إذا واجهت أي مشاكل:

1. تحقق من [وثائق Railway](https://docs.railway.app/)
2. راجع [وثائق Django](https://docs.djangoproject.com/)
3. افتح Issue على [GitHub](https://github.com/MoainAlabbasi/django-supabase-storage/issues)

---

✅ **تم إنشاء هذا الدليل بواسطة Manus AI**
