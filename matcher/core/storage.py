import h5py
import numpy as np
import cv2
import os

# 读取 HDF5 文件
with h5py.File('matcher/features.h5', 'r') as f:
    # 读取关键点数据
    kp_data = f['keypoints'][:]
    keypoints = []

    # 解析关键点数据
    for pt, size, angle, response, octave, class_id in kp_data:
        kp = cv2.KeyPoint(x=pt[0], y=pt[1], size=size, angle=angle, response=response, octave=octave, class_id=class_id)
        keypoints.append(kp)

    # 读取描述子数据
    des = f['descriptors'][:]

# 打印关键点数据和描述子数据的形状
print("Keypoints shape:", len(keypoints))
print("Descriptors shape:", des.shape)

# 打印前几个关键点和描述子的值
print("First few keypoints:", keypoints[:5])
print("First few descriptors:", des[:5])

class ImageDataSet:
    def __init__(self, folder_path, dataset_name):
        _path = os.path.dirname(os.path.abspath(__file__))
        self.folder_path = os.path.join(_path, "../..", folder_path)

        self.dataset_name = dataset_name
        self.sift = cv2.SIFT_create()


    def create_dataset(self):
        with h5py.File(self.dataset_name, 'w') as f:
            for filename in os.listdir(self.folder_path):
                if filename.endswith('.jpg') or filename.endswith('.png'):
                    image_path = os.path.join(self.folder_path, filename)
                    self.fetch_image(image_path)

    def read_image(self, image_name):
        with h5py.File(self.dataset_name, 'r') as f:
            if image_name in f:
                image_data = f[image_name][:]
                return image_data
            else:
                print(f"Image {image_name} not found in the dataset.")

    def fetch_image(self, image_path):
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        kp, des = self.sift.detectAndCompute(image, None)

        with h5py.File('matcher/features.h5', 'w') as f:
            group = f.create_group(image_path)

            kp_data = np.array([(kp[i].pt, kp[i].size, kp[i].angle, kp[i].response, kp[i].octave, kp[i].class_id) for i in range(len(kp))], dtype=[('pt', 'f4', 2), ('size', 'f4'), ('angle', 'f4'), ('response', 'f4'), ('octave', 'i4'), ('class_id', 'i4')])
            group.create_dataset('keypoints', data=kp_data)
            group.create_dataset('descriptors', data=des)

# TODO: 1. Create a new instance of the ImageDataSet class
#       2. Call the create_dataset method on the instance
#       3. Call the read_image method on the instance
#       4. Print the returned image data
#       5. Call the fetch_image method on the instance
        