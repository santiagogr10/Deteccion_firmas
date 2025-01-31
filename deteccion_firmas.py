from pdf2image import convert_from_path
import cv2
import numpy as np
import os
import shutil
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import io

from PyPDF2 import PageObject
from pdf2image import convert_from_path


def folder(path):
    image_path = r'C:\Users\santi\OneDrive\Escritorio\projects\SODIMAC\firmas\firma.png'
    output_folder = r'C:\Users\santi\OneDrive\Escritorio\projects\SODIMAC\firmas\firmado'
    no_firmado_folder = r'C:\Users\santi\OneDrive\Escritorio\projects\SODIMAC\firmas\no_firmado'

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(no_firmado_folder):
        os.makedirs(no_firmado_folder)

    for filename in os.listdir(path):
        cont = 0 
        file_path = os.path.join(path, filename)
        num_pages = get_pdf_page_count(file_path)

        if num_pages == 20:
            hojas = convert_pdf_to_images_primero(file_path)  # Ahora no se guarda en ninguna carpeta
            b = 7
        else:
            continue

        for i in hojas.values():
            image = i[0]  # Ahora la imagen está en memoria
            square_coordinates = (i[1][0][0], i[1][0][1], i[1][1][0], i[1][1][1])
            signature_detected = detect_signature_with_visualization(image, square_coordinates)
            if signature_detected:
                cont += 1

        if cont == b:
            x = 70  # Coordenada X para la imagen
            y = 170
            output_path = os.path.join(output_folder, os.path.basename(file_path))
            insert_image_in_last_page(file_path, image_path, output_path, x, y, width=30, height=30)
        else:
            shutil.copy(file_path, no_firmado_folder)

def get_pdf_page_count(pdf_path):
    reader = PdfReader(pdf_path)
    return len(reader.pages)

def convert_pdf_to_images_primero(pdf_path):
    ubi_firma = {
        1: ((140, 2140), (660 - 130, 2183 - 2140)),
        4: ((238, 1567), (675 - 234, 1628 - 1560)),
        5: ((811, 1911), (1382 - 811, 1968 - 1911)),
        6: ((394, 1550), (822 - 394, 1581 - 1541)),
        7: ((977, 1318), (1372 - 977, 1365 - 1318)),
        8: ((280, 1750), (590 - 280, 1794 - 1750)),
        20: ((960, 1675), (1495 - 960, 1723 - 1675)),
    }
    return convert_pdf_to_images_generic(pdf_path, ubi_firma)

def convert_pdf_to_images_generic(pdf_path, ubi_firma):
    dic = {k: [0, 0] for k in ubi_firma}
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        page_num = i + 1
        if page_num in ubi_firma:
            # No se guarda la imagen en ninguna carpeta, solo se mantiene en memoria
            dic[page_num][0] = np.array(image)  # Convertimos la imagen a un array de NumPy
            dic[page_num][1] = ubi_firma[page_num]
    return dic

def detect_signature_with_visualization(image, square_coords):
    x, y, w, h = square_coords
    roi = image[y:y+h, x:x+w]
    
    # Verificar si algún valor en la ROI es menor o igual a 240
    return np.any(roi <= 240)

def insert_image_in_last_page(pdf_path, image_path, output_path, x, y, width=None, height=None):
    # Leer el PDF existente
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    # Obtener la última página
    last_page_index = len(reader.pages) - 1
    last_page = reader.pages[last_page_index]

    # Convertir la última página a una imagen para eliminar capas ocultas
    images = convert_from_path(pdf_path, first_page=last_page_index+1, last_page=last_page_index+1)
    last_page_image = images[0]  # Convertimos solo la última página

    # Guardar la imagen temporalmente para trabajar sobre ella
    temp_image_path = "temp_last_page.jpg"
    last_page_image.save(temp_image_path, "JPEG")

    # Crear un lienzo en memoria
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    # Dibujar la imagen de la última página en el lienzo
    can.drawImage(temp_image_path, 0, 0, width=letter[0], height=letter[1])

    # Ajustar el tamaño de la firma
    if width is None or height is None:
        image = ImageReader(image_path)
        img_width, img_height = image.getSize()
        width = width if width else img_width * 2  # Aumentar tamaño 50%
        height = height if height else img_height * 2

    # Dibujar la firma encima de la imagen de la página
    can.drawImage(image_path, x, y, width=width, height=height)

    # Guardar el lienzo
    can.showPage()
    can.save()

    # Mover a la primera posición en el lienzo en memoria
    packet.seek(0)

    # Leer el contenido del lienzo en memoria como un PDF
    new_pdf = PdfReader(packet)

    # Crear una nueva página en blanco con la imagen fusionada
    new_last_page = PageObject.create_blank_page(width=letter[0], height=letter[1])
    new_last_page.merge_page(new_pdf.pages[0])

    # Agregar todas las páginas del PDF original al escritor
    for i in range(len(reader.pages)):
        if i == last_page_index:
            writer.add_page(new_last_page)  # Reemplazamos la última página con la nueva
        else:
            writer.add_page(reader.pages[i])

    # Escribir el PDF modificado en el archivo de salida
    with open(output_path, 'wb') as f:
        writer.write(f)

    # Eliminar imagen temporal
    os.remove(temp_image_path)


pdfs = folder(r'C:\Users\santi\OneDrive\Escritorio\projects\SODIMAC\firmas\pdf')
