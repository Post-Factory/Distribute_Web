# 2021 빅리더 AI 아카데미 with 울산항망공사

프로젝트 진행 기간 : 2021-08-02 ~ 2021-08-30

자동차 화물 수기 문제를 해결하기 위해 OCR과 데이터 공유 서비스 개발

app.py : 웹을 실행시키는 파일로 flask 기반으로 작동된다. 현재 AWS EC2를 통해 배포 중입니다.
※ 고도화 작업으로 디버깅이 끝나지 않았습니다.

loading_DB.sql : MySQL로 만든 DB입니다. 다양한 테스트를 진행하게 되면 DB 충돌이 나서 DB를 초기화 할 때 사용하고 있습니다.

실행 방법
1) localCamera 폴더를 clone 받으시고 실행을 시킵니다. (저자는 pycharm 환경에서 실행을 시켰습니다.)
2) AWS의 주소(http://3.20.99.214:4997/)로 접속 후 사용이 가능합니다.

    ※ 웹은 이미 AWS로 배포 중임으로 AWS 주소로 접속이 가능하나 OCR 페이지로 이동이 불가능합니다.
    OCR은 로컬 카메라를 사용하기 위해 git의 localCamera 폴더를 받으시고 local에서 실행이 가능합니다.
    
    ※ localCamera를 실행을 시켜도 되지 않는 경우 line87 : cam = cv2.VideoCapture(1)의 숫자를 카메라가 연결되있는 index로 변경하면 가능합니다.
   
