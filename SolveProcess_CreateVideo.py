import cv2
import os

class VideoCreator():
    def __init__(self, mazeName):
        #1 picture = 1 frame
        self.framesList = [img for img in os.listdir('Processing')]
        self.framesList = self.bubbleSort_frames(self.framesList)
        #create a VideoWriter object to save the frames (out)
        self.fourcc = cv2.VideoWriter_fourcc(*'h264')#ASCII codec for compressing and decompressing the video (encoding it to compress file size)
        self.fps = 10
        frame = cv2.imread('Processing\\'+ str(self.framesList[0]))
        self.height, self.width, _ = frame.shape
        self.outputPath = 'Processing Video\\' + mazeName + ".mp4"
        self.out = cv2.VideoWriter(self.outputPath, self.fourcc, self.fps, (self.width, self.height)) #output

    def to_animation(self):
        for frame in self.framesList:
            self.out.write(cv2.imread('Processing\\'+ frame))
        cv2.destroyAllWindows()
        self.out.release()
        print("Finished")
    
    def bubbleSort_frames(self, framesList):
        stillSorting = True
        while True:
            stillSorting = False
            for i, frame in enumerate(framesList):
                if i!=0:
                    if int(frame[frame.find('p')+1:frame.find('.')]) < int(framesList[i-1][framesList[i-1].find('p')+1:framesList[i-1].find('.')]):
                        framesList[i] = framesList[i-1]
                        framesList[i-1] = frame
                        stillSorting = True
            if stillSorting == False:
                break
        return framesList
                
if __name__ == "__main__":
    vidConverter = VideoCreator("Test")
    vidConverter.to_animation()
