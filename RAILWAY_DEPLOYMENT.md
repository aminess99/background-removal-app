# نشر التطبيق على Railway

## الملفات المطلوبة للنشر

تم إنشاء الملفات التالية لضمان نشر ناجح على Railway:

### 1. nixpacks.toml
```toml
# nixpacks.toml

[start]
cmd = "gunicorn app:app"
```

### 2. railway.json
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "gunicorn app:app",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## خطوات النشر على Railway

### الطريقة الأولى: النشر من GitHub

1. **رفع الكود إلى GitHub:**
   ```bash
   git add .
   git commit -m "Add Railway deployment configuration"
   git push origin main
   ```

2. **إنشاء مشروع جديد على Railway:**
   - اذهب إلى [Railway.app](https://railway.app)
   - سجل دخول باستخدام GitHub
   - انقر على "New Project"
   - اختر "Deploy from GitHub repo"
   - اختر المستودع الخاص بك

3. **تكوين النشر:**
   - Railway سيكتشف تلقائياً أنه تطبيق Python
   - سيستخدم ملفات التكوين التي أنشأناها
   - انتظر حتى اكتمال النشر

4. **إنشاء رابط عام:**
   - اذهب إلى إعدادات المشروع
   - انقر على "Networking"
   - انقر على "Generate Domain"

### الطريقة الثانية: استخدام Railway CLI

1. **تثبيت Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **تسجيل الدخول:**
   ```bash
   railway login
   ```

3. **إنشاء مشروع:**
   ```bash
   railway init
   ```

4. **نشر التطبيق:**
   ```bash
   railway up
   ```

## المتغيرات البيئية المطلوبة

لا توجد متغيرات بيئية إضافية مطلوبة للتطبيق الأساسي.

## ملاحظات مهمة

- تم تعديل `app.py` لإيقاف وضع التطوير (`debug=False`)
- Railway سيستخدم `gunicorn` كخادم الإنتاج
- التطبيق سيعمل على المنفذ الذي يحدده Railway تلقائياً
- جميع التبعيات موجودة في `requirements.txt`

## استكشاف الأخطاء

إذا واجهت مشاكل في النشر:

1. تحقق من سجلات النشر في لوحة تحكم Railway
2. تأكد من أن جميع التبعيات موجودة في `requirements.txt`
3. تحقق من أن `gunicorn` مثبت في `requirements.txt`
4. تأكد من أن ملف `nixpacks.toml` في المجلد الجذر

## الدعم

للمزيد من المساعدة، راجع:
- [وثائق Railway](https://docs.railway.com/)
- [دليل نشر Flask على Railway](https://docs.railway.com/guides/flask)