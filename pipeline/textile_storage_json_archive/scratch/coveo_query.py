import json, sys, time
from curl_cffi import requests

TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJ2OCI6dHJ1ZSwidG9rZW5JZCI6InJ2bGpzenRtZm9obmhwaWJsNzR5d21jZXI0Iiwib3JnYW5pemF0aW9uIjoiZnJlZWRvbWZ1cm5pdHVyZXByb2R1Y3Rpb24xczRubXoyOHUiLCJ1c2VySWRzIjpbeyJ0eXBlIjoiVXNlciIsIm5hbWUiOiJhbm9ueW1vdXMiLCJwcm92aWRlciI6IkVtYWlsIFNlY3VyaXR5IFByb3ZpZGVyIn1dLCJyb2xlcyI6WyJxdWVyeUV4ZWN1dG9yIl0sImlzcyI6IlNlYXJjaEFwaSIsImV4cCI6MTc4NzgxODkyMCwiaWF0IjoxNzg3NzMyNTIwfQ.zSDSo9OuVINKG8vIvrRlq_ih52yinclMpk3ZYZhibWU'
URL = 'https://freedomfurnitureproduction1s4nmz28u.org.coveo.com/rest/organizations/freedomfurnitureproduction1s4nmz28u/commerce/v2/listing'
HEADERS = {
    'authorization': f'Bearer {TOKEN}',
    'content-type': 'application/json',
    'referer': 'https://www.freedom.com.au/'
}

def query(slug, per_page=5):
    payload = {
        'trackingId': 'freedom_au',
        'clientId': '3d8fee66-b0d1-4db5-a2a9-e8271785dcd7',
        'context': {
            'user': {'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
            'view': {'url': f'https://www.freedom.com.au/c/{slug}'},
            'capture': True,
            'cart': [],
            'source': ['@coveo/headless@3.53.0'],
            'dictionaryFieldContext': {'custom_prd_alternatepriceinfo': 'myfreedomcustomergroup', 'ec_images': 'product'}
        },
        'language': 'en', 'country': 'AU', 'currency': 'AUD',
        'page': 0, 'perPage': per_page, 'facets': [],
        'sort': {'sortCriteria': 'relevance'}, 'enableResults': True
    }
    r = requests.post(URL, json=payload, headers=HEADERS, impersonate='chrome', timeout=20)
    if r.status_code != 200:
        return {'slug': slug, 'error': f'HTTP {r.status_code}'}
    data = r.json()
    pag = data.get('pagination', {})
    results = data.get('results', [])
    names = []
    taxonomy = None
    for p in results[:per_page]:
        n = p.get('ec_name')
        names.append(n)
        if taxonomy is None:
            taxonomy = p.get('additionalFields', {}).get('custom_prd_taxonomy')
    return {
        'slug': slug,
        'total': pag.get('totalProducts'),
        'sample': names,
        'taxonomy': taxonomy
    }

if __name__ == '__main__':
    slugs = sys.argv[1:]
    results = []
    for s in slugs:
        res = query(s)
        results.append(res)
        print(json.dumps(res, ensure_ascii=False))
        time.sleep(0.3)
