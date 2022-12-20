from queue import Queue
import threading, time
import cv2 as cv
from concurrent.futures import ThreadPoolExecutor
import torch

thread_state = True
state = False
ret = {}
frame = {}
fps = 0


#
class ProcessFrame(threading.Thread):
    def __init__(self, name, queue1):
        threading.Thread.__init__(self, name=name)
        self.process_data = queue1

    def run(self):
        global thread_state
        global state
        global ret
        global frame

        print("thread2 open!")

        model = torch.hub.load('D:\\yolo\\yolov5-master', "custom", "D:\\yolo\\yolov5-master\\yolov5s.pt",
                               source="local")
        while True:

            if ret:
                # start = time.time()
                res = model(frame)

                res.render()  # 打标签
                #res.print()
                im = res.imgs[0]
                self.process_data.put(im)
                state = True
            elif thread_state is False:
                break
        print("t2 finished")


#
class VideoPlay(threading.Thread):
    def __init__(self, name, queue):
        threading.Thread.__init__(self, name=name)
        self.process_data = queue
        # self.retdata=RET
        # self.img=IMG

    def run(self):
        global state, fps
        global thread_state
        global ret
        global frame
        global start

        print("thread1 open!")

        cap = cv.VideoCapture(0)
        ret, frame = cap.read()
        start = time.time()
        while True:

            ret, frame = cap.read()

            # self.retdata.put(ret)
            # self.img.put(frame)
            if state:

                im = self.process_data.get()
                cv.imshow('pic', im)
                fps = fps + 1
                if cv.waitKey(1) & 0xFF == ord('q'):
                    end = time.time()
                    elapsed=end-start
                    print("FPS: {} , Elapsed Time: {} , Frames Processed: {}".format(fps/elapsed, elapsed, fps))
                    break

        ret = False
        thread_state = False
        cap.release()
        cv.destroyAllWindows()
        print("t1 finished")


if __name__ == '__main__':
    print("---主线程开始---")
    queue = Queue()  # 实例化堵塞队列，保证线程安全
    # RET=Queue()
    # IMG=Queue()

    # producer = ProcessFrame("ProcessFrame", queue)  # 实例化线程 ，并传入队列作为参数
    # consumer = VideoPlay("VideoPlay", queue)  # 实例化线程 ，并传入队列作为参数
    #
    # producer.start()
    # consumer.start()
    # producer.join()
    # consumer.join()
    pool = ThreadPoolExecutor(10)
    pool.submit(ProcessFrame('PROCESS', queue).run)
    pool.submit(VideoPlay('PLAY', queue).run)
    pool.shutdown(True)
    print("---主线程结束---")
