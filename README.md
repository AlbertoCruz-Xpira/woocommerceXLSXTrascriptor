# 🛒 Script de Conversión CSV a WooCommerce

Script en Python para transformar archivos CSV/Excel de inventario al formato compatible con WooCommerce.

## 📋 Descripción

Este script convierte archivos Excel con múltiples páginas (categorías) de productos a un formato CSV listo para importar en WooCommerce. Procesa automáticamente los precios, calcula el precio base dividiendo el total por 1.03, y asigna categorías basadas en los nombres de las páginas del archivo Excel.

## 🚀 Características

- ✅ **Lectura automática** de archivos Excel con múltiples hojas
- ✅ **Conversión de precios** automática (TOTAL ÷ 1.03)
- ✅ **Mapeo completo** a formato WooCommerce
- ✅ **Generación de SKUs** únicos automáticos
- ✅ **Categorización** basada en nombres de páginas
- ✅ **Modo ejemplo** para pruebas con 100 productos
- ✅ **Imágenes automáticas** desde APIs gratuitas de internet
- ✅ **Manejo de errores** robusto para datos inconsistentes

## 📦 Requisitos

```bash
pip install pandas openpyxl requests
```

## 📁 Estructura de Archivos

```
nk2connector/
├── csv_to_woocommerce.py    # Script principal
├── Productos.xlsx           # Archivo Excel de origen (tu archivo)
├── productos_woocommerce_*.csv  # Archivos CSV generados
└── README.md               # Este archivo
```

## 🔧 Instalación

1. **Clona o descarga** los archivos del script
2. **Instala las dependencias**:
   ```bash
   pip install pandas openpyxl requests
   ```
3. **Coloca tu archivo Excel** (`Productos.xlsx`) en la misma carpeta
4. **Ejecuta el script**

## 💻 Uso

### Comando Básico
```bash
python csv_to_woocommerce.py
```
Procesa todos los productos del archivo Excel y genera un CSV completo.

### Modo Ejemplo (Recomendado para pruebas)
```bash
python csv_to_woocommerce.py --ejemplo
```
o
```bash
python csv_to_woocommerce.py -e
```
Procesa solo **100 productos variados** de diferentes categorías para pruebas.

### Modo con Imágenes Automáticas
```bash
python csv_to_woocommerce.py --imagenes
```
o
```bash
python csv_to_woocommerce.py -i
```
Busca automáticamente **imágenes de internet** para cada producto y las agrega al CSV.

### Combinación de Modos
```bash
python csv_to_woocommerce.py --ejemplo --imagenes
```
o
```bash
python csv_to_woocommerce.py -e -i
```
Procesa **100 productos con imágenes automáticas** - ideal para pruebas completas.

### Ayuda
```bash
python csv_to_woocommerce.py --ayuda
```
o
```bash
python csv_to_woocommerce.py -h
```
Muestra información de ayuda y opciones disponibles.

## 🏷️ Flags Disponibles

| Flag | Descripción | Ejemplo |
|------|-------------|---------|
| `--ejemplo`, `-e` | Procesa solo 100 productos variados para prueba | `python csv_to_woocommerce.py -e` |
| `--imagenes`, `-i` | Agrega imágenes automáticamente desde internet | `python csv_to_woocommerce.py -i` |
| `--ayuda`, `-h` | Muestra la ayuda del comando | `python csv_to_woocommerce.py -h` |

### 🔄 Combinaciones de Flags

Los flags se pueden combinar para mayor funcionalidad:

```bash
# Ejemplo + Imágenes (recomendado para primera prueba)
python csv_to_woocommerce.py --ejemplo --imagenes
python csv_to_woocommerce.py -e -i
```

## 📊 Formato del Archivo de Entrada

El archivo Excel debe tener:

### Estructura por Página/Hoja:
- **Nombre de la página** = Categoría del producto
- **Columnas requeridas**:
  - `PRODUCTO`: Nombre del producto
  - `PRECIO`: Precio base (opcional)
  - `0.3`: Columna de impuesto (puede ser numérica)
  - `TOTAL`: Precio total con impuesto

