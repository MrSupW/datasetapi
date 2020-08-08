import os
import re

CLASS_NAMES = ['CA001', 'CA002', 'CA003', 'CA004',
               'CD001', 'CD002', 'CD003', 'CD004',
               'CD005', 'CD006',
               'ZA001', 'ZA002', 'ZA003', 'ZA004',
               'ZA005', 'ZA006',
               'ZB001', 'ZB002', 'ZB003', 'ZB004',
               'ZB005', 'ZB006', 'ZB007', 'ZB008',
               'ZB009', 'ZB010',
               'ZC001', 'ZC002', 'ZC003', 'ZC004',
               'ZC005', 'ZC006', 'ZC007', 'ZC008',
               'ZC009', 'ZC010', 'ZC011', 'ZC012',
               'ZC013', 'ZC014', 'ZC015', 'ZC016',
               'ZC017', 'ZC018', 'ZC019', 'ZC020',
               'ZC021', 'ZC022', 'ZC023'
               ]
CLASS_REAL_NAMES = ['draw_paper', 'roll_paper', 'toothbrush', 'tape',
                    'apple', 'pear', 'melon', 'kiwi',
                    'grapefruit', 'banana',
                    'soap', 'fulid', 'toothpaste', 'flower',
                    'duck', 'pencilbox',
                    'porridge', 'godmother', 'cookie', 'powder',
                    'gum', 'noodle', 'biscuit', 'chips',
                    'fries', 'seeds',
                    'sprite', 'cola', 'fenta', 'redbull',
                    'ADCaMilk', 'juice', 'WLJ', 'JDB',
                    'ice_tea', 'green_tea', 'Sydney', 'tea_pi',
                    'coco', 'NF_Spring', 'wahaha', 'ganten',
                    'c\'est_bon', 'hengda', 'master', 'JML', 'KLS',
                    'QCYH', 'ICE'
                    ]
CLASS_NAME_DICT = {
    'CA001': 'draw_paper',
    'CA002': 'roll_paper',
    'CA003': 'toothbrush',
    'CA004': 'tape',
    'CD001': 'apple',
    'CD002': 'pear',
    'CD003': 'melon',
    'CD004': 'kiwi',
    'CD005': 'grapefruit',
    'CD006': 'banana',
    'ZA001': 'soap',
    'ZA002': 'fulid',
    'ZA003': 'toothpaste',
    'ZA004': 'flower',
    'ZA005': 'duck',
    'ZA006': 'pencilbox',
    'ZB001': 'porridge',
    'ZB002': 'godmother',
    'ZB003': 'cookie',
    'ZB004': 'powder',
    'ZB005': 'gum',
    'ZB006': 'noodle',
    'ZB007': 'biscuit',
    'ZB008': 'chips',
    'ZB009': 'fries',
    'ZB010': 'seeds',
    'ZC001': 'sprite',
    'ZC002': 'cola',
    'ZC003': 'fenta',
    'ZC004': 'redbull',
    'ZC005': 'ADCaMilk',
    'ZC006': 'juice',
    'ZC007': 'WLJ',
    'ZC008': 'JDB',
    'ZC009': 'ice_tea',
    'ZC010': 'green_tea',
    'ZC011': 'Sydney',
    'ZC012': 'tea_pi',
    'ZC013': 'coco',
    'ZC014': 'NF_Spring',
    'ZC015': 'wahaha',
    'ZC016': 'ganten',
    'ZC017': 'c\'est_bon',
    'ZC018': 'hengda',
    'ZC019': 'master',
    'ZC020': 'JML',
    'ZC021': 'KLS',
    'ZC022': 'QCYH',
    'ZC023': 'ICE'
}

dir_path = './'
pattern = re.compile('"label": "([A-Z]{2}[0-9]{3}(?:.+)?)",')
class_ids = []
for file in os.listdir(dir_path):
    if os.path.splitext(file)[-1] != '.json':
        continue
    with open(os.path.join(dir_path, file), 'r+', encoding='utf-8') as f:
        content = f.read()
        image_class_ids = pattern.findall(content)
        for id in image_class_ids:
            if id not in class_ids:
                if len(id) > 5:
                    print("Find invalid id !!")
                    content = content.replace(id, id[:5])
                    with open(os.path.join(dir_path, file), 'w', encoding='utf-8') as f:
                        f.write(content)
                else:
                    class_ids.append(id)
print('一共有{}种class'.format(len(class_ids)))
print('分别是')
index = 1
for id in class_ids:
    print('"{}",'.format(id), end="")
    index += 1
print()
index = 1
for id in class_ids:
    print('"{}":{},'.format(id, index))
    index += 1

for id in class_ids:
    print("'{}',".format(CLASS_NAME_DICT[id]),end="")



