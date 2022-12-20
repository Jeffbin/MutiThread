import torch
import cv2 as cv
import threading
from queue import Queue
import time
from concurrent.futures import ThreadPoolExecutor

ret = {}
frame = {}

state = False
cap = cv.VideoCapture(0)
thread_state = True


def process_frame(queue2):
    print("thread2 open!")
    # time.sleep(1)
    global frame, state, thread_state, start,ret
    model = torch.hub.load('D:\\yolo\\yolov5-master', "custom", "D:\\yolo\\yolov5-master\\yolov5s.pt", source="local")
    while True:

        if ret is False:
            print('can not open the camera')
        else:
            # start = time.time()
            res = model(frame)

            res.render()  # 打标签
            res.print()
            a = res.imgs[0]
            queue2.put(a)
            state = True
        if thread_state is False:
            break
    print("t2 finished")


def show_frame(queue1):
    print("thread1 open!")
    global frame, ret, state, thread_state
    while True:
        ret, frame = cap.read()
        #print('running')
        if state:

            cv.imshow("res", queue1.get())
            # end = time.time()
            # # Time elapsed
            # seconds = end - start + 0.0000001
            # print("Time taken : {0} seconds".format(seconds))
            # # Calculate frames per second
            # fps = 1 / seconds
            # print("Estimated frames per second : {0}".format(fps))
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    ret = False
    thread_state = False
    cap.release()
    cv.destroyAllWindows()
    print("t1 finished")


# def model_learn():
#     thread1 = threading.Thread(name='t1', target=show_frame)
#     thread2 = threading.Thread(name='t2', target=process_frame)
#     thread1.start()
#     thread2.start()
#     thread1.join()
#     thread2.join()


if __name__ == '__main__':
    # model_learn()
    print('----主线程开始----')
    queue = Queue()

    pool = ThreadPoolExecutor(10)
    # pool.submit(show_frame)

    pool.submit(process_frame, queue)
    pool.submit(show_frame, queue)

    pool.shutdown(True)
    print('----主线程结束----')
