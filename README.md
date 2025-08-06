# تطبيق إزالة الخلفية المتقدم

تطبيق ويب متقدم لإزالة الخلفية من الصور باستخدام الذكاء الاصطناعي مع واجهة مستخدم عربية حديثة.

## 🌟 المميزات

- إزالة خلفية احترافية باستخدام نماذج AI متقدمة
- معالجة متقدمة للحواف لنتائج أكثر نعومة
- إزالة الحدود السوداء والتشويش
- واجهة مستخدم عربية حديثة وسهلة الاستخدام
- دعم تحميل الصور أو اختيار من الصور النموذجية
- معاينة فورية للنتائج
- تحميل الصور المعالجة بجودة عالية
- **جاهز للنشر على الإنترنت مع دومين مخصص**

## 🚀 النشر على الإنترنت

### المنصات المجانية المتاحة:
- **Render** (الأفضل) - استضافة مجانية دائمة
- **Heroku** - يتطلب بطاقة ائتمان للتحقق
- **Vercel** - للتطبيقات البسيطة

### خطوات سريعة للنشر على Render:

1. **رفع الكود على GitHub:**
```bash
git init
git add .
git commit -m "Deploy background removal app"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

2. **النشر على Render:**
   - اذهب إلى [render.com](https://render.com)
   - سجل حساب جديد
   - اختر "New Web Service"
   - اربط حساب GitHub واختر المستودع
   - Render سيكتشف الإعدادات تلقائياً

3. **إضافة دومين مخصص:**
   - في لوحة تحكم Render: Settings > Custom Domains
   - أضف الدومين وأعد إعداد DNS

📖 **للتفاصيل الكاملة:** راجع ملف `DEPLOYMENT_GUIDE.md`

## 💻 التقنيات المستخدمة

- **Backend:** Python Flask
- **AI Model:** rembg مع نماذج متقدمة
- **Image Processing:** OpenCV, Pillow, NumPy
- **Frontend:** HTML5, CSS3, JavaScript
- **UI Framework:** تصميم مخصص مع دعم العربية
- **Deployment:** Gunicorn, Docker-ready

## 🛠️ التثبيت والتشغيل المحلي

### المتطلبات
- Python 3.8 أو أحدث
- pip (مدير حزم Python)

### خطوات التثبيت

1. **استنساخ المشروع:**
```bash
git clone <repository-url>
cd removal
```

2. **إنشاء بيئة افتراضية:**
```bash
python -m venv venv

# على Windows
venv\Scripts\activate

# على macOS/Linux
source venv/bin/activate
```

3. **تثبيت المتطلبات:**
```bash
pip install -r requirements.txt
```

4. **تشغيل التطبيق:**
```bash
python app.py
```

5. **فتح التطبيق:**
افتح المتصفح واذهب إلى `http://localhost:5000`

## 📱 كيفية الاستخدام

1. **تحميل صورة:** اضغط على "اختر ملف" وحدد الصورة المطلوبة
2. **أو اختر صورة نموذجية:** اضغط على إحدى الصور النموذجية
3. **معالجة:** اضغط على "إزالة الخلفية"
4. **تحميل النتيجة:** اضغط على "تحميل الصورة" لحفظ النتيجة

## 🧠 الخوارزمية المتقدمة

يستخدم التطبيق خوارزمية متقدمة تتضمن:

- **نماذج AI متعددة:** للحصول على أفضل النتائج
- **معالجة الحواف:** تطبيق Gaussian blur وfeathering
- **تحسين مضاد التشويش:** لحواف أكثر نعومة
- **إزالة البكسلات المعزولة:** تنظيف الضوضاء
- **معالجة متعددة المراحل:** لنتائج احترافية
- **تنعيم ما بعد الإنتاج:** للمسة الأخيرة

## 📁 هيكل المشروع

```
removal/
├── app.py                    # التطبيق الرئيسي
├── requirements.txt          # متطلبات Python
├── Procfile                  # إعدادات Heroku
├── render.yaml              # إعدادات Render
├── vercel.json              # إعدادات Vercel
├── runtime.txt              # إصدار Python
├── .gitignore               # ملفات Git المتجاهلة
├── DEPLOYMENT_GUIDE.md      # دليل النشر الشامل
├── static/                  # الملفات الثابتة
│   ├── *.svg               # صور نموذجية
│   ├── *.jpg               # صور اختبار
│   └── fabric.min.js       # مكتبة JavaScript
├── templates/               # قوالب HTML
│   ├── index.html          # الصفحة الرئيسية
│   ├── about.html          # صفحة حول
│   ├── contact.html        # صفحة الاتصال
│   ├── privacy.html        # سياسة الخصوصية
│   └── terms.html          # شروط الاستخدام
├── uploads/                 # مجلد الصور المرفوعة
├── outputs/                 # مجلد النتائج
├── test_samples/           # صور اختبار
└── README.md               # هذا الملف
```

## 🌐 ملفات النشر المتضمنة

- **Procfile:** لـ Heroku
- **render.yaml:** لـ Render
- **vercel.json:** لـ Vercel
- **runtime.txt:** تحديد إصدار Python
- **.gitignore:** حماية الملفات الحساسة
- **DEPLOYMENT_GUIDE.md:** دليل شامل للنشر

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:

1. عمل Fork للمشروع
2. إنشاء branch جديد للميزة
3. إجراء التغييرات
4. إرسال Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف LICENSE للتفاصيل.

## 🆘 الدعم

إذا واجهت أي مشاكل أو لديك اقتراحات، يرجى فتح issue في GitHub.

## 🔗 روابط مفيدة

- [دليل النشر الشامل](DEPLOYMENT_GUIDE.md)
- [Render.com](https://render.com) - استضافة مجانية
- [Namecheap](https://namecheap.com) - شراء دومينات
- [Cloudflare](https://cloudflare.com) - DNS وحماية

---

**ملاحظة:** هذا التطبيق يستخدم نماذج الذكاء الاصطناعي التي قد تتطلب اتصال بالإنترنت لأول مرة لتحميل النماذج.

**🎉 التطبيق جاهز للنشر على الإنترنت مع دومين مخصص!**