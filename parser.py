import json
import os

content = []
for path, subdirs, files in os.walk('json_files'):
    for filename in files:
        with open('json_files\\' + filename, 'r') as file:
            f = json.loads(file.read())
            for line in f:
                content.append(line['content'])

with open('korpus_finansowy.txt', 'w', encoding='utf-8') as file:
	for c in content:
		file.write(c)