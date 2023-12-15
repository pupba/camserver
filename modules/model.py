import torch
import cv2
import os
import numpy as np


class DetectModel:
    def __init__(self) -> None:
        self.__PATH = "./modules/weights/best.pt"
        # 모델 파일 있는지 확인
        if not os.path.isfile(self.__PATH):
            raise FileNotFoundError(
                f"'best.pt' 파일을 찾을 수 없습니다. 경로: {self.__PATH}")
        # GPU가 있다면 GPU 사용
        self.__device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        # self.__model = torch.hub.load(
        #     "ultralytics/yolov5", "custom", path=self.__PATH, force_reload=True)
        self.__model = torch.hub.load(
            'ultralytics/yolov5', 'yolov5s', pretrained=True, device=self.__device)
        self.__model.to(self.__device)
        # img가 저장될 변수
        self.img: np.ndarray = None
        self.result = {"class": None, "ProcessingImg": None}
        self.__class = ("ship", "bouy", "structure")

    def detectVideo(self, frame) -> dict:
        self.img = frame
        result = self.__model(self.img)
        self.__makeBOX(result.pred[0], frame)
        return self.result

    def __makeBOX(self, result: torch.Tensor, origin: np.array) -> None:
        # 바운딩 박스 그리기
        i = 0
        for det in result:
            if i % 2 == 0:
                COLOR = (0, 0, 255)
                i += 1
            else:
                COLOR = (0, 255, 255)
                i += 1
            label = int(det[5])  # 식별 클래스

            conf = float(det[4])  # 결과 신뢰도
            box = det[:4]
            if conf > 0.2 and label == 8:  # 신뢰도가 50% 이상인 것만 바운딩 박스 생성
                # if conf > 0.3:
                x1, y1, x2, y2 = map(int, box)  # 객체 식별 좌표

                # box 그리기
                cv2.rectangle(self.img, (x1, y1), (x2, y2), COLOR, 3)
                # 클래스 출력
                # TEXT = f"{self.__class[label]}"
                TEXT = "Ship"
                cv2.putText(self.img, TEXT, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR, 3)

                # 결과를 저장
                # self.result["class"] = self.__class[label]
                self.result['class'] = "Ship"
                self.result["ProcessingImg"] = self.img

            else:  # 신뢰도가 낮음
                # 결과를 저장
                self.result["class"] = "None"
                self.result["ProcessingImg"] = origin


if __name__ == "__main__":
    dm = DetectModel()
    for i in range(1, 11):
        img = cv2.imread(f"./test/test{i}.jpg")
        result = dm.detectVideo(img)
        if result["class"] != "None":
            cv2.imshow(f"{i}", result["ProcessingImg"])
            cv2.waitKey(0)
            cv2.destroyAllWindows()
