import os
from arabic_reshaper import ArabicReshaper
from bidi.algorithm import get_display
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import goldenrod, black
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont 
from datetime import datetime

# goldenrod = colors.HexColor("#CAA860")
# black = colors.HexColor("#347181")

def get_static_path():
    """Function to get the static path."""
    return os.path.join(os.getcwd() , 'staticfiles')

# Registering fonts
pdfmetrics.registerFont(TTFont('Arabic', os.path.join(get_static_path(),'Arabic.ttf')))
pdfmetrics.registerFont(TTFont('Arabic-Bold', os.path.join(get_static_path(),'Arabic-Bold.ttf')))

def generate_pdf(pdf_name,service_num,info):
    """Function to generate PDF."""
    # Configuring ArabicReshaper
    configuration = {
        'delete_harakat': False,
        'support_ligatures': True,
    }
    reshaper = ArabicReshaper(configuration=configuration)

    # Creating Canvas
    static_path = get_static_path()
    canvas = Canvas(os.path.join(static_path , f"pdfs/{pdf_name}.pdf"))

    # Adding logo
    add_logo(canvas,reshaper)

    service_name, data = prepare_data(service_num,info)

    # Adding data
    add_data(canvas, reshaper,service_name,data)

    # Saving the file
    canvas.save()

def add_logo(canvas,reshaper):
    """Function to add logo to the PDF."""
    logo_width = 300
    logo_height = 50

    static_path = get_static_path()
    # background_path = os.path.join(static_path , "BG.jpg")
    # canvas.drawImage(background_path, 0, 0)
    logo_path = os.path.join(static_path , "SIIB_logo.png")
    canvas.drawInlineImage(str(logo_path), canvas._pagesize[0] - (.5 * inch) - logo_width, canvas._pagesize[1] - (inch), width=logo_width, height=logo_height, anchor='ne', preserveAspectRatio=True)

    canvas.setFont('Arabic', 10)
    canvas.setFillColor(black)
    footer = "بنك سورية الدولي الإسلامي ش.م.م.ع رأس المال ١۵,۰۰۰,۰۰۰,۰۰۰ ل.س مدفوعة بالكامل سجل تجاري رقم ١٤٨٨٦ دمشق"
    canvas.drawRightString(canvas._pagesize[0] - 20 * mm, 10, get_display(reshaper.reshape(footer)))

def add_data(canvas, reshaper,service_name,data):
    """Function to add data to the PDF."""
    width = canvas._pagesize[0]
    padding = 10 * mm
    
    canvas.setFont("Arabic-Bold", 24)
    canvas.setFillColor(goldenrod)

    header = f"الخدمة المطلوبة: {service_name}"
    if service_name == 'فتح حساب التوفير':
        canvas.drawRightString(width - 4.5*padding, 700, get_display(reshaper.reshape(header)))
    else:
        canvas.drawRightString(width - 6*padding, 700, get_display(reshaper.reshape(header)))

    canvas.setFont('Arabic', 14)
    canvas.setFillColor(black)

    lines = data

    # Setting the initial value for ys
    start_value = 650

    # Decrement value for each line
    decrement = 25

    # Creating ys list based on the number of sentences and distributing the values
    ys = [start_value - decrement * i for i in range(len(lines))]

    for y, line in zip(ys, lines):
        canvas.drawRightString(width - padding, y, get_display(reshaper.reshape(line)))
    
    canvas.setFont('Arabic-Bold', 16)
    canvas.setFillColor(black)

    sign = "التوقيع"
    canvas.drawRightString(150, 150, get_display(reshaper.reshape(sign)))

def prepare_data(service_num,info):

    # Convert time from JSON string to datetime object
    # created_time = datetime.strptime(info['created'], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Format the time in the desired format
    # formatted_time = created_time.strftime("%H:%M:%S %Y-%m-%d")

    formatted_time = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    
    if service_num == 0:
        service_name = 'فتح حساب التوفير'
        data = [
            "الرقم الوطني: "+f"{info['national_id']}",
            "الاسم الثلاثي: "+f"{info['client_name']}",
            "اسم وكنية الأم: "+f"{info['mother_firstname']} {info['mother_lastname']}",
            "العنوان: "+f"{info['address']}"
            ]
        
        if info['working']:
            data.extend([
                "العمل: "+"يملك عمل",
                "مجال العمل: "+f"{info['working_field']}",
                "اسم الشركة: "+f"{info['company_name']}",
                "الراتب الشهري: "+f"{info['salary']}"
            ])
        if not info['working']:
            data.extend([
                "العمل: "+f"{info['client_status']}"
            ])
        
        if info['housing']:
            data.append(
                "المنزل: "+"ملك"
            )
        if not info['housing']:
            data.append(
                "المنزل: "+ "آجار"
            )
        
        if info['married']:
            data.extend([
                "الحالة الاجتماعية: "+"متزوج",
                "اسم وكنية الزوج / ة: "+f"{info['spouse_firstname']} {info['spouse_lastname']}",
                "عدد الأطفال: "+f"{info['num_children']}"
            ])
        if not info['married']:
            data.append(
                "الحالة الاجتماعية: "+"غير متزوج"
            )
        
        data.extend([
            "رقم الموبايل: "+f"{info['phone']}",
            "وقت الطلب: "+f"{formatted_time}"
        ])
            
    elif service_num == 1:
        service_name = info['service_name']
        data = [
            "الرقم الوطني: "+f"{info['client']}",
            "رقم الحساب: "+f"{info['account_id']}",
            "الاسم الثلاثي: "+f"{info['client_name']}",
            "المبلغ المراد إيداعه: "+f"{info['amount']}",
            "مصدر المبلع المودع: "+f"{info['source']}",
            "سبب الإيداع: "+f"{info['cause']}",
            "رقم الموبايل: "+f"{info['phone']}",
            "وقت الطلب: "+f"{formatted_time}"
        ]
        
    elif service_num == 2:
        service_name = info['service_name']
        data = [
            "الرقم الوطني: "+f"{info['client']}",
            "رقم الحساب: " + f"{info['account_id']}",
            "الاسم الثلاثي: "+f"{info['client_name']}",
            "المبلغ المراد سحبه: "+f"{info['amount']}",
            "سبب السحب: "+f"{info['cause']}",
            "رقم الموبايل: "+f"{info['phone']}",
            "وقت الطلب: "+f"{formatted_time}"
        ]
    return service_name,data
