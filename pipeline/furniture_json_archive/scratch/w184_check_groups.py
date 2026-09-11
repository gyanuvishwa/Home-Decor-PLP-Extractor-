import json
d = json.load(open('scratch/w184_draft.json', encoding='utf-8'))
rows = d['rows']
i = 0
n = len(rows)
zero_count_groups = []
while i < n:
    r = rows[i]
    if r['is_group']:
        j = i + 1
        cnt = 0
        while j < n and not rows[j]['is_group']:
            cnt += 1
            j += 1
        label = r['sub_category']
        print(label + ': ' + str(cnt) + ' immediate leaves')
        if cnt == 0:
            zero_count_groups.append(label)
    i += 1
print('---')
print('groups with zero immediate leaves:', zero_count_groups)
