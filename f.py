import torch
import cv2 as cv


def show_frame():
    cap = cv.VideoCapture(0)
    model = torch.hub.load('D:\\yolo\\yolov5-master', "custom", "D:\\yolo\\yolov5-master\\yolov5s.pt", source="local")
    while True:
        ret, frame = cap.read()
        if ret:
            res = model(frame)
            res.render()  # 打标签
            cv.imshow("res", res.imgs[0])
            if cv.waitKey(10) & 0xFF == ord('q'):
                break
    cap.release()
    cv.destroyAllWindows()


if __name__ == '__main__':
    show_frame()