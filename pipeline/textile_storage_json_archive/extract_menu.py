import json

with open('jaypore_home.html', encoding='utf-8') as f:
    t = f.read()

idx = t.find('menuData')
brace_start = idx + len('menuData') + 3

depth = 0
i = brace_start
n = len(t)
in_str = False
BACKSLASH = chr(92)
QUOTE = chr(34)
while i < n:
    c = t[i]
    if c == BACKSLASH and i + 1 < n:
        i += 2
        continue
    if c == QUOTE:
        in_str = not in_str
        i += 1
        continue
    if not in_str:
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                i += 1
                break
    i += 1

raw = t[brace_start:i]
print('length', len(raw))

# Unescape: this text has backslash-escaped quotes (\" -> ") and backslash-escaped backslashes.
# It's JSON embedded as a JS string literal value, so standard JSON string unescaping applies.
# Wrap it as a JSON string and let json.loads do the unescaping.
wrapped = '"' + raw.replace(chr(92)+chr(92), '\x00BSLASH\x00') + '"'
# Actually simplest: treat raw as content of a JSON string (without outer quotes) and decode via json.loads on '"'+raw+'"'
try:
    unescaped = json.loads('"' + raw + '"')
except Exception as e:
    print('unescape error', e)
    unescaped = None

if unescaped:
    with open('menudata_raw.json', 'w', encoding='utf-8') as f:
        f.write(unescaped)
    data = json.loads(unescaped)
    print('parsed OK, results count', len(data.get('results', [])))
    with open('menudata_parsed.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
