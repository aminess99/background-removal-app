# دليل رفع تطبيق إزالة الخلفية على الإنترنت

## المنصات المجانية المتاحة

### 1. Render (الأفضل والأسهل)

**المميزات:**
- استضافة مجانية دائمة
- سهولة في الإعداد
- دعم دومين مخصص
- SSL مجاني

**خطوات النشر:**

1. **إنشاء حساب على Render:**
   - اذهب إلى [render.com](https://render.com)
   - سجل حساب جديد

2. **رفع الكود على GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

3. **ربط المشروع بـ Render:**
   - اختر "New Web Service"
   - اربط حساب GitHub
   - اختر المستودع
   - Render سيكتشف ملف `render.yaml` تلقائياً

4. **إضافة دومين مخصص:**
   - في لوحة تحكم Render، اذهب إلى "Settings"
   - اختر "Custom Domains"
   - أضف الدومين الخاص بك
   - اتبع تعليمات DNS

### 2. Heroku (يتطلب بطاقة ائتمان للتحقق)

**خطوات النشر:**

1. **تثبيت Heroku CLI:**
   - حمل من [devcenter.heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **تسجيل الدخول:**
   ```bash
   heroku login
   ```

3. **إنشاء تطبيق:**
   ```bash
   heroku create your-app-name
   ```

4. **رفع الكود:**
   ```bash
   git init
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

5. **إضافة دومين مخصص:**
   ```bash
   heroku domains:add www.yourdomain.com
   ```

### 3. Vercel (للتطبيقات البسيطة)

**خطوات النشر:**

1. **تثبيت Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **النشر:**
   ```bash
   vercel
   ```

3. **إضافة دومين:**
   - في لوحة تحكم Vercel
   - اذهب إلى "Domains"
   - أضف الدومين الخاص بك

## شراء وإعداد دومين مخصص

### مواقع شراء الدومينات:
- **Namecheap** (الأرخص)
- **GoDaddy** (الأشهر)
- **Cloudflare** (أسعار جيدة + حماية)

### إعداد DNS:

1. **للدومين الفرعي (www):**
   ```
   Type: CNAME
   Name: www
   Value: your-app.onrender.com (أو الرابط من المنصة)
   ```

2. **للدومين الرئيسي:**
   ```
   Type: A
   Name: @
   Value: IP address من المنصة
   ```

## نصائح مهمة:

### الأمان:
- لا تضع مفاتيح API في الكود
- استخدم متغيرات البيئة للمعلومات الحساسة

### الأداء:
- المنصات المجانية قد تكون بطيئة
- التطبيق قد ينام بعد فترة عدم استخدام

### التكلفة:
- **Render:** مجاني تماماً
- **Heroku:** يتطلب بطاقة ائتمان للتحقق
- **Vercel:** مجاني للاستخدام الشخصي

## استكشاف الأخطاء:

### مشاكل شائعة:
1. **خطأ في المكتبات:** تأكد من `requirements.txt`
2. **مشكلة في الذاكرة:** قلل حجم النماذج
3. **بطء في التحميل:** استخدم CDN للملفات الثابتة

### فحص السجلات:
```bash
# Heroku
heroku logs --tail

# Render
# من لوحة التحكم > Logs
```

## الخطوات التالية:

1. اختر المنصة المناسبة
2. اشتر دومين من Namecheap أو GoDaddy
3. اتبع خطوات النشر
4. اربط الدومين
5. اختبر التطبيق

**ملاحظة:** قد تستغرق تغييرات DNS من 15 دقيقة إلى 48 ساعة للانتشار عالمياً.