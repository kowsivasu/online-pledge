from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import PledgeForm, PledgeCreateForm
from .models import Pledge, pledgeCreate
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from .models import Admin
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from django.utils import translation
from django.utils.translation import gettext as _
from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime
import os
from django.conf import settings
import html

# Create your views here.

# frontend pledge page view and pledge store
def download_certificate(request, pledge_id):
    # 1. Fetch data
    pledge_data = Pledge.objects.get(id=pledge_id)
    user_name = pledge_data.name 
    
    # 2. Load the template
    template_path = os.path.join(settings.MEDIA_ROOT, 'certificate_template.jpg')
    image = Image.open(template_path).convert("RGBA")
    draw = ImageDraw.Draw(image)
    width, height = image.size

    # --- SECTION 1: DYNAMIC LOGOS (Centered with Top Margin) ---
    pledgeCreateField = pledgeCreate.objects.first()
    logo_fields = [pledgeCreateField.logo1, pledgeCreateField.logo2, pledgeCreateField.logo3]
    active_logos = [f for f in logo_fields if f]

    if active_logos:
        processed_logos = []
        target_h = 90  # Increased slightly for better visibility
        for logo_field in active_logos:
            img = Image.open(logo_field.path).convert("RGBA")
            aspect = img.width / img.height
            img = img.resize((int(target_h * aspect), target_h))
            processed_logos.append(img)

        spacing = 40
        total_group_width = sum(l.width for l in processed_logos) + (spacing * (len(processed_logos) - 1))
        
        current_x = (width - total_group_width) / 2
        # Move logos down from the very edge for a cleaner look
        y_logo = 250  

        for l in processed_logos:
            image.paste(l, (int(current_x), y_logo), l)
            current_x += l.width + spacing

    # --- SECTION 2: STATIC TEXT (Now placed correctly BELOW "Given To") ---
    static_text = "has successfully taken the pledge to support the mission."
    try:
        static_font = ImageFont.truetype("arial.ttf", 30)
    except:
        static_font = ImageFont.load_default()
        
    s_w = draw.textlength(static_text, font=static_font)
    # This sits between the "Award is given to" text and the dashed line
    draw.text(((width - s_w) / 2, 700), static_text, fill="#555555", font=static_font)

    # --- SECTION 3: THE USER NAME (Now perfectly on the Dash) ---
    try:
        # Bold font makes the name stand out
        name_font = ImageFont.truetype("arialbd.ttf", 40) 
    except:
        name_font = ImageFont.truetype("arial.ttf", 40)

    n_w = draw.textlength(user_name, font=name_font)
    x_name = (width - n_w) / 2
    
    # ADJUSTED: On this template, the dashed line is at roughly 615px
    # Your previous code was putting it at 825, which was off-screen or too low
    y_name = 800 


    draw.text((x_name, y_name), user_name, fill="#2c3e50", font=name_font)

    # 3. Finalize and Return
    image = image.convert("RGB")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=95)
    buffer.seek(0)

    # Correct way to return the file for download
    response = HttpResponse(buffer, content_type="image/jpeg")
    
    # This header is what triggers the 'Download' dialog in the browser
    filename = f"certificate_{pledge_id}.jpg"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

def pledge_page(request):
    if request.method == "POST":
        form = PledgeForm(request.POST)
        pledgeCreateObj = pledgeCreate.objects.first()
        selectedLanguage = request.POST.get("pledgeLanguage")

        if form.is_valid():
            pledge = form.save(commit=False)
            if selectedLanguage == "TA":
                pledge.pledge_text = pledgeCreateObj.tamilPledgeText
                pledge.pledgeName = pledgeCreateObj.tamilPledgeName
            elif selectedLanguage == "HI":
                pledge.pledge_text = pledgeCreateObj.hindiPledgeText
                pledge.pledgeName = pledgeCreateObj.hindiPledgeName
            else:
                pledge.pledge_text = pledgeCreateObj.pledgeText
                pledge.pledgeName = pledgeCreateObj.pledgeName


            pledge = form.save()
            return redirect("thankyou", pledgeCreateObj_id=pledgeCreateObj.id, pledge_id=pledge.id)

    else:
        form = PledgeForm()
        pledgeCreateObj = pledgeCreate.objects.first()


    return render(request, "pledge.html", {"form": form, "pledgeCreateObj": pledgeCreateObj})

