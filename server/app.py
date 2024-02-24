from ..matcher.core.match import Matcher
from flask import Flask, url_for, request
from PIL import Image
import base64
import numpy as np
import cv2
app = Flask(__name__, static_folder="../static")
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/upload", methods=["POST"])
def upload():
    """
    get img_base64 => save => cv2.imread => match
    """
    data = request.json
    image_data_base64 = data.get("image_data")

    # 去除前缀
    prefix = 'data:image/png;base64,'
    if image_data_base64.startswith(prefix):
        base64_encoded_data = image_data_base64[len(prefix):]
    else:
        base64_encoded_data = image_data_base64

    # 添加填充字符
    padding_needed = 4 - len(base64_encoded_data) % 4
    base64_encoded_data += '=' * padding_needed

    # 解码 Base64 编码的图像数据
    decoded_data = base64.b64decode(base64_encoded_data)

    # 将二进制数据保存为图片文件
    with open('../image.png', 'wb') as image_file:
        image_file.write(decoded_data)

    matcher = Matcher("foo")
    best_match_path, best_match_similarity = matcher.match("image.png")
    if best_match_path is None:
        return "No match found."
    return url_for("static", filename=f"{best_match_path}.jpg", _external=False) + f" similarity: {best_match_similarity}"

@app.route("/match", methods=["POST"])
def match():
    sum_buffer = request.data
    width = int(request.args.get("w"))
    height = int(request.args.get("h"))
    # 切分 ybuffer 和 uvbuffer
    ybuffer = sum_buffer[:width * height]
    uvbuffer = sum_buffer[width * height:]

    # 将 ybuffer 和 uvbuffer 转换为 NumPy 数组
    ybuffer_np = np.frombuffer(ybuffer, dtype=np.uint8)
    uvbuffer_np = np.frombuffer(uvbuffer, dtype=np.uint8)

    # 重新构造 YUV 图像
    yuv_image = np.concatenate((ybuffer_np.reshape((height, width)),
                                uvbuffer_np.reshape((height // 2, width))),
                                axis=0)

    gray_image = cv2.cvtColor(yuv_image, cv2.COLOR_YUV2GRAY_420)
    # cv2.imwrite("output_gray_image.jpg", gray_image)
    matcher = Matcher("foo")
    best_match_path, best_match_similarity = matcher.match_from_cv2(gray_image)
    if best_match_path is None:
        return "No match found."
    return {
        "url": url_for("static", filename=f"foo/{best_match_path}.jpg", _external=False),
        "similarity": best_match_similarity
    }
    

# if __name__ == "__main__":
#     app.run("localhost", 5000, True)