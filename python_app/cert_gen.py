#!/bin/python3.6
from fpdf import FPDF
import random
import string

countries = {
    'GTN': 'rus_crt.jpg',
    'KNG': 'kj_crt.jpg', 
    'NGT': 'tj_crt.jpg',
    'KAZ': 'kz_crt.jpg',
    'KGN': 'kj_crt.jpg',
    'NG2': 'rus_crt.jpg',
    }



letters = string.ascii_lowercase

def generate_cert(codes):
    names = []
    for code in codes:
        img_path = countries[code[0:3]]
        txt ='  '.join(list(code))
        pdf = FPDF(orientation='L', unit='pt', format=(708, 1500))
        pdf.add_page()
        pdf.set_font("Arial", size=24)
        pdf.image(img_path, x=0, y=0, w=1500, h=708)
        pdf.set_text_color(r=90)
        pdf.text(1130, 531, txt=txt)
        name = ''.join(random.choice(letters) for i in range(15)) 
        pdf.output('./certs_folder/{}.pdf'.format(name))
        names.append(name)
    return names