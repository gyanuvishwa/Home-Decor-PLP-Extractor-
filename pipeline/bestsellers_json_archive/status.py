import os, json, glob, re, sys
SP = os.path.dirname(os.path.abspath(__file__))
disp = set(int(x) for x in open(os.path.join(SP,'dispatched.txt')) if x.strip())
done = set()
for f in glob.glob(os.path.join(SP,'bs*.json')):
    m = re.match(r'^bs(\d+)\.json$', os.path.basename(f))
    if m: done.add(int(m.group(1)))
running = sorted(disp - done)
todo = [s for s in range(1,287) if s not in disp]
print('dispatched %d | done %d | in-flight %d | not yet dispatched %d' % (len(disp), len(done), len(running), len(todo)))
print('in-flight:', running)
print('next up  :', todo[:30])
