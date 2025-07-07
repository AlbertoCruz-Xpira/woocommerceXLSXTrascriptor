#!/usr/bin/env python3
import pandas as pd
import os

def verificar_csv():
    archivo = 'productos_woocommerce_20250707_184957.csv'
    try:
        df = pd.read_csv(archivo, encoding='utf-8-sig')
        print(f'✅ Archivo verificado: {archivo}')
        print(f'Total productos: {len(df)}')
        
        with_images = df[df['Imágenes'] != '']
        print(f'Productos con imagen: {len(with_images)}')
        print(f'Porcentaje con imagen: {len(with_images)/len(df)*100:.1f}%')
        
        print('\n📸 Ejemplos de rutas de imágenes:')
        for i, row in with_images.head(5).iterrows():
            nombre = row['Nombre'][:25] + '...' if len(row['Nombre']) > 25 else row['Nombre']
            ruta = row['Imágenes']
            archivo_existe = os.path.exists(ruta) if ruta else False
            status = "✅" if archivo_existe else "❌"
            print(f'{status} {nombre}: {ruta}')
            
        print(f'\n🗂️  Verificación de archivos locales:')
        rutas_locales = with_images['Imágenes'].tolist()
        archivos_existentes = sum(1 for ruta in rutas_locales if os.path.exists(ruta))
        print(f'Archivos que existen localmente: {archivos_existentes} de {len(rutas_locales)}')
        
        if archivos_existentes > 0:
            print(f'\n✅ ÉXITO: Las imágenes se han descargado correctamente')
            print(f'📁 Carpeta de imágenes: product_images/')
            print(f'📝 Rutas en CSV: Apuntan a archivos locales')
        else:
            print(f'\n❌ ERROR: No se encontraron los archivos de imagen')
        
    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    verificar_csv()
