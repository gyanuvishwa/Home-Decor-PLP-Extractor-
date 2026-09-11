import re, json, sys

def extract_balanced(text, start_idx):
    open_ch = text[start_idx]
    close_ch = ']' if open_ch == '[' else '}'
    depth = 0
    i = start_idx
    in_str = False
    esc = False
    while i < len(text):
        c = text[i]
        if in_str:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                in_str = False
        else:
            if c == '"':
                in_str = True
            elif c == open_ch:
                depth += 1
            elif c == close_ch:
                depth -= 1
                if depth == 0:
                    return text[start_idx:i+1]
        i += 1
    raise ValueError('no matching close bracket found')

def jsify(s):
    s = re.sub(r'\$R\[\d+\]=', '', s)
    s = re.sub(r'([{,\[])(\s*)([A-Za-z_][A-Za-z0-9_]*):', r'\1\2"\3":', s)
    s = re.sub(r',(\s*[\]}])', r'\1', s)
    return s

def main():
    infile = sys.argv[1]
    outfile = sys.argv[2]
    html = open(infile, encoding='utf-8').read()
    idx = html.find('code:"category"')
    if idx == -1:
        print('category facet not found')
        return
    idx_data = html.find('data:', idx)
    idx_eq = html.find('=', idx_data)
    idx_bracket = html.find('[', idx_eq)
    raw = extract_balanced(html, idx_bracket)
    js = jsify(raw)
    try:
        tree = json.loads(js)
        print('PARSED OK, top-level nodes:', len(tree))
        with open(outfile, 'w', encoding='utf-8') as f:
            json.dump(tree, f, indent=1)
    except Exception as e:
        print('FAIL', e)
        with open(outfile + '.raw.txt', 'w', encoding='utf-8') as f:
            f.write(js)

if __name__ == '__main__':
    main()
