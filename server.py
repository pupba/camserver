from modules.model import DetectModel
import cv2
import numpy as np
import requests
from flask import Flask, request, jsonify
import base64
import os
import json
from flask_cors import CORS

dm = DetectModel()
server = Flask(__name__)
CORS(server, resources={r"/*": {"origins": "*"}})
frame_data = None


@server.route('/detect', methods=['POST', 'GET'])
def detect():
    global frame_data
    global dm
    if request.method == "POST":
        # 전송된 프레임 받아오기
        frame_data = request.data
        # decoding
        img_array = np.frombuffer(frame_data, np.uint8)
        frame = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        # 선박 검출
        result = dm.detectVideo(frame)
        # 객체 판별
        # "BigShip", "Boat", "Bridge", "Buoy", "Island"
        class_ = result["class"]
        # class_ 각 BigShip 또는 Boat일 떄는 기본적으로 1단계
        env_value = os.environ.get('MY_ENV_VARIABLE')
        # env_value = "localhost:5003"
        if class_ == "ship":
            # requests로 전달
            response = requests.post(
                f"http://{env_value}/decision", data=json.dumps({"detect": True}), headers={'Content-Type': 'application/json'})
            # box 처리한 이미지
            img = result["ProcessingImg"]
            cv2.imwrite("./img.png", img)
        else:
            response = requests.post(
                f"http://{env_value}/decision", data=json.dumps({"detect": False}), headers={'Content-Type': 'application/json'})
            cv2.imwrite("./img.png", frame)
        return "success"
    if request.method == "GET":
        # 이미지 처리
        with open('./img.png', 'rb') as f:
            image_data = f.read()
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        return jsonify({'image_data': image_base64})


if __name__ == '__main__':
    server.run(host='0.0.0.0', port='8081')
