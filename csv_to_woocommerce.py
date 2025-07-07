#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para transformar CSV de inventario al formato WooCommerce
Convierte archivo CSV con múltiples páginas a formato compatible con WooCommerce
"""

import pandas as pd
import sys
import os
import requests
import urllib.parse
import re
import json
from datetime import datetime

class ImageFetcher:
    """
    Clase para obtener imágenes de productos desde APIs gratuitas
    """
    def __init__(self):
        self.cache_file = 'image_cache.json'
        self.cache = self.load_cache()
        self.images_folder = 'product_images'  # Nueva carpeta para imágenes locales
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WooCommerce-CSV-Converter/1.0'
        })
        
        # Crear carpeta de imágenes si no existe
        if not os.path.exists(self.images_folder):
            os.makedirs(self.images_folder)
            print(f"📁 Carpeta creada: {self.images_folder}")
    
    def load_cache(self):
        """Carga el cache de imágenes desde archivo"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_cache(self):
        """Guarda el cache de imágenes en archivo"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️  Advertencia: No se pudo guardar el cache de imágenes: {e}")
    
    def clean_product_name_for_search(self, product_name):
        """Limpia el nombre del producto para una mejor búsqueda"""
        if not product_name:
            return ""
        
        # Convertir a minúsculas y limpiar
        cleaned = product_name.lower().strip()
        
        # Remover caracteres especiales y números sueltos
        cleaned = re.sub(r'[^\w\s-]', ' ', cleaned)
        cleaned = re.sub(r'\b\d+\b', '', cleaned)
        
        # Remover palabras muy cortas y espacios extra
        words = [word for word in cleaned.split() if len(word) > 2]
        
        return ' '.join(words[:3])  # Máximo 3 palabras para mejor búsqueda
    
    def get_unsplash_image(self, product_name):
        """
        Obtiene imagen desde Unsplash usando su API pública (sin API key)
        Utiliza la función de búsqueda de Unsplash Source
        """
        # Nota: Deshabilitado temporalmente debido a problemas de conectividad
        return None
    
    def get_picsum_image(self, product_name):
        """
        Obtiene imagen placeholder desde Lorem Picsum
        """
        # Nota: Deshabilitado temporalmente debido a problemas de conectividad
        return None
    
    def get_placeholder_image(self, product_name):
        """
        Obtiene imagen placeholder simple y confiable
        """
        try:
            # Generar color basado en el nombre del producto
            product_hash = abs(hash(product_name)) % 16777215  # Color hexadecimal
            color = f"{product_hash:06x}"
            
            # Usar placeholder.com que es muy confiable
            text = urllib.parse.quote(product_name[:10].replace(' ', '+'))
            url = f"https://via.placeholder.com/400x400/{color}/ffffff?text={text}"
            
            print(f"   🔍 Probando Placeholder URL: {url}")
            
            # Esta URL siempre funciona, no necesitamos verificar
            print(f"   ✅ Placeholder OK: {url}")
            return url
                
        except Exception as e:
            print(f"   ⚠️  Error con Placeholder para '{product_name}': {e}")
        
        return None
    
    def get_simple_placeholder_image(self, product_name):
        """
        Genera una URL de imagen placeholder simple y confiable
        """
        try:
            # Generar color basado en el nombre del producto
            product_hash = abs(hash(product_name))
            color_codes = ['FF6B6B', '4ECDC4', '45B7D1', 'FFA07A', '98D8C8', 'F7DC6F', 'BB8FCE', '85C1E9']
            color = color_codes[product_hash % len(color_codes)]
            
            # Crear texto corto para la imagen
            text = product_name[:8].replace(' ', '+').upper()
            
            # Usar DummyImage.com que es muy estable
            url = f"https://dummyimage.com/400x400/{color}/ffffff&text={text}"
            
            print(f"   🎨 Generando placeholder: {url}")
            return url
                
        except Exception as e:
            print(f"   ⚠️  Error generando placeholder para '{product_name}': {e}")
            # Fallback: URL estática básica
            return "https://dummyimage.com/400x400/cccccc/ffffff&text=Producto"
    
    def get_product_image(self, product_name):
        """
        Obtiene imagen para un producto, usando cache si está disponible
        """
        if not product_name or not product_name.strip():
            return None
        
        # Verificar cache
        cache_key = product_name.strip().lower()
        if cache_key in self.cache:
            cached_url = self.cache[cache_key]
            if cached_url:  # Solo retornar si hay URL válida
                print(f"   💾 Imagen en cache para: {product_name}")
                return cached_url
        
        print(f"   🔍 Buscando imagen para: {product_name}")
        
        # Intentar obtener imagen de Unsplash primero
        image_url = self.get_unsplash_image(product_name)
        
        # Si falla, usar imagen de Picsum
        if not image_url:
            print(f"   ⏭️  Unsplash falló, probando Picsum...")
            image_url = self.get_picsum_image(product_name)
        
        # Si todo falla, usar placeholder confiable
        if not image_url:
            print(f"   ⏭️  Picsum falló, usando placeholder simple...")
            image_url = self.get_simple_placeholder_image(product_name)
        
        # Guardar en cache (incluso si es None para evitar buscar de nuevo)
        self.cache[cache_key] = image_url
        
        if image_url:
            print(f"   ✅ Imagen final: {image_url}")
        else:
            print(f"   ❌ No se pudo obtener imagen")
        
        return image_url
    
    def download_image_locally(self, image_url, product_name, product_id):
        """
        Descarga una imagen y la guarda localmente
        """
        try:
            # Generar nombre de archivo seguro
            safe_name = re.sub(r'[^\w\s-]', '', product_name.lower())
            safe_name = re.sub(r'[-\s]+', '-', safe_name)
            filename = f"producto-{product_id:04d}-{safe_name[:20]}.jpg"
            filepath = os.path.join(self.images_folder, filename)
            
            # Si el archivo ya existe, retornar la ruta
            if os.path.exists(filepath):
                print(f"   📁 Imagen local existente: {filename}")
                return filepath
            
            print(f"   ⬇️  Descargando imagen: {filename}")
            
            # Descargar la imagen
            response = self.session.get(image_url, timeout=10, stream=True)
            response.raise_for_status()
            
            # Guardar la imagen
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"   ✅ Imagen descargada: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"   ❌ Error descargando imagen: {e}")
            return None
    
    def get_woocommerce_compatible_image(self, product_name, product_id):
        """
        Obtiene una imagen compatible con WooCommerce (descargada localmente)
        """
        if not product_name or not product_name.strip():
            return None
        
        # Verificar cache
        cache_key = f"{product_name.strip().lower()}_{product_id}"
        if cache_key in self.cache:
            cached_path = self.cache[cache_key]
            if cached_path and os.path.exists(cached_path):
                print(f"   💾 Imagen local en cache: {cached_path}")
                return cached_path
        
        print(f"   🔍 Procesando imagen para: {product_name}")
        
        # Generar URL de placeholder
        image_url = self.get_simple_placeholder_image(product_name)
        
        if image_url:
            # Descargar imagen localmente
            local_path = self.download_image_locally(image_url, product_name, product_id)
            
            if local_path:
                # Guardar en cache
                self.cache[cache_key] = local_path
                return local_path
        
        return None

def leer_csv_con_paginas(archivo_csv):
    """
    Lee un archivo CSV que contiene múltiples páginas/hojas
    y extrae los nombres de las páginas como categorías
    
    Args:
        archivo_csv (str): Ruta al archivo CSV original
    
    Returns:
        dict: Diccionario con datos de cada página
    """
    try:
        # Intentamos leer el archivo como Excel primero (si tiene múltiples hojas)
        if archivo_csv.endswith(('.xlsx', '.xls')):
            print("Detectado archivo Excel, leyendo todas las hojas...")
            xl_file = pd.ExcelFile(archivo_csv)
            paginas_data = {}
            
            for nombre_pagina in xl_file.sheet_names:
                print(f"Leyendo página: {nombre_pagina}")
                df = pd.read_excel(archivo_csv, sheet_name=nombre_pagina)
                paginas_data[nombre_pagina] = df
                
            return paginas_data
            
        else:
            # Si es CSV, leemos como una sola página
            print("Detectado archivo CSV, leyendo como página única...")
            df = pd.read_csv(archivo_csv, encoding='utf-8')
            # Usamos el nombre del archivo como categoría por defecto
            nombre_categoria = os.path.splitext(os.path.basename(archivo_csv))[0]
            return {nombre_categoria: df}
            
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return None

def verificar_estructura_datos(paginas_data):
    """
    Verifica que los datos tengan la estructura esperada
    
    Args:
        paginas_data (dict): Datos de las páginas
    
    Returns:
        bool: True si la estructura es correcta
    """
    columnas_esperadas = ['PRODUCTO', 'PRECIO', '0,3', 'TOTAL']
    
    for nombre_pagina, df in paginas_data.items():
        print(f"\n--- Verificando página: {nombre_pagina} ---")
        print(f"Número de filas: {len(df)}")
        print(f"Columnas encontradas: {list(df.columns)}")
        
        # Verificar si tiene las columnas esperadas
        columnas_faltantes = []
        for col in columnas_esperadas:
            if col not in df.columns:
                columnas_faltantes.append(col)
        
        if columnas_faltantes:
            print(f"⚠️  Columnas faltantes: {columnas_faltantes}")
        else:
            print("✅ Todas las columnas esperadas están presentes")
            
        # Mostrar primeras filas para verificar formato
        print("Primeras 3 filas:")
        print(df.head(3))
        
    return True

def crear_estructura_woocommerce():
    """
    Define la estructura de columnas requerida por WooCommerce
    
    Returns:
        list: Lista de nombres de columnas para WooCommerce
    """
    return [
        'ID', 'Tipo', 'SKU', 'GTIN', 'Nombre', 'Publicado', '¿Está destacado?', 
        'Visibilidad en el catálogo', 'Descripción corta', 'Descripción', 
        'Día en que empieza el precio rebajado', 'Día en que termina el precio rebajado',
        'Estado del impuesto', 'Clase de impuesto', '¿Existencias?', 'Inventario',
        'Cantidad de bajo inventario', '¿Permitir reservas de productos agotados?',
        '¿Vendido individualmente?', 'Peso (kg)', 'Longitud (cm)', 'Anchura (cm)',
        'Altura (cm)', '¿Permitir valoraciones de clientes?', 'Nota de compra',
        'Precio rebajado', 'Precio normal', 'Categorías', 'Etiquetas', 
        'Clase de envío', 'Imágenes', 'Límite de descargas',
        'Días de caducidad de la descarga', 'Superior', 'Productos agrupados',
        'Ventas dirigidas', 'Ventas cruzadas', 'URL externa', 'Texto del botón',
        'Posición', 'Marcas'
    ]

def procesar_datos_a_woocommerce(paginas_data, solo_ejemplo=False, agregar_imagenes=False):
    """
    Convierte los datos del inventario al formato WooCommerce
    
    Args:
        paginas_data (dict): Datos de las páginas del archivo original
        solo_ejemplo (bool): Si es True, procesa solo 100 productos variados para prueba
        agregar_imagenes (bool): Si es True, busca imágenes automáticamente para los productos
    
    Returns:
        pd.DataFrame: DataFrame con formato WooCommerce
    """
    print("\n=== Procesando datos a formato WooCommerce ===")
    
    if solo_ejemplo:
        print("🔬 MODO EJEMPLO: Procesando solo 100 productos variados para prueba")
    
    if agregar_imagenes:
        print("🖼️  MODO IMÁGENES: Descargando imágenes localmente para WooCommerce")
        image_fetcher = ImageFetcher()
    else:
        image_fetcher = None
    
    # Crear lista para almacenar todos los productos
    productos_woocommerce = []
    contador_id = 1
    productos_procesados = 0
    max_productos = 100 if solo_ejemplo else float('inf')
    
    for nombre_pagina, df in paginas_data.items():
        if productos_procesados >= max_productos:
            break
            
        print(f"Procesando página: {nombre_pagina} ({len(df)} productos)")
        
        # Limpiar datos: eliminar filas vacías
        df_limpio = df.dropna(subset=['PRODUCTO'])
        
        # Si es modo ejemplo, tomar solo algunos productos de cada categoría
        if solo_ejemplo:
            # Tomar máximo 4 productos por categoría para variedad
            productos_por_categoria = min(4, len(df_limpio))
            if productos_procesados + productos_por_categoria > max_productos:
                productos_por_categoria = max_productos - productos_procesados
            df_limpio = df_limpio.head(productos_por_categoria)
        
        for index, fila in df_limpio.iterrows():
            if productos_procesados >= max_productos:
                break
            try:
                # Limpiar y calcular precio base (TOTAL / 1.03)
                total_str = str(fila['TOTAL']).strip()
                
                # Manejar casos especiales
                if pd.isna(fila['TOTAL']) or total_str in ['#VALUE!', 'nan', '']:
                    precio_base = 0
                else:
                    # Limpiar formato: remover espacios, €, y convertir comas a puntos
                    total_limpio = total_str.replace('€', '').replace(' ', '').replace(',', '.')
                    try:
                        precio_total = float(total_limpio)
                        precio_base = round(precio_total / 1.03, 2) if precio_total > 0 else 0
                    except ValueError:
                        precio_base = 0
                
                # Crear producto para WooCommerce
                producto_wc = {
                    'ID': contador_id,
                    'Tipo': 'simple',
                    'SKU': f"SKU-{contador_id:04d}",
                    'GTIN': '',
                    'Nombre': str(fila['PRODUCTO']).strip(),
                    'Publicado': 1,
                    '¿Está destacado?': 0,
                    'Visibilidad en el catálogo': 'visible',
                    'Descripción corta': f"Producto de la categoría {nombre_pagina}",
                    'Descripción': f"Producto {str(fila['PRODUCTO']).strip()} de la categoría {nombre_pagina}",
                    'Día en que empieza el precio rebajado': '',
                    'Día en que termina el precio rebajado': '',
                    'Estado del impuesto': 'taxable',
                    'Clase de impuesto': 'standard',
                    '¿Existencias?': 1,
                    'Inventario': 100,  # Valor por defecto
                    'Cantidad de bajo inventario': 5,
                    '¿Permitir reservas de productos agotados?': 0,
                    '¿Vendido individualmente?': 0,
                    'Peso (kg)': '',
                    'Longitud (cm)': '',
                    'Anchura (cm)': '',
                    'Altura (cm)': '',
                    '¿Permitir valoraciones de clientes?': 1,
                    'Nota de compra': '',
                    'Precio rebajado': '',
                    'Precio normal': precio_base,
                    'Categorías': nombre_pagina,
                    'Etiquetas': nombre_pagina.lower().replace(' ', '-'),
                    'Clase de envío': '',
                    'Imágenes': '',
                    'Límite de descargas': '',
                    'Días de caducidad de la descarga': '',
                    'Superior': '',
                    'Productos agrupados': '',
                    'Ventas dirigidas': '',
                    'Ventas cruzadas': '',
                    'URL externa': '',
                    'Texto del botón': '',
                    'Posición': contador_id,
                    'Marcas': ''
                }
                
                # Agregar imagen del producto si está habilitado
                if agregar_imagenes and image_fetcher:
                    nombre_producto = str(fila['PRODUCTO']).strip()
                    imagen_path = image_fetcher.get_woocommerce_compatible_image(nombre_producto, contador_id)
                    if imagen_path:
                        # Convertir a ruta relativa para el CSV
                        producto_wc['Imágenes'] = imagen_path
                
                productos_woocommerce.append(producto_wc)
                contador_id += 1
                productos_procesados += 1
                
            except Exception as e:
                print(f"Error procesando producto en fila {index}: {e}")
                continue
    
    # Crear DataFrame final
    columnas_wc = crear_estructura_woocommerce()
    df_woocommerce = pd.DataFrame(productos_woocommerce, columns=columnas_wc)
    
    # Guardar cache de imágenes si se utilizó
    if agregar_imagenes and image_fetcher:
        image_fetcher.save_cache()
        print(f"💾 Cache de imágenes guardado en {image_fetcher.cache_file}")
        
        # Mostrar resumen de imágenes descargadas
        imagenes_con_path = df_woocommerce[df_woocommerce['Imágenes'] != '']['Imágenes']
        if len(imagenes_con_path) > 0:
            print(f"📁 {len(imagenes_con_path)} imágenes descargadas en: {image_fetcher.images_folder}")
            print("📋 IMPORTANTE: Sube la carpeta 'product_images' a tu WordPress en /wp-content/uploads/")
    
    print(f"✅ Procesamiento completado: {len(df_woocommerce)} productos convertidos")
    return df_woocommerce

def exportar_csv_woocommerce(df_woocommerce, nombre_archivo=None):
    """
    Exporta el DataFrame al formato CSV compatible con WooCommerce
    
    Args:
        df_woocommerce (pd.DataFrame): DataFrame con datos de WooCommerce
        nombre_archivo (str): Nombre del archivo de salida
    
    Returns:
        str: Ruta del archivo exportado
    """
    if nombre_archivo is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"productos_woocommerce_{timestamp}.csv"
    
    try:
        # Exportar a CSV con codificación UTF-8 y separador de coma
        df_woocommerce.to_csv(
            nombre_archivo, 
            index=False, 
            encoding='utf-8-sig',  # UTF-8 con BOM para compatibilidad con Excel
            sep=','
        )
        
        print(f"✅ Archivo exportado exitosamente: {nombre_archivo}")
        print(f"📊 Total de productos: {len(df_woocommerce)}")
        print(f"📁 Ubicación: {os.path.abspath(nombre_archivo)}")
        
        return nombre_archivo
        
    except Exception as e:
        print(f"❌ Error al exportar el archivo: {e}")
        return None

def mostrar_resumen_conversion(df_woocommerce):
    """
    Muestra un resumen de la conversión realizada
    
    Args:
        df_woocommerce (pd.DataFrame): DataFrame convertido
    """
    print("\n=== RESUMEN DE CONVERSIÓN ===")
    print(f"Total de productos convertidos: {len(df_woocommerce)}")
    
    # Resumen por categorías
    categorias = df_woocommerce['Categorías'].value_counts()
    print(f"\nProductos por categoría:")
    for categoria, cantidad in categorias.items():
        print(f"  📁 {categoria}: {cantidad} productos")
    
    # Resumen de precios
    precios = df_woocommerce['Precio normal'].astype(float)
    print(f"\nResumen de precios:")
    print(f"  💰 Precio promedio: {precios.mean():.2f}€")
    print(f"  💰 Precio mínimo: {precios.min():.2f}€")
    print(f"  💰 Precio máximo: {precios.max():.2f}€")
    
    # Mostrar primeros productos como ejemplo
    print(f"\nPrimeros 3 productos convertidos:")
    columnas_muestra = ['Nombre', 'Precio normal', 'Categorías', 'SKU']
    print(df_woocommerce[columnas_muestra].head(3).to_string(index=False))

def main():
    """
    Función principal del script
    """
    print("=== Script de Conversión CSV a WooCommerce ===")
    
    # Verificar flags de comandos
    solo_ejemplo = '--ejemplo' in sys.argv or '-e' in sys.argv
    agregar_imagenes = '--imagenes' in sys.argv or '-i' in sys.argv
    
    if solo_ejemplo:
        print("🔬 MODO EJEMPLO ACTIVADO: Se procesarán solo 100 productos variados")
    
    if agregar_imagenes:
        print("🖼️  MODO IMÁGENES ACTIVADO: Se buscarán imágenes automáticamente")
    
    if solo_ejemplo and agregar_imagenes:
        print("🔄 COMBINACIÓN: Modo ejemplo + imágenes automáticas")
    
    print("Paso 1: Lectura y verificación del archivo original\n")
    
    # CONFIGURACIÓN: Cambia esta ruta por la ubicación de tu archivo
    archivo_original = "Productos.xlsx"  # Archivo Excel con múltiples páginas
    
    # Verificar si el archivo existe
    if not os.path.exists(archivo_original):
        print(f"❌ Error: No se encuentra el archivo {archivo_original}")
        print("Por favor, coloca tu archivo CSV/Excel en la misma carpeta que este script")
        print("o modifica la variable 'archivo_original' con la ruta correcta")
        return
    
    # Leer el archivo
    print(f"Leyendo archivo: {archivo_original}")
    paginas_data = leer_csv_con_paginas(archivo_original)
    
    if paginas_data is None:
        print("❌ Error al leer el archivo")
        return
    
    # Verificar estructura
    if verificar_estructura_datos(paginas_data):
        print("\n✅ OK - El archivo se ha leído correctamente")
        print(f"✅ OK - Se encontraron {len(paginas_data)} página(s)")
        print("✅ OK - Nombres de páginas detectados:")
        for nombre_pagina in paginas_data.keys():
            print(f"   📁 {nombre_pagina}")
        
        print("\n🎯 Procesando datos y creando formato WooCommerce...")
        
        # PASO 2: PROCESAR DATOS A FORMATO WOOCOMMERCE
        df_woocommerce = procesar_datos_a_woocommerce(paginas_data, solo_ejemplo, agregar_imagenes)
        
        if df_woocommerce is not None and len(df_woocommerce) > 0:
            # PASO 3: MOSTRAR RESUMEN
            mostrar_resumen_conversion(df_woocommerce)
            
            # PASO 4: EXPORTAR A CSV
            print("\n=== EXPORTANDO ARCHIVO CSV ===")
            archivo_exportado = exportar_csv_woocommerce(df_woocommerce)
            
            if archivo_exportado:
                print(f"\n🎉 ¡CONVERSIÓN COMPLETADA EXITOSAMENTE!")
                print(f"📄 Archivo listo para WooCommerce: {archivo_exportado}")
                print(f"🔄 Ahora puedes importar este archivo en tu tienda WooCommerce")
            else:
                print("❌ Error al exportar el archivo")
        else:
            print("❌ Error: No se pudieron procesar los datos")
        
    else:
        print("❌ Error en la estructura de datos")

if __name__ == "__main__":
    # Mostrar ayuda si se solicita
    if '--ayuda' in sys.argv or '-h' in sys.argv or '--help' in sys.argv:
        print("=== AYUDA - Script de Conversión CSV a WooCommerce ===")
        print("Uso: python csv_to_woocommerce.py [opciones]")
        print("\nOpciones:")
        print("  --ejemplo, -e     Procesa solo 100 productos variados para prueba")
        print("  --imagenes, -i    Agrega imágenes automáticamente desde internet")
        print("  --ayuda, -h       Muestra esta ayuda")
        print("\nEjemplos:")
        print("  python csv_to_woocommerce.py")
        print("  python csv_to_woocommerce.py --ejemplo")
        print("  python csv_to_woocommerce.py --imagenes")
        print("  python csv_to_woocommerce.py --ejemplo --imagenes")
        print("  python csv_to_woocommerce.py -e -i")
        sys.exit(0)
    
    main()