### Ejemplo de Estructura:
```
Página: "PAPAS MATUTANO"
| PRODUCTO           | PRECIO | 0.3  | TOTAL   |
|--------------------|--------|------|---------|
| BITS DORITOS       | 1.25   | 0.375| 1.63 €  |
| PISTACHOS HORNO    | 2.70   | 0.81 | 3.51 €  |
```

## 📤 Formato de Salida WooCommerce

El CSV generado incluye todas las columnas requeridas por WooCommerce:

- `ID`, `Tipo`, `SKU`, `GTIN`, `Nombre`
- `Publicado`, `¿Está destacado?`, `Visibilidad en el catálogo`
- `Descripción corta`, `Descripción`
- `Precio normal`, `Categorías`, `Etiquetas`
- `Estado del impuesto`, `Clase de impuesto`
- `¿Existencias?`, `Inventario`
- Y muchas más...

## 🎯 Casos de Uso

### 1. Primera Importación (Modo Ejemplo)
```bash
# Genera 100 productos para probar la importación
python csv_to_woocommerce.py --ejemplo
```
**Uso**: Prueba inicial en WooCommerce antes de importar todo el inventario.

### 2. Primera Importación con Imágenes (Recomendado)
```bash
# Genera 100 productos CON imágenes automáticas
python csv_to_woocommerce.py --ejemplo --imagenes
```
**Uso**: Prueba inicial completa con imágenes para ver cómo queda la tienda.

### 3. Importación Completa
```bash
# Procesa todos los productos del inventario
python csv_to_woocommerce.py
```
**Uso**: Importación completa del inventario a la tienda.

### 4. Importación Completa con Imágenes
```bash
# Procesa todos los productos CON imágenes automáticas
python csv_to_woocommerce.py --imagenes
```
**Uso**: Importación completa del inventario con imágenes automáticas.

### 5. Actualización de Inventario
```bash
# Actualiza el archivo Excel y vuelve a ejecutar
python csv_to_woocommerce.py
```
**Uso**: Actualización periódica del catálogo de productos.

## 📋 Ejemplo de Ejecución

```bash
PS D:\Proyectos> python csv_to_woocommerce.py --ejemplo --imagenes

=== Script de Conversión CSV a WooCommerce ===
🔬 MODO EJEMPLO ACTIVADO: Se procesarán solo 100 productos variados
🖼️  MODO IMÁGENES ACTIVADO: Se buscarán imágenes automáticamente
🔄 COMBINACIÓN: Modo ejemplo + imágenes automáticas
Paso 1: Lectura y verificación del archivo original

Leyendo archivo: Productos.xlsx
Detectado archivo Excel, leyendo todas las hojas...
Leyendo página: MUEBLE TABACO
Leyendo página: NEVERA MONSTER
[... más páginas ...]

✅ OK - El archivo se ha leído correctamente
✅ OK - Se encontraron 29 página(s)

🎯 Procesando datos y creando formato WooCommerce...
🔬 MODO EJEMPLO: Procesando solo 100 productos variados para prueba
🖼️  MODO IMÁGENES: Agregando imágenes automáticamente a los productos

Procesando página: MUEBLE TABACO (347 productos)
   🔍 Buscando imagen para: PIPA BLANCA
   ✅ Imagen encontrada: https://source.unsplash.com/400x400/?pipa-blanca-product-food-snack
   🔍 Buscando imagen para: MECHERO BIC MINI
   ✅ Imagen encontrada: https://source.unsplash.com/400x400/?mechero-bic-mini-product-food-snack

💾 Cache de imágenes guardado en image_cache.json
✅ Procesamiento completado: 100 productos convertidos

=== RESUMEN DE CONVERSIÓN ===
Total de productos convertidos: 100
Productos por categoría:
  📁 MUEBLE TABACO: 4 productos
  📁 NEVERA MONSTER: 4 productos
  [... más categorías ...]

🎉 ¡CONVERSIÓN COMPLETADA EXITOSAMENTE!
📄 Archivo listo para WooCommerce: productos_woocommerce_20250707_175123.csv
```

