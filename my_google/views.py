from google.cloud import vision
from PIL import Image, ImageEnhance, ImageFilter
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from transformers import pipeline
import pytesseract
from PIL import Image
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from urllib.parse import quote
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import io
import cv2
import numpy as np
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Shortcut
from .forms import ShortcutForm



# Create your views here.
def google(request):
    
    shortcuts = Shortcut.objects.all()
    if request.method == 'POST':
        form = ShortcutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # اسم الـ URL الخاص بالصفحة
    else:
        form = ShortcutForm()

    return render(request, 'google/google.html',{'shortcuts': shortcuts, 'form': form})
def home_view(request):
    return render(request, 'google/home.html')

@login_required
def gmail_view(request):
    # Example user-specific data
    user_data = {'emails': ['Welcome to Gmail!', 'New login from Chrome']}
    return render(request, 'google/gmail.html', user_data)

@login_required
def images_view(request):
    # Example user-specific data
    user_data = {'images': ['img1.jpg', 'img2.jpg']}
    return render(request, 'google/images.html', user_data)




# ضبط المسار بتاع Tesseract (لو مش مضبوط بالفعل)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # عدل المسار حسب جهازك

@csrf_exempt
def extract_text(request):
    if request.method != 'POST' or 'image' not in request.FILES:
        return JsonResponse({'error': 'Invalid request. Image is missing or wrong method.'}, status=400)

    try:
        image_file = request.FILES['image']
        image = Image.open(image_file).convert('RGB')  # تحويل لضمان التنسيق الصحيح

        # تحسين الصورة: إزالة الضوضاء + تحسين الحدة + تحسين التباين
        image = image.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2)  # زيادة التباين
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2)  # زيادة الحدة

        # تحويل إلى تدرج رمادي ومعالجة ثنائية
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        processed_image = Image.fromarray(thresh)

        # OCR باستخدام الإنجليزية والعربية
        extracted_text = pytesseract.image_to_string(processed_image, lang='eng+ara')
        print("Extracted Text:", extracted_text)

        if not extracted_text.strip():
            return HttpResponseRedirect('/extract/?text=No+text+found')

        encoded_text = base64.urlsafe_b64encode(extracted_text.encode()).decode()
        return HttpResponseRedirect(f'/extract/?text={quote(encoded_text)}')

    except Exception as e:
        print("Error processing image:", str(e))
        return JsonResponse({'error': f'Internal error: {str(e)}'}, status=500)


def extract_page(request):
    encoded_text = request.GET.get('text', '')

    if not encoded_text:
        extracted_text = 'No text extracted.'
    else:
        try:
            extracted_text = base64.urlsafe_b64decode(encoded_text.encode()).decode()
        except Exception as e:
            extracted_text = f'Error decoding text: {str(e)}'

    return render(request, 'google/extract.html', {'extracted_text': extracted_text})


chatbot_pipeline = pipeline("text-generation", model="microsoft/DialoGPT-medium")

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').strip().lower()  # تحويل النص إلى حروف صغيرة
        
        # ردود مخصصة بناءً على الكلمات المفتاحية
        if "hello" in user_message:
            response = "Hello! How can I assist you today?"
        elif "django" in user_message:
            response = "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design."
        elif "python" in user_message:
            response = "Python is a versatile programming language known for its simplicity and readability. It's widely used in web development, data science, automation, and more."
        elif "backend" in user_message:
            response = "Backend development involves server-side logic, databases, and application architecture. It ensures the functionality of web applications."
        elif "frontend" in user_message:
            response = "Frontend development focuses on the user interface and user experience. It includes HTML, CSS, JavaScript, and frameworks like React or Vue.js."
        else:
            # استخدام النموذج اللغوي لتوليد رد
            try:
                generated = chatbot_pipeline(user_message, max_length=50)[0]['generated_text']
                response = generated.replace(user_message, '').strip()  # إزالة المدخل من الرد
            except Exception as e:
                response = f"Sorry, I encountered an error: {str(e)}"
        
        return JsonResponse({'response': response})