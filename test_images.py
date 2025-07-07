#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test de conectividad para APIs de imágenes
"""

import requests
import urllib.parse

def test_image_apis():
    print('🧪 Test de conectividad a APIs de imágenes:')
    
    try:
        # Test 1: Unsplash Source
        print('\n1. Probando Unsplash Source...')
        url1 = 'https://source.unsplash.com/400x400/?food'
        response1 = requests.get(url1, timeout=10)
        print(f'   Status: {response1.status_code}')
        print(f'   Content-Type: {response1.headers.get("content-type", "N/A")}')
        print(f'   URL final: {response1.url}')
        
        # Test 2: Picsum
        print('\n2. Probando Lorem Picsum...')
        url2 = 'https://picsum.photos/400/400?random=123'
        response2 = requests.head(url2, timeout=10)
        print(f'   Status: {response2.status_code}')
        
        # Test 3: Placeholder
        print('\n3. Probando Via Placeholder...')
        url3 = 'https://via.placeholder.com/400x400/ff0000/ffffff?text=Test'
        response3 = requests.head(url3, timeout=10)
        print(f'   Status: {response3.status_code}')
        
        print('\n✅ Tests completados')
        
    except Exception as e:
        print(f'❌ Error: {e}')

if __name__ == "__main__":
    test_image_apis()
