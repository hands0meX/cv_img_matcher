import os
import cv2
from .storage import ImageDataSet, DetectorType
from enum import Enum

class MatcherType(Enum):
    FLANN = 'FLANN'
    BF = 'BF'
class MatcherNumMethod(Enum):
    KNN = 'KNN'
    SINGLE = 'SINGLE'

class Matcher:
    DEBUG = False
    def __init__(self, dataset_name, debug=False, match_method=MatcherType.BF, match_num_method=MatcherNumMethod.KNN, detector_type=DetectorType.ORB):
        if debug:
            self.DEBUG = debug
        self._path = os.path.dirname(os.path.abspath(__file__))
        self.dataset = ImageDataSet(dataset_name, debug=debug, detector_type=detector_type)
        self.matcher_type = match_method
        self.matcher_num_method = match_num_method
        self.threshold = 0.75
        self.show_matches_pic = True

    def match(self, target_image_path):
        target_image_path = os.path.join(self._path, "../../", target_image_path)
        target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)
        return self.match_main(target_image, target_image_path)

    def match_from_cv2(self, cv_mat):
        return self.match_main(cv_mat)

    def match_main(self, target_image, target_image_name):
        best_match_image_path = None
        best_match_similarity = 0
        best_keypoints = None
        best_matches = None

        if not self.dataset or self.dataset.is_empty():
            print("No dataset found.")
            return best_match_image_path, best_match_similarity

        if target_image is None:
            print(f"Image {target_image_name} not found.")
            return best_match_image_path, best_match_similarity

        if self.DEBUG:
            print("matcher is:", self.matcher_type)
            print("targe_image:", target_image_name)
        kp1, des1 = self.dataset.detector.detectAndCompute(target_image, None)

        for image_name, (keypoints, descriptors) in self.dataset.read_all():
            matcher = None
            matches = None

            if self.DEBUG:
                print(f"Reading image: {image_name}")
            if self.matcher_type == MatcherType.FLANN:
                matcher = cv2.FlannBasedMatcher()
                if self.matcher_num_method == MatcherNumMethod.KNN:
                    matches = matcher.knnMatch(des1, descriptors, k=2)
                elif self.matcher_num_method == MatcherNumMethod.SINGLE:
                    # FIXME: sth error.
                    matches = matcher.match(des1, descriptors)
            elif self.matcher_type == MatcherType.BF:
                matcher = cv2.BFMatcher()
                if self.matcher_num_method == MatcherNumMethod.KNN:
                    matches = matcher.knnMatch(des1, descriptors, k=2)
                elif self.matcher_num_method == MatcherNumMethod.SINGLE:
                    matches = matcher.match(des1, descriptors)

            if len(matches) == 0:
                continue

            if self.matcher_num_method == MatcherNumMethod.KNN:
                good_matches = [m for m, n in matches if m.distance < self.threshold * n.distance]
                similarity = len(good_matches) / len(matches)
            elif self.matcher_num_method == MatcherNumMethod.SINGLE:
                similarity = len(matches) / max(len(kp1), len(keypoints))

            if similarity > best_match_similarity:
                    best_match_similarity = similarity
                    best_match_image_path = image_name
                    best_keypoints = keypoints
                    best_matches = matches
        if self.DEBUG:
            print(f"Best match: {best_match_image_path}, similarity: {best_match_similarity}")
        if self.show_matches_pic:
            best_match_jpg = os.path.join(self.dataset.fetch_folder_path, f"{best_match_image_path}.jpg")
            img2 = cv2.imread(best_match_jpg, cv2.IMREAD_GRAYSCALE)
            if self.matcher_num_method == MatcherNumMethod.KNN:
                out_img = cv2.drawMatchesKnn(target_image, kp1, img2, best_keypoints, best_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
            elif self.matcher_num_method == MatcherNumMethod.SINGLE:
                out_img = cv2.drawMatches(target_image, kp1, img2, best_keypoints, best_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

            # 显示图像
            cv2.imshow('Matches', out_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return best_match_image_path, best_match_similarity