def thankyou_page(request, pledgeCreateObj_id,pledge_id):
    pledgeCreateObj = pledgeCreate.objects.get(id=pledgeCreateObj_id)
    pledge = Pledge.objects.get(id=pledge_id)

    return render(request, "thankyou.html", {"pledgeCreateObj":pledgeCreateObj, "pledge": pledge})

@login_required
def pledgeList(request):
    pledges = Pledge.objects.all()
    return render(request, "pledge_list.html", {"pledges": pledges})

@login_required
def pledgeView(request, id):
    pledge = get_object_or_404(Pledge, id=id)
    return render(request, "pledge_view.html", {"pledge":pledge})

def generate_pdf(request, id):
    pledge = Pledge.objects.get(id=id)

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph("Pledge Details", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    data = [
        ["Name:", pledge.name],
        ["Email:", pledge.email],
        ["Department:", pledge.department],
        ["Designation:", pledge.designation],
    ]

    table = Table(data, colWidths=[120, 300])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
    ]))

    elements.append(table)

    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="pledge_{id}.pdf"'
    response.write(pdf)

    return response

@login_required
def adminList(request):
    admins = User.objects.all()
    return render(request, "admin_list.html", {"admins":admins})

#admin create page
@login_required
def adminCreate(request):
    form = UserForm()
    return render(request, "admin_create.html", {"form": form})

#login page
def login_page(request):
    return render(request, "login.html")

#authentication
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            # Get user by email
            user_obj = User.objects.get(email=email)

            # Authenticate using username
            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is not None:
                login(request, user)
                return redirect("admins")  # your dashboard page
            else:
                messages.error(request, "Invalid password")

        except User.DoesNotExist:
            messages.error(request, "Email not registered")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect("login_page")


#admin store function
def create_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")

        if username and email and password:
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name
            )
            return redirect("admins")
        else:
            messages.error(request, "All fields are required")

    return render(request, "admin_create.html")

@login_required
def pledgeCreatePage(request):
    form = PledgeCreateForm()
    return render(request, "PledgeCreatePage.html", {"form": form})

@login_required
def backendPledgeList(request):
    pledges = pledgeCreate.objects.all()
    return render(request, "backend_pledges.html", {"pledges":pledges})

def pledgeStore(request):
    if request.method == "POST":
        pledgeName = request.POST.get("pledgeName")
        pledgeText = request.POST.get("pledgeText")
        checkboxText = request.POST.get("checkboxText")
        logo1 = request.FILES.get("logo1")
        logo2 = request.FILES.get("logo2")
        logo3 = request.FILES.get("logo3")
        tamilPledgeText = request.POST.get("tamilPledgeText")
        hindiPledgeText = request.POST.get("hindiPledgeText")


        pledgeCreate.objects.create(
            pledgeName = pledgeName,
            pledgeText = pledgeText,
            checkboxText = checkboxText,
            logo1 = logo1,
            logo2 = logo2,
            logo3 = logo3,
            tamilPledgeText = tamilPledgeText,
            hindiPledgeText = hindiPledgeText
        )

        return redirect("backend_pledges")

def backendPledgeView(request, id):
    pledge = get_object_or_404(pledgeCreate, id=id)
    clean_text = html.unescape(pledge.pledgeText)
    context = {
        "clean_text": clean_text
    }
    return render(request, "backend_pledge_view.html", {"pledge":pledge, "clean_text":clean_text})

def backendPledgeUpdate(request, id):
    pledge = get_object_or_404(pledgeCreate, id=id)
    return render(request, "backend_pledge_update.html", {"pledge":pledge})

def pledgeUpdateFun(request, id):
    pledge = get_object_or_404(pledgeCreate, id=id)

    if request.method == "POST":
        pledge.pledgeName = request.POST.get("pledgeName")
        pledge.pledgeText = request.POST.get("pledgeText")
        pledge.checkboxText = request.POST.get("checkboxText")
        pledge.language = request.POST.get("language")
        pledge.tamilPledgeText = request.POST.get("tamilPledgeText")
        pledge.hindiPledgeText = request.POST.get("hindiPledgeText")
        pledge.tamilPledgeName = request.POST.get("tamilPledgeName")
        pledge.hindiPledgeName = request.POST.get("hindiPledgeName")

        if request.FILES.get("logo1"):
            pledge.logo1 = request.FILES.get("logo1")

        if request.FILES.get("logo2"):
            pledge.logo2 = request.FILES.get("logo2")

        if request.FILES.get("logo3"):
            pledge.logo3 = request.FILES.get("logo3")

        pledge.save()

        return redirect("backend_pledges")

    return render(request, "backend_pledge_edit.html", {"pledge": pledge})

