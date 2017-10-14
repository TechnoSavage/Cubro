import requests, json


response = requests.get('http://10.90.100.244/rest/groups/all?', auth=('admin', 'cubro'))
r = response.content
data = json.loads(r)
active_groups = json.dumps(data, indent=4)
json_groups = json.loads(active_groups)
existing = []
count = 0
# for group in json_groups['groups']:
#     existing.append(json_groups['groups'][group]['group_id'])
#     count +=1
for item in json_groups['groups']:
    for attrib in item:
        if attrib == 'group_id':
            existing.append(json_groups['groups'][item][attrib][0])
print existing
