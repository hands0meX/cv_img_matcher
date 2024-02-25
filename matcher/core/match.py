import os
import cv2
from .storage import ImageDataSet

class Matcher:
    DEBUG = False
    def __init__(self, dataset_name, debug=False):
        if debug:
            self.DEBUG = debug
        self._path = os.path.dirname(os.path.abspath(__file__))
        self.dataset = ImageDataSet(dataset_name)

    def match(self, target_image_path):
        target_image_path = os.path.join(self._path, "../../", target_image_path)
        if self.DEBUG:
            print("target_image_path:", target_image_path, self.dataset)
        if not self.dataset or self.dataset.is_empty():
            print("No dataset found.")
            return None, 0

        target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
        if target_image is None:
            print(f"Image {target_image_path} not found.")
            return None, 0

        if self.DEBUG:
            print("targe_image:", target_image, target_image_path)
        kp1, des1 = self.dataset.sift.detectAndCompute(target_image, None)
        threshold = 0.75

        best_match_image_path = None
        best_match_similarity = 0

        for image_name, (keypoints, descriptors) in self.dataset.read_all():
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, descriptors, k=2)
            if len(matches) == 0:
                continue
            good_matches = [m for m, n in matches if m.distance < threshold * n.distance]
            similarity = len(good_matches) / len(matches)

            if similarity > best_match_similarity:
                best_match_similarity = similarity
                best_match_image_path = image_name
        if self.DEBUG:
            print(f"Best match: {best_match_image_path}, similarity: {best_match_similarity}")
        return best_match_image_path, best_match_similarity

    def match_from_cv2(self, cv_mat):
        if not self.dataset or self.dataset.is_empty():
            print("No dataset found.")
            return None, 0

        target_image = cv_mat
        kp1, des1 = self.dataset.sift.detectAndCompute(target_image, None)
        threshold = 0.75

        best_match_image_path = None
        best_match_similarity = 0

        for image_name, (keypoints, descriptors) in self.dataset.read_all():
            bf = cv2.BFMatcher()
            matches = bf.knnMatch(des1, descriptors, k=2)
            good_matches = [m for m, n in matches if m.distance < threshold * n.distance]
            similarity = len(good_matches) / len(matches)

            if similarity > best_match_similarity:
                best_match_similarity = similarity
                best_match_image_path = image_name
        if self.DEBUG:
            print(f"Best match: {best_match_image_path}, similarity: {best_match_similarity}")
        return best_match_image_path, best_match_similarity

# matcher = Matcher("foo")
# matcher.match("matcher/home.jpg")

