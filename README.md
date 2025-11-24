# 📁 Simple Storage App

نظام بسيط لتخزين واسترجاع الملفات باستخدام Django و Supabase

## 🚀 المميزات

- **رفع الملفات**: رفع الملفات إلى Supabase Storage
- **تخزين المعلومات**: حفظ معلومات الملفات في قاعدة بيانات PostgreSQL
- **واجهة مستخدم**: واجهة ويب بسيطة وجميلة
- **REST API**: نقاط نهاية API للتكامل مع التطبيقات الأخرى
- **إدارة الملفات**: عرض، تحميل، وحذف الملفات

## 🛠️ التقنيات المستخدمة

- **Backend**: Django 5.2.8
- **Database**: Supabase PostgreSQL
- **Storage**: Supabase Storage
- **Hosting**: Railway
- **Version Control**: GitHub

## 📋 المتطلبات

- Python 3.11+
- حساب Supabase (مجاني)
- حساب Railway (مجاني)
- حساب GitHub

## 🔧 التثبيت والإعداد

### 1. استنساخ المشروع

```bash
git clone https://github.com/YOUR_USERNAME/simple-storage-app.git
cd simple-storage-app
```

### 2. إنشاء بيئة افتراضية

```bash
python -m venv venv
source venv/bin/activate  # على Linux/Mac
# أو
venv\Scripts\activate  # على Windows
```

### 3. تثبيت المكتبات

```bash
pip install -r requirements.txt
```

### 4. إعداد متغيرات البيئة

انسخ ملف `.env.example` إلى `.env` وقم بتعبئة البيانات:

```bash
cp .env.example .env
```

قم بتحرير ملف `.env` وأضف بياناتك:

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key

# Database Configuration
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=your_supabase_db_host
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Storage Bucket
STORAGE_BUCKET=uploads
```

### 5. إنشاء Bucket في Supabase

1. اذهب إلى لوحة تحكم Supabase
2. اختر **Storage** من القائمة
3. اضغط **New Bucket**
4. سمّه: `uploads`
5. فعّل خيار **Public Bucket**

### 6. تطبيق Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. إنشاء حساب مدير

```bash
python manage.py createsuperuser
```

### 8. تشغيل المشروع

```bash
python manage.py runserver
```

افتح المتصفح على: `http://localhost:8000`

## 📡 API Endpoints

### قائمة جميع الملفات
```
GET /api/files/
```

### تفاصيل ملف معين
```
GET /api/files/{id}/
```

### رفع ملف جديد
```
POST /api/upload/
Content-Type: multipart/form-data

Parameters:
- file: الملف المراد رفعه
- description: وصف الملف (اختياري)
```

### حذف ملف
```
DELETE /api/files/{id}/delete/
```

## 🚀 النشر على Railway

### 1. إنشاء مشروع جديد

1. اذهب إلى [Railway](https://railway.app/)
2. اضغط **New Project**
3. اختر **Deploy from GitHub repo**
4. اختر المستودع `simple-storage-app`

### 2. إضافة متغيرات البيئة

في إعدادات المشروع على Railway، أضف المتغيرات التالية:

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_database_password
DB_HOST=your_supabase_db_host
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.railway.app
STORAGE_BUCKET=uploads
```

### 3. النشر

سيتم النشر تلقائياً عند كل push إلى GitHub!

## 📂 هيكل المشروع

```
simple-storage-app/
├── config/                 # إعدادات Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── storage/               # تطبيق التخزين
│   ├── models.py         # نماذج قاعدة البيانات
│   ├── views.py          # Views و API
│   ├── urls.py           # URLs
│   ├── utils.py          # وظائف Supabase
│   └── admin.py          # إدارة Django
├── templates/            # قوالب HTML
│   └── storage/
│       ├── base.html
│       ├── index.html
│       ├── upload.html
│       └── detail.html
├── .env.example          # مثال لمتغيرات البيئة
├── .gitignore
├── requirements.txt      # المكتبات المطلوبة
├── Procfile             # إعدادات Railway
├── runtime.txt          # إصدار Python
└── README.md            # هذا الملف
```

## 🔒 الأمان

- لا تشارك ملف `.env` أبداً
- استخدم `SECRET_KEY` قوي في الإنتاج
- اضبط `DEBUG=False` في الإنتاج
- فعّل HTTPS في الإنتاج
- استخدم Row Level Security في Supabase

## 📝 الترخيص

هذا المشروع مفتوح المصدر ومتاح للاستخدام الحر.

## 👨‍💻 المطور

تم تطوير هذا المشروع كمثال تعليمي لاستخدام Django مع Supabase.

## 🤝 المساهمة

المساهمات مرحب بها! لا تتردد في فتح Issue أو Pull Request.

## 📧 الدعم

إذا واجهت أي مشاكل، يرجى فتح Issue على GitHub.

---

**ملاحظة**: تأكد من إعداد Supabase Storage Bucket بشكل صحيح قبل استخدام التطبيق.
