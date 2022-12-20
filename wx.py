# importing required libraries
import cv2
import time
from threading import Thread  # library for implementing multi-threaded processing
import torch
from queue import Queue


# defining a helper class for implementing multi-threaded processing
class WebcamStream:
    def __init__(self, stream_id=0):
        self.stream_id = stream_id  # default is 0 for primary camera

        # opening video capture stream
        self.cap = cv2.VideoCapture(self.stream_id)
        if self.cap.isOpened() is False:
            print("[Exiting]: Error accessing webcam stream.")
            exit(0)
        fps_input_stream = int(self.cap.get(5))
        print("FPS of webcam hardware/input stream: {}".format(fps_input_stream))

        # reading a single frame from vcap stream for initializing
        self.ret, self.frame = self.cap.read()
        if self.ret is False:
            print('[Exiting] No more frames to read')
            exit(0)

        # self.stopped is set to False when frames are being read from self.vcap stream
        self.stopped = True
        self.que=q
        # reference to the thread for reading next available frame from input stream
        self.t = Thread(target=self.update, args=())
        self.t.daemon = True  # daemon threads keep running in the background while the program is executing

    # method for starting the thread for grabbing next available frame in input stream
    def start(self):
        self.stopped = False
        self.t.start()

    # method for reading next frame
    def update(self):
        print("thread2 open!")
        model = torch.hub.load('D:\\yolo\\yolov5-master', "custom", "D:\\yolo\\yolov5-master\\yolov5s.pt",
                               source="local")
        while True:
            if self.stopped is True:
                break
            self.ret, self.frame = self.cap.read()
            if self.ret:
                # start = time.time()
                res = model(self.frame)
                res.render()  # 打标签
                res.print()
                im = res.imgs[0]
                q.put(im)
            if self.ret is False:
                print('[Exiting] No more frames to read')
                self.stopped = True
                break
        self.cap.release()

    # method for returning latest read frame
    def read(self):
        return self.frame

    # method called to stop reading frames
    def stop(self):
        self.stopped = True


q = Queue()
# initializing and starting multi-threaded webcam capture input stream
webcam_stream = WebcamStream(stream_id=0)  # stream_id = 0 is for primary camera
webcam_stream.start()

# processing frames in input stream
num_frames_processed = 0
start = time.time()
while True:
    if webcam_stream.stopped is True:
        break
    else:
        frame = webcam_stream.read()

    # adding a delay for simulating time taken for processing a frame
    # delay = 0.03  # delay value in seconds. so, delay=1 is equivalent to 1 second
    # time.sleep(delay)
    num_frames_processed += 1
    frame1 = q.get()
    cv2.imshow('frame', frame1)
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
end = time.time()
webcam_stream.stop()  # stop the webcam stream

# printing time elapsed and fps
elapsed = end - start
fps = num_frames_processed / elapsed
print("FPS: {} , Elapsed Time: {} , Frames Processed: {}".format(fps, elapsed, num_frames_processed))

# closing all windows
cv2.destroyAllWindows()
