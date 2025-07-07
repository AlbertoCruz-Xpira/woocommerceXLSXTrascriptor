#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test simple del nuevo sistema de placeholder
"""

import urllib.parse

def test_simple_placeholder():
    product_name = "PIPA BLANCA"
    
    # Generar color basado en el nombre del producto
    product_hash = abs(hash(product_name))
    color_codes = ['FF6B6B', '4ECDC4', '45B7D1', 'FFA07A', '98D8C8', 'F7DC6F', 'BB8FCE', '85C1E9']
    color = color_codes[product_hash % len(color_codes)]
    
    # Crear texto corto para la imagen
    text = product_name[:8].replace(' ', '+').upper()
    
    # Usar DummyImage.com que es muy estable
    url = f"https://dummyimage.com/400x400/{color}/ffffff&text={text}"
    
    print(f"Producto: {product_name}")
    print(f"URL generada: {url}")
    print(f"Color seleccionado: #{color}")
    print(f"Texto: {text}")

if __name__ == "__main__":
    test_simple_placeholder()
