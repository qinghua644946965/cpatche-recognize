from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import os
import ddddocr

ocr = ddddocr.DdddOcr()


app = Flask(__name__)

# 启用 CORS
CORS(app, supports_credentials=True)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, World!'}), 200

@app.route('/api', methods=['POST'])
def upload_image():
    data = request.json

    # 检查是否提供了图片数据
    if 'image' not in data:
        return jsonify({'error': 'No image provided'}), 400

    # 获取 Base64 编码的图片
    image_data = data['image']

    try:
        # 解码 Base64 图片
        image_data = base64.b64decode(image_data.split(',')[1])  # 处理可能的 data:image/png;base64, 前缀

        # 保存图片
        image_path = 'uploaded_image.png'  # 或者使用 UUID 生成文件名
        with open(image_path, 'wb') as f:
            f.write(image_data)

        image = open("uploaded_image.png", "rb").read()
        result = ocr.classification(image)
        print(result)

        return jsonify({'message': 'Image saved successfully', 'data': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
