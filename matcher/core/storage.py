import h5py
import numpy as np
import cv2
import os
from tqdm import tqdm

class ImageDataSet:
    DEBUG = False
    def __init__(self, fetch_folder_name, force_update=False):
        if not os.path.exists(fetch_folder_name):
            print(f"Folder {fetch_folder_name} not found.")
            return

        _path = os.path.dirname(os.path.abspath(__file__))
        self.fetch_folder_path = os.path.join(_path, "../..", fetch_folder_name)
        self.save_folder_path = os.path.join(_path, "..", "storage")
        os.makedirs(self.save_folder_path, exist_ok=True)
        self.dataset_name = fetch_folder_name
        self.h5_file = h5py.File(f'{self.save_folder_path}/{self.dataset_name}.h5', 'a')
        self.waiting_list = []

        self.sift = cv2.SIFT_create()
        if self.is_empty() or force_update:
            if force_update:
                print(f"Force update {self.dataset_name}.")
                self.h5_file.clear()
            self.__create_dataset__()
            self.save_all()

    def is_empty(self):
        return len(self.h5_file.items()) == 0

    def __create_dataset__(self):
        for filename in os.listdir(self.fetch_folder_path):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                image_path = os.path.join(self.fetch_folder_path, filename)
                self.waiting_list.append((image_path, filename.split('.')[0]))

    def read(self, image_name):
        """ Read keypoints and descriptors from the dataset with image_name."""
        if image_name in self.h5_file:
            image_data = self.h5_file[image_name]
            keypoints = []
            for pt, size, angle, response, octave, class_id in image_data['keypoints'][:]:
                kp = cv2.KeyPoint(x=pt[0], y=pt[1], size=size, angle=angle, response=response, octave=octave, class_id=class_id)
                keypoints.append(kp)
            return (image_name, (keypoints, image_data['descriptors'][:]))
        else:
            print(f"Image {image_name} not found in the dataset.")
            return (image_name, (None, None))

    def read_all(self):
        """ Read all keypoints and descriptors from the dataset. """
        return [self.read(image_name) for image_name in list(self.h5_file.keys())]

    def save_all(self):
        """ Extract features from images and save to HDF5 file. """
        if len(self.waiting_list) == 0:
            print("No image to fetch.")
            return

        for image_path, filename in tqdm(self.waiting_list, desc=f"Extracting features from {self.dataset_name}...", total=len(self.waiting_list)):
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            kp, des = self.sift.detectAndCompute(image, None)
            group = self.h5_file.create_group(filename)
            print(f"Group {filename} created.")

            kp_data = np.array([(kp[i].pt, kp[i].size, kp[i].angle, kp[i].response, kp[i].octave, kp[i].class_id) for i in range(len(kp))], dtype=[('pt', 'f4', 2), ('size', 'f4'), ('angle', 'f4'), ('response', 'f4'), ('octave', 'i4'), ('class_id', 'i4')])
            group.create_dataset('keypoints', data=kp_data)
            group.create_dataset('descriptors', data=des)
        self.waiting_list = []

    def save_one(self, image_name, keypoints, descriptors):
        """ Save one image to the dataset. """
        if image_name in self.h5_file:
            print(f"Image {image_name} already exists in the dataset.")
            return
        group = self.h5_file.create_group(image_name)
        print(f"Group {image_name} created.")

        kp_data = np.array([(keypoints[i].pt, keypoints[i].size, keypoints[i].angle, keypoints[i].response, keypoints[i].octave, keypoints[i].class_id) for i in range(len(keypoints))], dtype=[('pt', 'f4', 2), ('size', 'f4'), ('angle', 'f4'), ('response', 'f4'), ('octave', 'i4'), ('class_id', 'i4')])
        group.create_dataset('keypoints', data=kp_data)
        group.create_dataset('descriptors', data=descriptors)

    def append_one(self, target_folder_path, image_name):
        """ Append one image to the dataset. """
        print("append image:", target_folder_path)
        if not os.path.exists(target_folder_path):
            print(f"Image {image_name} not found.")
            return
        image = cv2.imread(target_folder_path, cv2.IMREAD_GRAYSCALE)
        kp, des = self.sift.detectAndCompute(image, None)
        self.save_one(image_name, kp, des)

    def remove(self, image_name):
        """ Remove one image from the dataset. """
        if image_name in self.h5_file:
            del self.h5_file[image_name]
            print(f"Image {image_name} removed from the dataset.")
        else:
            print(f"Image {image_name} not found in the dataset.")