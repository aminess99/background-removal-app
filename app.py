from flask import Flask, render_template, request, send_file, jsonify, send_from_directory, session, redirect, url_for
from rembg import remove
from PIL import Image
import io
import os
import uuid
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this to a random secret key
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'outputs'


# Create directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

# Language translations
TRANSLATIONS = {
    'ar': {
        'title': 'فصل خلفية الصور - أداة مجانية لإزالة الخلفية من الصور',
        'description': 'أداة مجانية وسريعة لفصل وإزالة خلفية الصور باستخدام الذكاء الاصطناعي. قم برفع صورتك واحصل على نتيجة احترافية في ثوانٍ.',
        'keywords': 'فصل خلفية الصور, إزالة الخلفية, تحرير الصور, ذكاء اصطناعي, مجاني, أونلاين, تصميم جرافيك, فوتوشوب بديل, إزالة خلفية مجاني, أداة تحرير صور, AI background removal, صور شفافة, PNG, تجارة إلكترونية, وسائل التواصل الاجتماعي, معالجة الصور, تقطيع الصور, خلفية شفافة, تحرير احترافي, أدوات التصميم, صور المنتجات, التصوير الفوتوغرافي, الإعلانات, المحتوى الرقمي, التسويق الإلكتروني, برنامج تحرير مجاني, أتمتة التحرير, تقنية الذكاء الاصطناعي, معالجة تلقائية',
        'site_name': '🎨 فصل خلفية الصور',
        'main_heading': 'فصل خلفية الصور',
        'subtitle': 'أداة مجانية وسريعة لإزالة خلفية الصور باستخدام الذكاء الاصطناعي',
        'upload_title': 'اسحب وأفلت صورتك هنا أو انقر للاختيار',
        'supported_formats': 'يدعم PNG, JPG, JPEG, GIF, BMP, WEBP (حد أقصى 16 ميجابايت)',
        'nav_home': 'الرئيسية',
        'nav_about': 'حول',
        'nav_contact': 'اتصل بنا',
        'nav_privacy': 'الخصوصية',
        'nav_terms': 'الشروط',
        'how_it_works': 'كيف يعمل',
        'step1_title': 'ارفع صورتك',
        'step1_desc': 'اختر الصورة التي تريد إزالة خلفيتها من جهازك',
        'step2_title': 'معالجة تلقائية',
        'step2_desc': 'سيقوم الذكاء الاصطناعي بإزالة الخلفية تلقائياً',
        'step3_title': 'حمل النتيجة',
        'step3_desc': 'احصل على صورتك بخلفية شفافة بجودة عالية',
        'features_title': 'المميزات',
        'feature1_title': 'سريع ودقيق',
        'feature1_desc': 'إزالة الخلفية في ثوانٍ معدودة بدقة عالية',
        'feature2_title': 'مجاني تماماً',
        'feature2_desc': 'استخدم الأداة مجاناً بدون قيود أو رسوم',
        'feature3_title': 'جودة احترافية',
        'feature3_desc': 'نتائج بجودة احترافية مناسبة لجميع الاستخدامات',
        'download_hd': 'تحميل بجودة عالية',
        'download_sd': 'تحميل بجودة عادية',
        'process_new_image': 'معالجة صورة جديدة',
        'processing': 'جاري المعالجة...',
        'before': 'قبل',
        'after': 'بعد',
        'processing_complete': 'تمت المعالجة بنجاح',
        'result_ready': 'النتيجة جاهزة للتحميل',
        'before_after_comparison': 'مقارنة قبل وبعد',
        'footer_copyright': '© 2025 فصل خلفية الصور. جميع الحقوق محفوظة.',
        
        # About page
        'about_title': '🎨 حول موقع فصل خلفية الصور',
        'about_description': 'تعرف على موقع فصل خلفية الصور وكيفية عمل أداة إزالة الخلفية باستخدام الذكاء الاصطناعي',
        'about_intro': 'مرحباً بك في موقع فصل خلفية الصور، الأداة المجانية والمتطورة لإزالة خلفيات الصور باستخدام أحدث تقنيات الذكاء الاصطناعي. نحن نهدف إلى توفير حل سهل وسريع لجميع احتياجاتك في تحرير الصور.',
        'about_vision_title': '🚀 رؤيتنا',
        'about_vision_desc': 'نسعى لجعل تحرير الصور متاحاً للجميع بطريقة بسيطة ومجانية. نؤمن بأن التكنولوجيا يجب أن تكون في خدمة الإبداع، ولذلك نوفر أدوات متقدمة بواجهة سهلة الاستخدام.',
        'about_features_title': '⭐ مميزات موقعنا',
        'about_how_it_works_desc': 'يستخدم موقعنا تقنيات الذكاء الاصطناعي المتقدمة لتحليل الصور وتحديد الكائنات الرئيسية فيها، ثم يقوم بفصل هذه الكائنات عن الخلفية بدقة عالية. العملية بسيطة:',
        'about_uses_title': '🎨 استخدامات متنوعة',
        'about_uses_desc': 'يمكن استخدام أداتنا في العديد من المجالات:',
        'about_use1': 'تصميم الجرافيك والإعلانات',
        'about_use2': 'التجارة الإلكترونية وعرض المنتجات',
        'about_use3': 'وسائل التواصل الاجتماعي',
        'about_use4': 'التصوير الفوتوغرافي',
        'about_use5': 'المشاريع الشخصية والإبداعية',
        'about_commitment_title': '🌟 التزامنا',
        'about_commitment_desc': 'نحن ملتزمون بتوفير خدمة عالية الجودة وتحسين أدواتنا باستمرار. فريقنا يعمل على تطوير تقنيات جديدة لضمان أفضل تجربة ممكنة لمستخدمينا.',
        'try_now': 'جرب الأداة الآن',
        'back_to_home': 'العودة للرئيسية',
        'footer_description': 'أداة مجانية ومتطورة لإزالة خلفيات الصور باستخدام الذكاء الاصطناعي',
        'footer_quick_links': 'روابط سريعة',
        'footer_legal': 'قانوني',
        
        # JavaScript messages
        'js_select_file': 'يرجى اختيار ملف أولاً',
        'js_supported_formats': 'الصيغ المدعومة: PNG, JPG, JPEG, GIF, BMP, WEBP',
        'js_file_too_large': 'حجم الملف كبير جداً. الحد الأقصى 16 ميجابايت',
        'js_invalid_file': 'نوع الملف غير مدعوم. يرجى اختيار صورة صالحة',
        'js_upload_error': 'حدث خطأ أثناء رفع الملف. يرجى المحاولة مرة أخرى',
        'js_processing_error': 'حدث خطأ أثناء معالجة الصورة. يرجى المحاولة مرة أخرى'
     },
     'en': {
        'title': 'Background Remover - Free AI-Powered Background Removal Tool',
        'description': 'Free and fast background removal tool using artificial intelligence. Upload your image and get professional results in seconds.',
        'keywords': 'background removal, remove background, photo editing, AI, free, online, graphic design, photoshop alternative, free background remover, image editing tool, transparent images, PNG, ecommerce, social media, artificial intelligence, automatic background removal, image processing, photo cutout, transparent background, professional editing, design tools, product photography, digital marketing, content creation, online editor, AI-powered, machine learning, automated editing, image manipulation, photo retouching, visual content, branding, web design, digital assets, creative tools, batch processing, high quality, instant results',
        'site_name': '🎨 Background Remover',
        'main_heading': 'Background Remover',
        'subtitle': 'Free and fast background removal tool using artificial intelligence',
        'upload_text': 'Drag and drop your image here or click to select',
        'upload_subtext': 'Supports PNG, JPG, JPEG, GIF, BMP, WEBP (max 16MB)',
        'nav_home': 'Home',
        'nav_about': 'About',
        'nav_contact': 'Contact',
        'nav_privacy': 'Privacy',
        'nav_terms': 'Terms',
        'how_it_works': 'How It Works',
        'step1_title': 'Upload Your Image',
        'step1_desc': 'Choose the image you want to remove background from your device',
        'step2_title': 'Automatic Processing',
        'step2_desc': 'AI will automatically remove the background',
        'step3_title': 'Download Result',
        'step3_desc': 'Get your image with transparent background in high quality',
        'features_title': 'Features',
        'feature1_title': 'Fast & Accurate',
        'feature1_desc': 'Remove background in seconds with high accuracy',
        'feature2_title': 'Completely Free',
        'feature2_desc': 'Use the tool for free without limitations or fees',
        'feature3_title': 'Professional Quality',
        'feature3_desc': 'Professional quality results suitable for all uses',
        'download_hd': 'Download HD Quality',
        'download_sd': 'Download SD Quality',
        'process_new_image': 'Process New Image',
        'processing': 'Processing...',
        'before': 'Before',
        'after': 'After',
        'processing_complete': 'Processing Complete',
        'result_ready': 'Your result is ready for download',
        'before_after_comparison': 'Before & After Comparison',
        'footer_copyright': '© 2025 Background Remover. All rights reserved.',
        
        # About page
        'about_title': '🎨 About Background Remover',
        'about_description': 'Learn about our background removal tool and how our AI-powered background removal works',
        'about_intro': 'Welcome to Background Remover, the free and advanced tool for removing image backgrounds using the latest artificial intelligence technologies. We aim to provide an easy and fast solution for all your image editing needs.',
        'about_vision_title': '🚀 Our Vision',
        'about_vision_desc': 'We strive to make image editing accessible to everyone in a simple and free way. We believe that technology should serve creativity, so we provide advanced tools with an easy-to-use interface.',
        'about_features_title': '⭐ Our Features',
        'about_how_it_works_desc': 'Our website uses advanced artificial intelligence techniques to analyze images and identify the main objects in them, then separates these objects from the background with high accuracy. The process is simple:',
        'about_uses_title': '🎨 Various Uses',
        'about_uses_desc': 'Our tool can be used in many fields:',
        'about_use1': 'Graphic design and advertising',
        'about_use2': 'E-commerce and product display',
        'about_use3': 'Social media',
        'about_use4': 'Photography',
        'about_use5': 'Personal and creative projects',
        'about_commitment_title': '🌟 Our Commitment',
        'about_commitment_desc': 'We are committed to providing high-quality service and continuously improving our tools. Our team works on developing new technologies to ensure the best possible experience for our users.',
        'try_now': 'Try Now',
        'back_to_home': 'Back to Home',
        'footer_description': 'Free and advanced tool for removing image backgrounds using artificial intelligence',
        'footer_quick_links': 'Quick Links',
        'footer_legal': 'Legal',
        
        # JavaScript messages
        'js_select_file': 'Please select a file first',
        'js_supported_formats': 'Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP',
        'js_file_too_large': 'File is too large. Maximum size is 16MB',
        'js_invalid_file': 'Invalid file type. Please select a valid image',
        'js_upload_error': 'Error uploading file. Please try again',
        'js_processing_error': 'Error processing image. Please try again'
    },
    'fr': {
        'title': 'Suppresseur d\'Arrière-plan - Outil Gratuit de Suppression d\'Arrière-plan IA',
        'description': 'Outil gratuit et rapide de suppression d\'arrière-plan utilisant l\'intelligence artificielle. Téléchargez votre image et obtenez des résultats professionnels en secondes.',
        'keywords': 'suppression arrière-plan, supprimer arrière-plan, édition photo, IA, gratuit, en ligne, design graphique, alternative photoshop, suppresseur arrière-plan gratuit, outil édition image, images transparentes, PNG, commerce électronique, réseaux sociaux, intelligence artificielle, traitement image, découpage photo, fond transparent, édition professionnelle, outils design, photographie produit, marketing numérique, création contenu, éditeur en ligne, automatisation, apprentissage automatique, retouche photo, contenu visuel, marque, conception web, actifs numériques, outils créatifs, traitement par lots, haute qualité, résultats instantanés',
        'site_name': '🎨 Suppresseur d\'Arrière-plan',
        'main_heading': 'Suppresseur d\'Arrière-plan',
        'subtitle': 'Outil gratuit et rapide de suppression d\'arrière-plan utilisant l\'intelligence artificielle',
        'upload_text': 'Glissez et déposez votre image ici ou cliquez pour sélectionner',
        'upload_subtext': 'Supporte PNG, JPG, JPEG, GIF, BMP, WEBP (max 16MB)',
        'nav_home': 'Accueil',
        'nav_about': 'À propos',
        'nav_contact': 'Contact',
        'nav_privacy': 'Confidentialité',
        'nav_terms': 'Conditions',
        'how_it_works': 'Comment ça marche',
        'step1_title': 'Téléchargez votre image',
        'step1_desc': 'Choisissez l\'image dont vous voulez supprimer l\'arrière-plan',
        'step2_title': 'Traitement automatique',
        'step2_desc': 'L\'IA supprimera automatiquement l\'arrière-plan',
        'step3_title': 'Téléchargez le résultat',
        'step3_desc': 'Obtenez votre image avec un arrière-plan transparent en haute qualité',
        'features_title': 'Fonctionnalités',
        'feature1_title': 'Rapide et précis',
        'feature1_desc': 'Supprimez l\'arrière-plan en secondes avec une grande précision',
        'feature2_title': 'Complètement gratuit',
        'feature2_desc': 'Utilisez l\'outil gratuitement sans limitations ni frais',
        'feature3_title': 'Qualité professionnelle',
        'feature3_desc': 'Résultats de qualité professionnelle adaptés à tous les usages',
        'download_hd': 'Télécharger en HD',
        'download_sd': 'Télécharger en SD',
        'process_new_image': 'Traiter une nouvelle image',
        'processing': 'Traitement en cours...',
        'before': 'Avant',
        'after': 'Après',
        'processing_complete': 'Traitement terminé',
        'result_ready': 'Votre résultat est prêt à télécharger',
        'before_after_comparison': 'Comparaison Avant & Après',
        'footer_copyright': '© 2025 Suppresseur d\'arrière-plan. Tous droits réservés.',
        
        # About page
        'about_title': '🎨 À propos du Suppresseur d\'arrière-plan',
        'about_description': 'Découvrez notre outil de suppression d\'arrière-plan et comment fonctionne notre suppression d\'arrière-plan alimentée par l\'IA',
        'about_intro': 'Bienvenue sur Suppresseur d\'arrière-plan, l\'outil gratuit et avancé pour supprimer les arrière-plans d\'images en utilisant les dernières technologies d\'intelligence artificielle. Nous visons à fournir une solution facile et rapide pour tous vos besoins d\'édition d\'images.',
        'about_vision_title': '🚀 Notre Vision',
        'about_vision_desc': 'Nous nous efforçons de rendre l\'édition d\'images accessible à tous de manière simple et gratuite. Nous croyons que la technologie doit servir la créativité, c\'est pourquoi nous fournissons des outils avancés avec une interface facile à utiliser.',
        'about_features_title': '⭐ Nos Fonctionnalités',
        'about_how_it_works_desc': 'Notre site web utilise des techniques d\'intelligence artificielle avancées pour analyser les images et identifier les objets principaux qu\'elles contiennent, puis sépare ces objets de l\'arrière-plan avec une grande précision. Le processus est simple :',
        'about_uses_title': '🎨 Utilisations Diverses',
        'about_uses_desc': 'Notre outil peut être utilisé dans de nombreux domaines :',
        'about_use1': 'Design graphique et publicité',
        'about_use2': 'E-commerce et présentation de produits',
        'about_use3': 'Réseaux sociaux',
        'about_use4': 'Photographie',
        'about_use5': 'Projets personnels et créatifs',
        'about_commitment_title': '🌟 Notre Engagement',
        'about_commitment_desc': 'Nous nous engageons à fournir un service de haute qualité et à améliorer continuellement nos outils. Notre équipe travaille sur le développement de nouvelles technologies pour garantir la meilleure expérience possible à nos utilisateurs.',
        'try_now': 'Essayer Maintenant',
        'back_to_home': 'Retour à l\'Accueil',
        'footer_description': 'Outil gratuit et avancé pour supprimer les arrière-plans d\'images en utilisant l\'intelligence artificielle',
        'footer_quick_links': 'Liens Rapides',
        'footer_legal': 'Légal',
        
        # JavaScript messages
        'js_select_file': 'Veuillez d\'abord sélectionner un fichier',
        'js_supported_formats': 'Formats supportés: PNG, JPG, JPEG, GIF, BMP, WEBP',
        'js_file_too_large': 'Le fichier est trop volumineux. Taille maximale 16MB',
        'js_invalid_file': 'Type de fichier invalide. Veuillez sélectionner une image valide',
        'js_upload_error': 'Erreur lors du téléchargement. Veuillez réessayer',
        'js_processing_error': 'Erreur lors du traitement de l\'image. Veuillez réessayer'
    },
    'es': {
        'title': 'Removedor de Fondo - Herramienta Gratuita de Eliminación de Fondo con IA',
        'description': 'Herramienta gratuita y rápida para eliminar fondos usando inteligencia artificial. Sube tu imagen y obtén resultados profesionales en segundos.',
        'keywords': 'eliminar fondo, quitar fondo, edición de fotos, IA, gratis, en línea, diseño gráfico, alternativa photoshop, removedor fondo gratis, herramienta edición imagen, imágenes transparentes, PNG, comercio electrónico, redes sociales, inteligencia artificial, procesamiento imagen, recorte foto, fondo transparente, edición profesional, herramientas diseño, fotografía producto, marketing digital, creación contenido, editor online, automatización, aprendizaje automático, retoque fotográfico, contenido visual, marca, diseño web, activos digitales, herramientas creativas, procesamiento lotes, alta calidad, resultados instantáneos',
        'site_name': '🎨 Removedor de Fondo',
        'main_heading': 'Removedor de Fondo',
        'subtitle': 'Herramienta gratuita y rápida para eliminar fondos usando inteligencia artificial',
        'upload_text': 'Arrastra y suelta tu imagen aquí o haz clic para seleccionar',
        'upload_subtext': 'Soporta PNG, JPG, JPEG, GIF, BMP, WEBP (máx 16MB)',
        'nav_home': 'Inicio',
        'nav_about': 'Acerca de',
        'nav_contact': 'Contacto',
        'nav_privacy': 'Privacidad',
        'nav_terms': 'Términos',
        'how_it_works': 'Cómo funciona',
        'step1_title': 'Sube tu imagen',
        'step1_desc': 'Elige la imagen de la que quieres eliminar el fondo',
        'step2_title': 'Procesamiento automático',
        'step2_desc': 'La IA eliminará automáticamente el fondo',
        'step3_title': 'Descarga el resultado',
        'step3_desc': 'Obtén tu imagen con fondo transparente en alta calidad',
        'features_title': 'Características',
        'feature1_title': 'Rápido y preciso',
        'feature1_desc': 'Elimina el fondo en segundos con alta precisión',
        'feature2_title': 'Completamente gratis',
        'feature2_desc': 'Usa la herramienta gratis sin limitaciones ni tarifas',
        'feature3_title': 'Calidad profesional',
        'feature3_desc': 'Resultados de calidad profesional adecuados para todos los usos',
        'download_hd': 'Descargar en HD',
        'download_sd': 'Descargar en SD',
        'process_new_image': 'Procesar nueva imagen',
        'processing': 'Procesando...',
        'before': 'Antes',
        'after': 'Después',
        'processing_complete': 'Procesamiento completado',
        'result_ready': 'Tu resultado está listo para descargar',
        'before_after_comparison': 'Comparación Antes y Después',
        'footer_copyright': '© 2025 Eliminador de Fondo. Todos los derechos reservados.',
        
        # About page
        'about_title': '🎨 Acerca del Eliminador de Fondo',
        'about_description': 'Conoce nuestra herramienta de eliminación de fondos y cómo funciona nuestra eliminación de fondos impulsada por IA',
        'about_intro': 'Bienvenido a Eliminador de Fondo, la herramienta gratuita y avanzada para eliminar fondos de imágenes utilizando las últimas tecnologías de inteligencia artificial. Nuestro objetivo es proporcionar una solución fácil y rápida para todas tus necesidades de edición de imágenes.',
        'about_vision_title': '🚀 Nuestra Visión',
        'about_vision_desc': 'Nos esforzamos por hacer que la edición de imágenes sea accesible para todos de manera simple y gratuita. Creemos que la tecnología debe servir a la creatividad, por eso proporcionamos herramientas avanzadas con una interfaz fácil de usar.',
        'about_features_title': '⭐ Nuestras Características',
        'about_how_it_works_desc': 'Nuestro sitio web utiliza técnicas avanzadas de inteligencia artificial para analizar imágenes e identificar los objetos principales en ellas, luego separa estos objetos del fondo con alta precisión. El proceso es simple:',
        'about_uses_title': '🎨 Usos Diversos',
        'about_uses_desc': 'Nuestra herramienta puede ser utilizada en muchos campos:',
        'about_use1': 'Diseño gráfico y publicidad',
        'about_use2': 'Comercio electrónico y presentación de productos',
        'about_use3': 'Redes sociales',
        'about_use4': 'Fotografía',
        'about_use5': 'Proyectos personales y creativos',
        'about_commitment_title': '🌟 Nuestro Compromiso',
        'about_commitment_desc': 'Estamos comprometidos a brindar un servicio de alta calidad y mejorar continuamente nuestras herramientas. Nuestro equipo trabaja en el desarrollo de nuevas tecnologías para garantizar la mejor experiencia posible para nuestros usuarios.',
        'try_now': 'Probar Ahora',
        'back_to_home': 'Volver al Inicio',
        'footer_description': 'Herramienta gratuita y avanzada para eliminar fondos de imágenes usando inteligencia artificial',
        'footer_quick_links': 'Enlaces Rápidos',
        'footer_legal': 'Legal',
        
        # JavaScript messages
        'js_select_file': 'Por favor selecciona un archivo primero',
        'js_supported_formats': 'Formatos soportados: PNG, JPG, JPEG, GIF, BMP, WEBP',
        'js_file_too_large': 'El archivo es demasiado grande. Tamaño máximo 16MB',
        'js_invalid_file': 'Tipo de archivo inválido. Por favor selecciona una imagen válida',
        'js_upload_error': 'Error al subir el archivo. Por favor intenta de nuevo',
        'js_processing_error': 'Error al procesar la imagen. Por favor intenta de nuevo'
    }
}

