import os
import re

# dir_path = os.path.dirname(__file__)
# print(dir_path)
dir_path = './'
pattern = re.compile('"imagePath": "(.+?png)",')
for file in os.listdir(dir_path):
    if os.path.splitext(file)[-1] != '.json':
        continue
    with open(os.path.join(dir_path, file), encoding='utf-8') as f:
        content = f.read()
        imagePath = pattern.findall(content)[0]
        print('imagePath ',imagePath)
        new_content = content.replace(imagePath, os.path.splitext(file)[0]+'.png')
    with open(os.path.join(dir_path, file), 'w', encoding='utf-8') as nf:
        nf.write(new_content)

