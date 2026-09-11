import json, sys, os
SP = os.path.dirname(os.path.abspath(__file__))
comps = {c['sr']: c for c in json.load(open(os.path.join(SP,'companies.json')))}
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for sr in range(lo, hi+1):
    c = comps[sr]
    print("=== SR %d ===" % sr)
    print("sr: %d" % sr)
    print('company: %s' % c['name'])
    print('brand_site: %s' % c['brand_site'])
    print('country: %s' % c['country'])
    print('site_url: %s' % c['url'])
    print('output_file: se%d.json' % sr)
    print()
