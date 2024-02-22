from ..matcher.core.match import Matcher
from flask import Flask, url_for, request
from PIL import Image
import base64
import io
app = Flask(__name__, static_folder="../static")
@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/upload", methods=["POST"])
def upload():
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

# @app.route("add")

# if __name__ == "__main__":
#     app.run("localhost", 5000, True)