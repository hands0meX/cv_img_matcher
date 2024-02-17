import cv2
import os
import h5py

# 读取目标图片
target_image_path = "matcher/home.jpg"
target_image = cv2.imread(target_image_path, cv2.IMREAD_GRAYSCALE)

# 创建SIFT对象
sift = cv2.SIFT_create(nfeatures=500, edgeThreshold=10, sigma=1.6)
# 提取目标图片的特征点和描述子
kp1, des1 = sift.detectAndCompute(target_image, None)
# # 读取 HDF5 文件
# with h5py.File('matcher/features.h5', 'r') as f:
#     # 读取关键点数据
#     kp_data = f['keypoints'][:]
#     kp1 = []

#     # 解析关键点数据
#     for pt, size, angle, response, octave, class_id in kp_data:
#         kp = cv2.KeyPoint(x=pt[0], y=pt[1], size=size, angle=angle, response=response, octave=octave, class_id=class_id)
#         kp1.append(kp)

#     # 读取描述子数据
#     des1 = f['descriptors'][:]

print("Keypoints shape:", len(kp1))
# 设置一个阈值，用于筛选匹配对
threshold = 0.75

# 遍历文件夹中的图片文件
image_folder = 'matcher/pics'
best_match_image_path = None
best_match_similarity = 0
output_image = None
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # 读取文件
        image_path = os.path.join(image_folder, filename)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # 提取当前图片的特征点和描述子
        kp2, des2 = sift.detectAndCompute(image, None)

        # 使用BFMatcher进行特征匹配
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)

        # 计算相似度比例
        good_matches = [m for m, n in matches if m.distance < threshold * n.distance]
        similarity = len(good_matches) / len(matches)

        # 更新最佳匹配
        if similarity > best_match_similarity:
            best_match_similarity = similarity
            best_match_image_path = image_path
            output_image = cv2.drawMatches(target_image, kp1, image, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv2.imwrite("matcher/result.jpg", output_image)

# 返回相似度最高的图片路径
print(f'Best match image path: {best_match_image_path}, Similarity: {best_match_similarity}')