# Default language
DEFAULT_LANGUAGE = 'en'

def get_language():
    return session.get('language', DEFAULT_LANGUAGE)

def get_text(key):
    lang = get_language()
    return TRANSLATIONS.get(lang, TRANSLATIONS[DEFAULT_LANGUAGE]).get(key, key)

def get_direction():
    lang = get_language()
    return 'rtl' if lang == 'ar' else 'ltr'



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/set_language/<language>')
def set_language(language):
    if language in TRANSLATIONS:
        session['language'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/')
def index():
    lang = get_language()
    translations = TRANSLATIONS[lang]
    return render_template('index.html', 
                         translations=translations, 
                         current_lang=lang, 
                         direction=get_direction())

@app.route('/about')
def about():
    lang = get_language()
    translations = TRANSLATIONS[lang]
    return render_template('about.html', 
                         translations=translations, 
                         current_lang=lang, 
                         direction=get_direction())

@app.route('/contact')
def contact():
    lang = get_language()
    translations = TRANSLATIONS[lang]
    return render_template('contact.html', 
                         translations=translations, 
                         current_lang=lang, 
                         direction=get_direction())

@app.route('/privacy')
def privacy():
    lang = get_language()
    translations = TRANSLATIONS[lang]
    return render_template('privacy.html', 
                         translations=translations, 
                         current_lang=lang, 
                         direction=get_direction())

@app.route('/terms')
def terms():
    lang = get_language()
    translations = TRANSLATIONS[lang]
    return render_template('terms.html', 
                         translations=translations, 
                         current_lang=lang, 
                         direction=get_direction())

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'لم يتم اختيار ملف'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'لم يتم اختيار ملف'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'نوع الملف غير مدعوم. يرجى استخدام PNG, JPG, JPEG, GIF, BMP, أو WEBP'}), 400
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        input_filename = f"{unique_id}_input.{file_extension}"
        output_filename = f"{unique_id}_output.png"
        
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_filename)
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Save uploaded file
        file.save(input_path)
        
        # Remove background
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
            output_data = remove(input_data)
        
        # Post-process the image to reduce artifacts
        output_image = Image.open(io.BytesIO(output_data))
        
        # Convert to RGBA if not already
        if output_image.mode != 'RGBA':
            output_image = output_image.convert('RGBA')
        
        # Advanced edge processing to eliminate black borders
        pixels = output_image.load()
        width, height = output_image.size
        
        # First pass: Clean up obvious artifacts
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                
                # If alpha is very low, make it fully transparent
                if a < 15:
                    pixels[x, y] = (0, 0, 0, 0)
                # If alpha is very high, make it fully opaque
                elif a > 240:
                    pixels[x, y] = (r, g, b, 255)
                # For semi-transparent pixels, preserve them for smoother edges
                elif a < 50:
                    # Gradually fade out very low alpha pixels
                    new_alpha = max(0, a - 20)
                    pixels[x, y] = (r, g, b, new_alpha)
        
        # Apply edge smoothing with multiple blur passes
        from PIL import ImageFilter
        
        # Separate RGB and Alpha channels
        r_channel, g_channel, b_channel, alpha_channel = output_image.split()
        
        # Apply gentle blur to alpha channel for smoother edges
        smoothed_alpha = alpha_channel.filter(ImageFilter.GaussianBlur(radius=0.8))
        
        # Apply very light blur to RGB channels to reduce color artifacts
        smoothed_r = r_channel.filter(ImageFilter.GaussianBlur(radius=0.3))
        smoothed_g = g_channel.filter(ImageFilter.GaussianBlur(radius=0.3))
        smoothed_b = b_channel.filter(ImageFilter.GaussianBlur(radius=0.3))
        
        # Recombine channels
        output_image = Image.merge('RGBA', (smoothed_r, smoothed_g, smoothed_b, smoothed_alpha))
        
        # Second pass: Edge refinement to prevent black borders
        pixels = output_image.load()
        for y in range(1, height-1):
            for x in range(1, width-1):
                r, g, b, a = pixels[x, y]
                
                if a > 0:  # Only process non-transparent pixels
                    # Check for dark pixels near edges that might be artifacts
                    if r < 50 and g < 50 and b < 50 and a < 200:
                        # Check surrounding pixels
                        surrounding_pixels = [
                            pixels[x-1, y-1], pixels[x, y-1], pixels[x+1, y-1],
                            pixels[x-1, y], pixels[x+1, y],
                            pixels[x-1, y+1], pixels[x, y+1], pixels[x+1, y+1]
                        ]
                        
                        # Count transparent neighbors
                        transparent_neighbors = sum(1 for p in surrounding_pixels if p[3] < 50)
                        
                        # If this dark pixel is near transparent areas, it's likely an artifact
                        if transparent_neighbors >= 3:
                            # Blend with nearby non-dark pixels or make transparent
                            non_dark_neighbors = [p for p in surrounding_pixels if p[3] > 100 and (p[0] > 80 or p[1] > 80 or p[2] > 80)]
                            
                            if non_dark_neighbors:
                                # Average the color of non-dark neighbors
                                avg_r = sum(p[0] for p in non_dark_neighbors) // len(non_dark_neighbors)
                                avg_g = sum(p[1] for p in non_dark_neighbors) // len(non_dark_neighbors)
                                avg_b = sum(p[2] for p in non_dark_neighbors) // len(non_dark_neighbors)
                                pixels[x, y] = (avg_r, avg_g, avg_b, max(50, a))
                            else:
                                # Make it more transparent
                                pixels[x, y] = (r, g, b, max(0, a - 100))
        
        # Final cleanup: remove isolated pixels and artifacts (noise reduction)
        pixels = output_image.load()
        for y in range(1, height-1):
            for x in range(1, width-1):
                r, g, b, a = pixels[x, y]
                
                # Check if this pixel is isolated (surrounded by transparent pixels)
                if a > 0:  # Only check non-transparent pixels
                    surrounding_alpha = [
                        pixels[x-1, y-1][3], pixels[x, y-1][3], pixels[x+1, y-1][3],
                        pixels[x-1, y][3],                      pixels[x+1, y][3],
                        pixels[x-1, y+1][3], pixels[x, y+1][3], pixels[x+1, y+1][3]
                    ]
                    
                    # Count opaque neighbors
                    opaque_neighbors = sum(1 for alpha in surrounding_alpha if alpha > 50)
                    
                    # If this pixel is isolated, remove it
                    if opaque_neighbors < 2:  # Less than 2 opaque neighbors
                        pixels[x, y] = (0, 0, 0, 0)
                    # If this is a dark pixel with few neighbors, it might be an artifact
                    elif opaque_neighbors < 4 and r < 60 and g < 60 and b < 60:
                        # Check if surrounding pixels are much brighter
                        surrounding_pixels = [
                            pixels[x-1, y-1], pixels[x, y-1], pixels[x+1, y-1],
                            pixels[x-1, y], pixels[x+1, y],
                            pixels[x-1, y+1], pixels[x, y+1], pixels[x+1, y+1]
                        ]
                        
                        bright_neighbors = [p for p in surrounding_pixels if p[3] > 100 and (p[0] > 100 or p[1] > 100 or p[2] > 100)]
                        
                        if len(bright_neighbors) >= 2:
                            # This dark pixel is likely an artifact, reduce its opacity significantly
                            pixels[x, y] = (r, g, b, max(0, a - 150))
        
        # Save the processed image
        output_image.save(output_path, 'PNG', optimize=True)
        
        # Clean up input file
        os.remove(input_path)
        
        return jsonify({
            'success': True,
            'output_filename': output_filename,
            'message': 'تم فصل الخلفية بنجاح!'
        })
    
    except Exception as e:
        # Log the error for debugging
        print(f"Error in upload_file: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Clean up input file if it exists
        try:
            if 'input_path' in locals() and os.path.exists(input_path):
                os.remove(input_path)
        except:
            pass
            
        return jsonify({'error': f'حدث خطأ أثناء معالجة الصورة: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=f'removed_bg_{filename}')
        else:
            return jsonify({'error': 'الملف غير موجود'}), 404
    except Exception as e:
        return jsonify({'error': f'حدث خطأ أثناء تحميل الملف: {str(e)}'}), 500

@app.route('/download/<filename>/<quality>')
def download_file_quality(filename, quality):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'الملف غير موجود'}), 404
        
        # Open the original image
        with Image.open(file_path) as img:
            if quality == 'hd':
                # Keep original size for HD
                output_img = img.copy()
                quality_suffix = '_HD'
            elif quality == 'sd':
                # Resize to 50% for SD
                width, height = img.size
                new_size = (width // 2, height // 2)
                output_img = img.resize(new_size, Image.Resampling.LANCZOS)
                quality_suffix = '_SD'
            else:
                return jsonify({'error': 'جودة غير مدعومة'}), 400
            
            # Save to memory
            img_io = io.BytesIO()
            output_img.save(img_io, 'PNG', optimize=True)
            img_io.seek(0)
            
            # Create filename with quality suffix
            base_name = filename.rsplit('.', 1)[0]
            download_name = f'removed_bg_{base_name}{quality_suffix}.png'
            
            return send_file(
                img_io,
                mimetype='image/png',
                as_attachment=True,
                download_name=download_name
            )
    except Exception as e:
        return jsonify({'error': f'حدث خطأ أثناء تحميل الملف: {str(e)}'}), 500

@app.route('/preview/<filename>')
def preview_file(filename):
    try:
        file_path = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({'error': 'الملف غير موجود'}), 404
    except Exception as e:
        return jsonify({'error': f'حدث خطأ أثناء عرض الملف: {str(e)}'}), 500

@app.route('/outputs/<filename>')
def output_file(filename):
    try:
        return send_from_directory(app.config['OUTPUT_FOLDER'], filename)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

@app.route('/sitemap.xml')
def sitemap():
    try:
        return send_from_directory('.', 'sitemap.xml', mimetype='application/xml')
    except FileNotFoundError:
        return jsonify({'error': 'Sitemap not found'}), 404

@app.route('/robots.txt')
def robots():
    try:
        return send_from_directory('.', 'robots.txt', mimetype='text/plain')
    except FileNotFoundError:
        return jsonify({'error': 'Robots.txt not found'}), 404



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)