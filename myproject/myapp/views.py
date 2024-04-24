from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PANCardForm, CreateUserForm
from .models import *
from datetime import datetime
from PIL import Image
import pytesseract
import PyPDF2
import re

# Set Tesseract OCR path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


# Views for User Authentication
def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CreateUserForm()
    return render(request, 'register_page.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.info(request, f'Welcome back, {username}! You are now logged in.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
            return redirect('login')

    return render(request, 'login_page.html')


def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')


# Home Page View
def home(request):
    return render(request, 'home.html')


# Profile Related Views
@login_required
def profile_view(request):
    try:
        profile_data = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile_data = None

    return render(request, 'profile_view.html', {'profile_data': profile_data})


@login_required
def Profile_edit(request):
    return render(request, "profile_edit.html")


# Information Extraction Functions
def extract_information(image):
    text = pytesseract.image_to_string(image)
    dob_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    pan_num_pattern = re.compile(r'Permanent Account Number Card\n.+')
    name_pattern = re.compile(r'Name\n.+')
    father_pattern = re.compile(r"Father's Name\n.+")

    dob_match = re.search(dob_pattern, text)
    pan_match = re.search(pan_num_pattern, text)
    name_match = re.search(name_pattern, text)
    father_match = re.search(father_pattern, text)

    dob = dob_match.group(0) if dob_match else None
    pan = pan_match.group(0).split('\n')[-1].strip() if pan_match else None
    name = name_match.group(0).split('\n')[-1].strip() if name_match else None
    father_name = father_match.group(0).split('\n')[-1].strip() if father_match else None

    return dob, pan, name, father_name


def extract_aadhar_data(aadhar_pdf):
    aadhar_number_regex = r'\b\d{4}\s\d{4}\s\d{4}'
    aadhar_name_regex = r'To\s+(.+)'
    aadhar_dob_regex = r'DOB:\s(\d{2}/\d{2}/\d{4})'
    aadhar_gender_regex = r'(FEMALE|MALE|female|male)'
    aadhar_Phone_regex = r'(\d{10})'
    aadhar_address_regex = r'Address:\s*([\w\s:/\\]+)\n([\w\s:/\\]+)\n([\w\s:/\\]+)\n([\w\s:/\\]+)\s+(?=\b\d{6}\b)'
    pin_regex = r'\b(\d{6})\b'

    aadhar_name = ''
    aadhar_dob = ''
    aadhar_gender = ''
    aadhar_number = ''
    aadhar_Phone = ''
    aadhar_address = ''
    pin = ''

    with open(aadhar_pdf.file.path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        page = pdf_reader.pages[0]
        aadhar_text = page.extract_text()

        clean_text = re.sub(r'[^a-zA-Z0-9\s:/\\]', '', aadhar_text)
        clean_text = '\n'.join(line.strip() for line in clean_text.split('\n') if line.strip())

        aadhar_name_match = re.search(aadhar_name_regex, clean_text)
        if aadhar_name_match:
            aadhar_name = aadhar_name_match.group(1).strip()

        aadhar_dob_match = re.search(aadhar_dob_regex, clean_text)
        if aadhar_dob_match:
            aadhar_dob = aadhar_dob_match.group(1).strip()

        aadhar_gender_match = re.search(aadhar_gender_regex, clean_text)
        if aadhar_gender_match:
            aadhar_gender = aadhar_gender_match.group(1).strip()

        aadhar_number_match = re.search(aadhar_number_regex, clean_text)
        if aadhar_number_match:
            aadhar_number = aadhar_number_match.group(0).strip()

        aadhar_Phone_match = re.search(aadhar_Phone_regex, clean_text)
        if aadhar_Phone_match:
            aadhar_Phone = aadhar_Phone_match.group(1).strip()

        aadhar_address_match = re.search(aadhar_address_regex, clean_text)
        if aadhar_address_match:
            address_parts = aadhar_address_match.groups()
            aadhar_address = ', '.join([part.strip() for part in address_parts[:-1]])

        pin_match = re.search(pin_regex, clean_text)
        if pin_match:
            pin = pin_match.group(0).strip()

    return aadhar_name, aadhar_dob, aadhar_gender, aadhar_number, aadhar_Phone, aadhar_address, pin


# Upload Views
@login_required
def upload_aadhar(request):
    if request.method == 'POST':
        aadhar_file = request.FILES['aadhar_pdf']
        aadhar_pdf = UploadFiles.objects.create(file=aadhar_file)
        aadhar_pdf.save()

        aadhar_name, aadhar_dob, aadhar_gender, aadhar_number, aadhar_Phone, aadhar_address, pin = extract_aadhar_data(aadhar_pdf)
        save_profile_info(request.user, None, None, None, None, aadhar_name, aadhar_dob, aadhar_gender, aadhar_number, aadhar_Phone, aadhar_address, pin)

        return render(request, 'result.html', {'aadhar_name': aadhar_name, 'aadhar_dob': aadhar_dob, 'aadhar_gender': aadhar_gender, 'aadhar_number': aadhar_number, 'aadhar_Phone': aadhar_Phone, 'aadhar_address': aadhar_address, 'pin': pin})

    return render(request, 'upload.html')


@login_required
def upload_pan_card(request):
    if request.method == 'POST':
        form = PANCardForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            uploaded_image = request.FILES['image']
            img = Image.open(uploaded_image)
            dob, pan, name, father_name = extract_information(img)
            save_profile_info(request.user, name, dob, pan, father_name, None, None, None, None, None, None, None)
            return render(request, 'success_page.html', {'dob': dob, 'pan': pan, 'name': name, 'father_name': father_name})
    else:
        form = PANCardForm()
    return render(request, 'pan.html', {'form': form})


# Profile Information Saving Function
def save_profile_info(user, name, dob, pan, father_name, aadhar_name, aadhar_dob, aadhar_gender, aadhar_number, aadhar_Phone, aadhar_address, pin):
    def convert_date(date_str):
        if date_str:
            return datetime.strptime(date_str, '%d/%m/%Y').strftime('%Y-%m-%d')
        return None

    def clean_aadhar_number(aadhar_num):
        if aadhar_num:
            return ''.join(filter(str.isdigit, aadhar_num))
        return None

    if pan:
        dob = convert_date(dob)
        user_profile, created = Profile.objects.get_or_create(user=user)
        user_profile.name = name
        user_profile.DOB = dob
        user_profile.Pan = pan
        user_profile.Fathers_Name = father_name
    elif aadhar_name:
        user_profile, created = Profile.objects.get_or_create(user=user)
        user_profile.name = aadhar_name
        user_profile.DOB = convert_date(aadhar_dob)
        user_profile.Fathers_Name = father_name
        user_profile.aadhar_gender = aadhar_gender
        user_profile.aadhar_number = clean_aadhar_number(aadhar_number)
        user_profile.aadhar_Phone = aadhar_Phone
        user_profile.aadhar_address = aadhar_address
        user_profile.pin = pin

    user_profile.save()


# Result and Success Page Views
def result(request):
    return render(request, 'result.html')


def success_page(request):
    return render(request, 'success_page.html')

def contact(request):
    return render(request, 'contact.html')