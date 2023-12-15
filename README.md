# 선박 식별 서버

본 서버는 YOLOv5x를 커스텀 학습하여 선박, 부표, 해상 구조물을 식별하는 모델을 사용하는 서버입니다.

## 설치 및 환경 설정

1. Git 저장소를 클론합니다.

```shell
git clone https://github.com/pupba/camserver
```

2. 필요한 종속성 설치

```shell
pip install -r requirements.txt
```

3. 서버를 실행

```shell
python server.py
```

-   현재 server.py는 Docker Container로 실행할 것을 가정하여 만들어졌습니다.
-   그냥 Python 코드로 실행 시키려면 server.py를 수정홰주세요.
