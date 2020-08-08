import os
import json
import numpy as np
import glob
import shutil
import cv2
from sklearn.model_selection import train_test_split

np.random.seed(41)

# 0为背景
classname_to_id = {
    "CA002": 1,
    "CA004": 2,
    "CA003": 3,
    "CD006": 4,
    "CD002": 5,
    "CD001": 6,
    "ZA001": 7,
    "ZA003": 8,
    "ZA002": 9,
    "ZA005": 10,
    "ZB005": 11,
    "ZA004": 12,
    "ZC009": 13,
    "ZB003": 14,
    "ZB004": 15,
    "ZC012": 16,
    "ZC011": 17,
    "ZC010": 18,
    "ZC023": 19,
    "ZC013": 20,
    "ZC014": 21,
    "ZC007": 22,
    "ZB006": 23,
    "ZC008": 24,
    "ZC002": 25,
    "ZB001": 26,
    "ZC001": 27,
    "CD003": 28,
    "CA001": 29,
}


class Lableme2CoCo:

    def __init__(self):
        self.images = []
        self.annotations = []
        self.categories = []
        self.img_id = 0
        self.ann_id = 0

    def save_coco_json(self, instance, save_path):
        json.dump(instance, open(save_path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)  # indent=2 更加美观显示

    # 由json文件构建COCO
    def to_coco(self, json_path_list):
        self._init_categories()
        for json_path in json_path_list:
            obj = self.read_jsonfile(json_path)
            self.images.append(self._image(obj, json_path))
            shapes = obj['shapes']
            for shape in shapes:
                annotation = self._annotation(shape)
                self.annotations.append(annotation)
                self.ann_id += 1
            self.img_id += 1
        instance = {}
        instance['info'] = 'spytensor created'
        instance['license'] = ['license']
        instance['images'] = self.images
        instance['annotations'] = self.annotations
        instance['categories'] = self.categories
        return instance

    # 构建类别
    def _init_categories(self):
        for k, v in classname_to_id.items():
            category = {}
            category['id'] = v
            category['name'] = k
            self.categories.append(category)

    # 构建COCO的image字段
    def _image(self, obj, path):
        image = {}
        from labelme import utils
        img_x = utils.img_b64_to_arr(obj['imageData'])
        h, w = img_x.shape[:-1]
        image['height'] = h
        image['width'] = w
        image['id'] = self.img_id
        image['file_name'] = os.path.basename(path).replace(".json", ".jpg")
        return image

    # 构建COCO的annotation字段
    def _annotation(self, shape):
        # print('shape', shape)
        label = shape['label']
        points = shape['points']
        annotation = {}
        annotation['id'] = self.ann_id
        annotation['image_id'] = self.img_id
        annotation['category_id'] = int(classname_to_id[label])
        annotation['segmentation'] = [np.asarray(points).flatten().tolist()]
        annotation['bbox'] = self._get_box(points)
        annotation['iscrowd'] = 0
        annotation['area'] = 1.0
        return annotation

    # 读取json文件，返回一个json对象
    def read_jsonfile(self, path):
        with open(path, "r", encoding='utf-8') as f:
            return json.load(f)

    # COCO的格式： [x1,y1,w,h] 对应COCO的bbox格式
    def _get_box(self, points):
        min_x = min_y = np.inf
        max_x = max_y = 0
        for x, y in points:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        return [min_x, min_y, max_x - min_x, max_y - min_y]


if __name__ == '__main__':
    labelme_path = "../../../xianjin_data-3/"
    saved_coco_path = "../../../xianjin_data-3/"
    print('reading...')
    # 创建文件
    if not os.path.exists("%scoco/annotations/" % saved_coco_path):
        os.makedirs("%scoco/annotations/" % saved_coco_path)
    if not os.path.exists("%scoco/images/train2017/" % saved_coco_path):
        os.makedirs("%scoco/images/train2017" % saved_coco_path)
    if not os.path.exists("%scoco/images/val2017/" % saved_coco_path):
        os.makedirs("%scoco/images/val2017" % saved_coco_path)
    # 获取images目录下所有的joson文件列表
    print(labelme_path + "/*.json")
    json_list_path = glob.glob(labelme_path + "/*.json")
    print('json_list_path: ', len(json_list_path))
    # 数据划分,这里没有区分val2017和tran2017目录，所有图片都放在images目录下
    train_path, val_path = train_test_split(json_list_path, test_size=0.1, train_size=0.9)
    print("train_n:", len(train_path), 'val_n:', len(val_path))

    # 把训练集转化为COCO的json格式
    l2c_train = Lableme2CoCo()
    train_instance = l2c_train.to_coco(train_path)
    l2c_train.save_coco_json(train_instance, '%scoco/annotations/instances_train2017.json' % saved_coco_path)
    for file in train_path:
        # shutil.copy(file.replace("json", "jpg"), "%scoco/images/train2017/" % saved_coco_path)
        img_name = file.replace('json', 'png')
        temp_img = cv2.imread(img_name)
        try:
            cv2.imwrite("{}coco/images/train2017/{}".format(saved_coco_path, img_name.replace('png', 'jpg')),temp_img)
        except Exception as e:
            print(e)
            print('Wrong Image:', img_name )
            continue
        print(img_name + '-->', img_name.replace('png', 'jpg'))

    for file in val_path:
        # shutil.copy(file.replace("json", "jpg"), "%scoco/images/val2017/" % saved_coco_path)
        img_name = file.replace('json', 'png')
        temp_img = cv2.imread(img_name)
        try:
            cv2.imwrite("{}coco/images/val2017/{}".format(saved_coco_path, img_name.replace('png', 'jpg')), temp_img)
        except Exception as e:
            print(e)
            print('Wrong Image:', img_name)
            continue
        print(img_name + '-->', img_name.replace('png', 'jpg'))

    # 把验证集转化为COCO的json格式
    l2c_val = Lableme2CoCo()
    val_instance = l2c_val.to_coco(val_path)
    l2c_val.save_coco_json(val_instance, '%scoco/annotations/instances_val2017.json' % saved_coco_path)

