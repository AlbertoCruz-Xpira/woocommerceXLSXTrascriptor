#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para transformar CSV de inventario al formato WooCommerce
Convierte archivo CSV con múltiples páginas a formato compatible con WooCommerce
"""

import pandas as pd
import sys
import os
from datetime import datetime

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

def procesar_datos_a_woocommerce(paginas_data):
    """
    Convierte los datos del inventario al formato WooCommerce
    
    Args:
        paginas_data (dict): Datos de las páginas del archivo original
    
    Returns:
        pd.DataFrame: DataFrame con formato WooCommerce
    """
    print("\n=== Procesando datos a formato WooCommerce ===")
    
    # Crear lista para almacenar todos los productos
    productos_woocommerce = []
    contador_id = 1
    
    for nombre_pagina, df in paginas_data.items():
        print(f"Procesando página: {nombre_pagina} ({len(df)} productos)")
        
        # Limpiar datos: eliminar filas vacías
        df_limpio = df.dropna(subset=['PRODUCTO'])
        
        for index, fila in df_limpio.iterrows():
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
                
                productos_woocommerce.append(producto_wc)
                contador_id += 1
                
            except Exception as e:
                print(f"Error procesando producto en fila {index}: {e}")
                continue
    
    # Crear DataFrame final
    columnas_wc = crear_estructura_woocommerce()
    df_woocommerce = pd.DataFrame(productos_woocommerce, columns=columnas_wc)
    
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
        df_woocommerce = procesar_datos_a_woocommerce(paginas_data)
        
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
    main()
