import numpy as np
import cv2 
from SolveProcess_CreateVideo import VideoCreator

class Solver:
    def __init__(self, inputName):
        self.corridorWidth = 10 #width of a corridor in the maze, important, fill out manually using pixelCount program
        self.corridorWidth = self.corridorWidth//2

        self.showProcess = True #display how the algorithm works with a series of pictures
        
        self.inputName = inputName
        outputName = inputName[0:inputName.find('.')] + "_Solved" + ".jpg"
        self.inputDir = 'C:\\Daniel\\Python\\Maze Solver\\' + inputName
        self.outputDir = 'C:\\Daniel\\Python\\Maze Solver\\' + outputName
        self.processDir = f'C:\\Daniel\\Python\\Maze Solver\\Processing\\SolvingStep'#for storing series of photos that explain how the algorithm works
        self.maze = cv2.imread(self.inputDir)
        
    #processing speed depends on dimensions of image (total number of pixels) and width of maze corridor (in pixels)
    def scale(self, img):
        width, height, _ = img.shape
        if width>800 or height>800:
            #scale the image down to max 800 x 800
            scale_factor = 800/width if width>height else 800/height
            new_width, new_height = int(width*scale_factor), int(height*scale_factor)
            img = cv2.resize(img, (new_height, new_width))
        return img

    def to_black(self, img):
        imgList = img.tolist()
        for i, row in enumerate(imgList):
            for j, pixel in enumerate(row):
                if sum(pixel)<200:
                    imgList[i][j] = 0
                else:
                    imgList[i][j] = 255
        return np.array(imgList, dtype=np.uint8)

    def cut_edges(self, img):
        imgList = img.tolist()
        width, height = img.shape
        
        leftGap = 0
        leftGapPixel = imgList[height//2][leftGap]
        while leftGapPixel != 0:
            leftGapPixel = imgList[height//2][leftGap]
            leftGap += 1
        
        rightGap = 0
        rightGapPixel = imgList[height//2][len(imgList[0])-1-rightGap]
        while rightGapPixel != 0:
            rightGapPixel = imgList[height//2][len(imgList[0])-1-rightGap]
            rightGap += 1

        topGap = 0
        topGapPixel = imgList[topGap][width//2]
        while topGapPixel != 0:
            topGapPixel = imgList[topGap][width//2]
            topGap += 1
        
        bottomGap = 0
        bottomGapPixel = imgList[len(imgList)-1-bottomGap][width//2]
        while bottomGapPixel != 0:
            bottomGapPixel = imgList[len(imgList)-1-bottomGap][width//2]
            bottomGap += 1
        
        print(leftGap, rightGap, topGap, bottomGap)
        return leftGap, rightGap, topGap, bottomGap
                    
    def isCorner(self, mazeList, i, j):
        isCorner = False
        a = 0
        topBlack = False
        bottomBlack = False
        leftBlack = False
        rightBlack = False
        while a <= self.corridorWidth:
            if i - a >= 0: #up
                if mazeList[i-a][j] == 0 or mazeList[i-a][j] == 50:
                    topBlack = True
            if i + a < len(mazeList): #down
                if mazeList[i+a][j] == 0 or mazeList[i+a][j] == 50:
                    bottomBlack = True
            if j - a >= 0: #left
                if mazeList[i][j-a] == 0 or mazeList[i][j-a] == 50: 
                    leftBlack = True
            if j + a < len(mazeList[0]): #right 
                if mazeList[i][j+a] == 0 or mazeList[i][j+a] == 50: 
                    rightBlack = True
                
            if topBlack and leftBlack and rightBlack: #corner type "top"
                isCorner = True
                break
            elif leftBlack and topBlack and bottomBlack: #corner type "bottom"
                isCorner = True 
            elif bottomBlack and leftBlack and rightBlack: #corner type "left"
                isCorner = True
            elif rightBlack and topBlack and bottomBlack: #corner type "right"
                isCorner = True
            a += 1
        return isCorner

    def highlight_dead_ends(self, maze):
        isDone = False
        #maze corridors about 50 pixels wide
        mazeList = maze.tolist()
        for i, row in enumerate(mazeList):
            for j, pixel in enumerate(row):
                if pixel == 255:
                    if self.isCorner(mazeList, i, j):
                        mazeList[i][j] = 50
        if mazeList == maze.tolist(): #no more changes were made
            isDone = True
        return np.array(mazeList, dtype=np.uint8), isDone
    
    def solidifyPath(self, maze):
        mazeList = maze.tolist()
        leftGap, rightGap, topGap, bottomGap = self.cut_edges(maze)
        for i, row in enumerate(mazeList):
            for j, pixel in enumerate(row):
                if j<leftGap-1 or j>len(mazeList[0])-rightGap or i<topGap-1 or i>len(mazeList)-bottomGap or pixel==0 or pixel==50: #if it is gap between maze and edge of image or it is wall in the maze, leave it unchanged
                    mazeList[i][j] = [pixel, pixel, pixel] #make it into colored
                elif pixel==255: #path is only thing that is white
                    mazeList[i][j] = [0, 255, 0]
        for i, row in enumerate(mazeList):
            for j, pixel in enumerate(row):
                if sum(pixel)/3==50:
                    mazeList[i][j] = [255,255,255]
        for i, row in enumerate(mazeList):
            for j, pixel in enumerate(row):
                if pixel[1]==255 and sum(mazeList[i-1][j])==0 and sum(mazeList[i+1][j])==0:
                    mazeList[i][j] = [255, 255, 255]
        return np.array(mazeList, dtype=np.uint8)
    
    def solve(self):
        self.maze = self.scale(self.maze)
        self.maze = self.to_black(self.maze)
                    
        isDone = False
        count = 0
        while isDone == False:
            if count%10 == 0:
                print(f"Iterations: {count}")
            if self.showProcess:
                cv2.imwrite(f'{self.processDir}{count}.jpg', self.maze)
            self.maze, isDone = self.highlight_dead_ends(self.maze)
            count += 1

        #create video of algorithm at work
        createVid = input("Create video? (Y/N) ") 
        if createVid.lower() == 'y' and self.showProcess:
            vidConverter = VideoCreator(self.inputName[0:self.inputName.find('.')])
            vidConverter.to_animation()
        
        self.maze = self.solidifyPath(self.maze) 
        cv2.imwrite(self.outputDir, self.maze)
        cv2.imshow("Maze", self.maze)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

mazeName = str(input("Enter maze name: ")) + ".jpg"
solver = Solver(mazeName)
solver.solve()

