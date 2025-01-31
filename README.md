# 📄 Detección de Firmas en Documentos PDF

## 📌 Descripción
Este proyecto automatiza la detección de firmas en documentos PDF mediante el uso de **procesamiento de imágenes** con OpenCV y la conversión de PDFs a imágenes con pdf2image.

El sistema analiza documentos con un número específico de páginas y evalúa la presencia de firmas en ubicaciones predefinidas. Si un documento está firmado correctamente, se marca y se almacena en una carpeta; si no, se redirige a otra carpeta para su revisión.

## 🚀 Características
- 📂 Conversión de documentos PDF a imágenes para su procesamiento.
- 🔍 Detección automática de firmas en posiciones específicas.
- 🗂 Clasificación de documentos en **firmados** y **no firmados**.
- ✏️ Inserción de una marca en documentos firmados correctamente.
- 📊 Uso de OpenCV y NumPy para el análisis de imágenes.

## 📦 Instalación
Para ejecutar el proyecto, primero instala las dependencias necesarias:

```bash
pip install opencv-python numpy pdf2image PyPDF2 reportlab
```

Además, si estás en Windows, asegúrate de instalar **poppler** para convertir PDFs a imágenes:
- Descarga **poppler** desde: https://github.com/oschwartz10612/poppler-windows/releases
- Extrae los archivos y agrega la carpeta `bin/` a la variable de entorno `PATH`.

## ⚙️ Uso
Para ejecutar la automatización, simplemente llama a la función principal:

```python
from deteccion_firmas import folder

folder("ruta/del/directorio/de/pdfs")
```

Esto procesará los PDFs en la carpeta indicada y clasificará los documentos en:
- 📁 **firmado/** (cuando detecta firmas en todas las páginas requeridas)
- 📁 **no_firmado/** (cuando la firma no está presente)

## 📂 Estructura del Proyecto
```bash
/
├── deteccion_firmas.py   # Código principal
├── README.md             # Documentación del proyecto
├── fotos/                # Carpeta para imágenes de referencia (opcional)
├── firmado/              # PDFs correctamente firmados
├── no_firmado/           # PDFs sin firmas
└── pdfs/                 # Carpeta con los archivos a procesar
```

## 🔮 Posibles Mejoras
- 💡 Permitir la detección de firmas en documentos con diferentes formatos de página.
- 🤖 Implementar un modelo de **Machine Learning** para mejorar la detección de firmas.
- 📊 Crear un dashboard para visualizar los resultados de la automatización.

---
💡 **Este proyecto fue desarrollado como parte de una automatización en People Analytics para Sodimac Homecenter.**