## 🖼️ Sistema de Imágenes Automáticas

### Cómo Funciona
El flag `--imagenes` activa la descarga automática de imágenes para cada producto:

1. **Genera placeholders únicos**: Crea imágenes placeholder con colores y texto identificativo
2. **Descarga localmente**: Guarda las imágenes en la carpeta `product_images/`
3. **Prepara para WooCommerce**: Las rutas en el CSV son compatibles con WordPress

### Proceso Completo
```bash
# 1. Generar CSV con imágenes
python csv_to_woocommerce.py --ejemplo --imagenes

# 2. Preparar paquete para WordPress
python prepare_images_for_woocommerce.py

# 3. Subir a WordPress y extraer ZIP en: /wp-content/uploads/
# 4. Importar CSV en WooCommerce
```

### Estructura Generada
```
project/
├── productos_woocommerce_YYYYMMDD_HHMMSS.csv  # CSV para importar
├── product_images/                              # Imágenes descargadas
│   ├── producto-0001-chesterfield-24.jpg
│   ├── producto-0002-carton-chesterfield.jpg
│   └── ...
├── woocommerce_images_YYYYMMDD_HHMMSS.zip     # Paquete para WordPress
└── image_cache.json                            # Cache de imágenes
```

### Ventajas
- ✅ **Compatible con WooCommerce**: No hay problemas de permisos
- ✅ **Imágenes locales**: Se almacenan en tu servidor WordPress
- ✅ **Cache inteligente**: Evita descargar la misma imagen múltiples veces
- ✅ **Proceso automatizado**: Script auxiliar para crear el paquete ZIP

### Configuración en WordPress
1. **Subir imágenes**: Sube el ZIP a `/wp-content/uploads/` y extráelo
2. **Importar CSV**: Las rutas de imágenes serán válidas automáticamente
3. **Resultado**: Productos con imágenes automáticamente asignadas

## ⚠️ Solución de Problemas

### Error: "No se encuentra el archivo Productos.xlsx"
**Solución**: Asegúrate de que el archivo `Productos.xlsx` esté en la misma carpeta que el script.

### Error: "No module named 'pandas'"
**Solución**: Instala las dependencias:
```bash
pip install pandas openpyxl
```

### Precios en 0 o incorrectos
**Causa**: El script detecta valores `#VALUE!` o formatos incorrectos en la columna TOTAL.
**Solución**: Revisa que los datos de precios en Excel estén en formato numérico correcto.

### Productos no procesados
**Causa**: Filas con la columna `PRODUCTO` vacía se omiten automáticamente.
**Solución**: Esto es normal, el script filtra filas vacías automáticamente.

## 📝 Personalización

### Cambiar el nombre del archivo de entrada
Edita la línea 278 en `csv_to_woocommerce.py`:
```python
archivo_original = "TU_ARCHIVO.xlsx"  # Cambia el nombre aquí
```

### Modificar valores por defecto
Edita la sección de `producto_wc` en la función `procesar_datos_a_woocommerce()` para cambiar:
- Inventario por defecto (línea 161): `'Inventario': 100`
- Cantidad de bajo inventario (línea 162): `'Cantidad de bajo inventario': 5`
- Otros campos según necesites

## 🤝 Soporte

Si encuentras problemas:
1. Verifica que el archivo Excel tenga el formato correcto
2. Revisa que las dependencias estén instaladas
3. Ejecuta primero en modo `--ejemplo` para pruebas
4. Revisa los mensajes de error en la consola

## 📄 Licencia

Este script es de uso libre para fines comerciales y personales.

---

**Desarrollado para NK2 Connector - Conversión de Inventario a WooCommerce**
