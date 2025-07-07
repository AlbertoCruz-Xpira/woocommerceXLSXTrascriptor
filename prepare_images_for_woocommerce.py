#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script auxiliar para preparar imágenes para WooCommerce
Crea un paquete ZIP con las imágenes listo para subir a WordPress
"""

import os
import zipfile
import shutil
from datetime import datetime

def create_image_package():
    """
    Crea un paquete con las imágenes listo para subir a WordPress
    """
    images_folder = 'product_images'
    
    if not os.path.exists(images_folder):
        print("❌ No se encontró la carpeta de imágenes")
        print("💡 Ejecuta primero: python csv_to_woocommerce.py --ejemplo --imagenes")
        return
    
    # Contar imágenes
    image_files = [f for f in os.listdir(images_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not image_files:
        print("❌ No se encontraron imágenes en la carpeta")
        return
    
    print(f"📁 Encontradas {len(image_files)} imágenes")
    
    # Crear ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"woocommerce_images_{timestamp}.zip"
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for image_file in image_files:
            image_path = os.path.join(images_folder, image_file)
            zipf.write(image_path, image_file)
    
    print(f"✅ Paquete creado: {zip_filename}")
    print(f"📦 Contiene {len(image_files)} imágenes")
    print(f"📁 Ubicación: {os.path.abspath(zip_filename)}")
    
    print("\n" + "="*60)
    print("📋 INSTRUCCIONES PARA WORDPRESS:")
    print("="*60)
    print("1. 📂 Accede a tu servidor WordPress via FTP/cPanel")
    print("2. 📁 Ve a la carpeta: /wp-content/uploads/")
    print(f"3. ⬆️  Sube el archivo: {zip_filename}")
    print("4. 📦 Extrae el ZIP en esa ubicación")
    print("5. 🔄 Importa el CSV en WooCommerce")
    print("\n💡 Las rutas de imágenes en el CSV serán válidas después de esto")
    
    return zip_filename

def show_instructions():
    """
    Muestra instrucciones detalladas
    """
    print("=== GUÍA COMPLETA DE IMÁGENES PARA WOOCOMMERCE ===")
    print()
    print("🔄 PROCESO COMPLETO:")
    print("1. python csv_to_woocommerce.py --ejemplo --imagenes")
    print("2. python prepare_images_for_woocommerce.py")
    print("3. Subir ZIP a WordPress")
    print("4. Importar CSV en WooCommerce")
    print()
    print("📁 ESTRUCTURA GENERADA:")
    print("├── productos_woocommerce_YYYYMMDD_HHMMSS.csv")
    print("├── product_images/")
    print("│   ├── producto-0001-chesterfield-24.jpg")
    print("│   ├── producto-0002-carton-chesterfield.jpg")
    print("│   └── ...")
    print("├── woocommerce_images_YYYYMMDD_HHMMSS.zip")
    print("└── image_cache.json")
    print()
    print("🌐 RUTA EN WORDPRESS:")
    print("/wp-content/uploads/producto-XXXX-nombre.jpg")

if __name__ == "__main__":
    import sys
    
    if '--help' in sys.argv or '-h' in sys.argv:
        show_instructions()
    else:
        create_image_package()
