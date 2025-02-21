from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
import qrcode
import os
import subprocess

# Configuración de la etiqueta
LABEL_WIDTH = 2.3 * inch  # 2 pulgadas de ancho
LABEL_HEIGHT = 1 * inch  # 1 pulgada de alto
QR_SIZE = 0.8 * inch  # Tamaño del QR
MARGIN = 0.1 * inch  # Margen alrededor del QR
TEXT_SPACING = 0.1 * inch  # Espaciado entre el QR y el texto

# Datos de ejemplo
datos = [
    {"codigo": "C001", "texto1": "L1", "texto2": "M1"},
    {"codigo": "C002", "texto1": "L2", "texto2": "M2"},
    {"codigo": "C003", "texto1": "L3", "texto2": "M3"},
]

def generar_qr(texto, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(filename)

def crear_pdf(nombre_archivo, datos):
    c = canvas.Canvas(nombre_archivo, pagesize=(LABEL_WIDTH, LABEL_HEIGHT))
    
    for item in datos:
        texto_qr = item['codigo']
        temp_file = f"temp_qr_{texto_qr}.png"
        generar_qr(texto_qr, temp_file)
        
        # Dibujar QR en la parte izquierda
        qr_x = MARGIN
        qr_y = (LABEL_HEIGHT - QR_SIZE) / 2
        c.drawImage(temp_file, qr_x, qr_y, width=QR_SIZE, height=QR_SIZE)
        
        # Dibujar textos a la derecha del QR en negrita
        text_x = qr_x + QR_SIZE + TEXT_SPACING
        text_y = qr_y + QR_SIZE / 2 + 5  # Ajuste para centrar texto con respecto al QR
        c.setFont("Helvetica-Bold", 10)
        c.drawString(text_x, text_y, item['texto1'])
        c.drawString(text_x, text_y - 12, item['texto2'])
        
        c.showPage()
        
        # Eliminar QR temporal
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    c.save()
    
    # Abrir PDF automáticamente
    if os.name == "nt":
        os.startfile(nombre_archivo)
    else:
        subprocess.run(["xdg-open", nombre_archivo], check=False)

# Ejecutar generación
crear_pdf("codigos_qr.pdf", datos)
