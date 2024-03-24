import cv2
import numpy as np

def scale(img):
    width, height, _ = img.shape
    if width>800 or height>800:
        #scale the image down to max 800 x 800
        scale_factor = 800/width if width>height else 800/height
        new_width, new_height = int(width*scale_factor), int(height*scale_factor)
        img = cv2.resize(img, (new_height, new_width))
    return img

def to_black(img):
    imgList = img.tolist()
    for i, row in enumerate(imgList):
        for j, pixel in enumerate(row):
            if sum(pixel)<200:
                imgList[i][j] = [0,0,0]
            else:
                imgList[i][j] = [255, 255, 255]
    return np.array(imgList, dtype=np.uint8)

def draw_pixel_guide(img):
    width, height, _ = img.shape
    verticalLineCo = width//2 #vetical line centered
    horizontalLineCo = height//2 #horizontal line centered
    imgList = img.tolist()
    for i, row in enumerate(imgList):
        for j, _ in enumerate(row):
            if i == verticalLineCo and j%2==0:
                imgList[i][j] = [0,0,200]
            if j == horizontalLineCo and i%2==0:
                imgList[i][j] = [0,0,200]
    img = np.array(imgList, dtype=np.uint8)
    cv2.imshow("Pixel Guide", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('C:\\Daniel\\Python\\Maze Solver\\PixelGuide.jpg', img)
                    
inputName = input("Enter maze name: ")
inputDir = 'C:\\Daniel\\Python\\Maze Solver\\' + inputName + ".jpg"
maze = cv2.imread(inputDir)
maze = scale(maze)
maze = to_black(maze)
draw_pixel_guide(maze)


