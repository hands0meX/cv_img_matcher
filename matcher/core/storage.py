import h5py
import numpy as np
import cv2
import os
from tqdm import tqdm

class ImageDataSet:
    def __init__(self, fetch_folder_name, force_update=False):
        if not os.path.exists(fetch_folder_name):
            print(f"Folder {fetch_folder_name} not found.")
            return

        _path = os.path.dirname(os.path.abspath(__file__))
        self.fetch_folder_path = os.path.join(_path, "../..", fetch_folder_name)
        self.save_folder_path = os.path.join(_path, "../..", "matcher")

        self.dataset_name = fetch_folder_name
        self.sift = cv2.SIFT_create()
        if (not os.path.exists(f'{self.save_folder_path}/{self.dataset_name}.h5')) or force_update:
            self.__create_dataset__()
            self.save_all()
        else:
            self.__create_dataset__()

    def __create_dataset__(self):
        self.waiting_list = []
        for filename in os.listdir(self.fetch_folder_path):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(self.fetch_folder_path, filename)
                # print(image_path, filename, self.dataset_name)
                self.waiting_list.append((image_path, filename.split('.')[0]))

    def read(self, image_name):
        """ Read keypoints and descriptors from the dataset with image_name."""
        with h5py.File(f'{self.save_folder_path}/{self.dataset_name}.h5', 'r') as f:
            if image_name in f:
                image_data = f[image_name]
                keypoints = []
                for pt, size, angle, response, octave, class_id in image_data['keypoints'][:]:
                    kp = cv2.KeyPoint(x=pt[0], y=pt[1], size=size, angle=angle, response=response, octave=octave, class_id=class_id)
                    keypoints.append(kp)
                print(len(keypoints), len(image_data['descriptors'][:]))
                return (image_name, (keypoints, image_data['descriptors'][:]))
            else:
                print(f"Image {image_name} not found in the dataset.")
                return (image_name, (None, None))

    def read_all(self):
        """ Read all keypoints and descriptors from the dataset. """
        return [self.read(image_name) for _, image_name in self.waiting_list]

    def save_all(self):
        """ Extract features from images and save to HDF5 file. """
        if len(self.waiting_list) == 0:
            print("No image to fetch.")
            return

        with h5py.File(f'{self.save_folder_path}/{self.dataset_name}.h5', 'w') as f:
                for image_path, filename in tqdm(self.waiting_list, desc=f"Extracting features from {self.dataset_name}...", total=len(self.waiting_list)):
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                    kp, des = self.sift.detectAndCompute(image, None)
                    group = f.create_group(filename)
                    print(f"Group {filename} created.")

                    kp_data = np.array([(kp[i].pt, kp[i].size, kp[i].angle, kp[i].response, kp[i].octave, kp[i].class_id) for i in range(len(kp))], dtype=[('pt', 'f4', 2), ('size', 'f4'), ('angle', 'f4'), ('response', 'f4'), ('octave', 'i4'), ('class_id', 'i4')])
                    group.create_dataset('keypoints', data=kp_data)
                    group.create_dataset('descriptors', data=des)
    
    def append_one(self, image_name):
        """ Append one image to the dataset. """
        if not os.path.exists(image_name):
            print(f"Image {image_name} not found.")
            return