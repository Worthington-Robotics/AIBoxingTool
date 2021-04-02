import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
from PIL import Image, ImageTk
from getTFBboxes import GetTFBBoxes
from createXmlFile import CreateXmlFile
import os

scriptLoc = os.path.dirname(os.path.realpath(__file__))

window = tk.Tk()
window.title("NNlabelImg")

COLORS = ['red', 'blue', 'yellow', 'pink', 'cyan', 'green', 'black']

imgList = []

imgFolder = ''

PATH_TO_MODEL_DIR = scriptLoc + "/TFmodel/" + "/saved_model"

class MainApplication(tk.Frame):
    bboxList = []
    bboxIdList = []
    imgList = []
    imgFolder = ''
    bboxName = ''
    currentImg = 0
    tkimg = None
    saveFolder = ''

    def nextImage(self):
        self.saveXML()
        self.clearBboxes()
        self.currentImg += 1
        self.loadImage()
        self.imgNum.config(text="Image {}/{}".format(self.currentImg, len(self.imgList)))
    
    def nextImageKeybind(self, event):
        self.saveXML()
        self.clearBboxes()
        self.currentImg += 1
        self.loadImage()
        self.imgNum.config(text="Image {}/{}".format(self.currentImg, len(self.imgList)))
        
    def prevImage(self):
        if self.currentImg == 0:
            return
        self.clearBboxes()
        self.currentImg -= 1
        self.loadImage()
        self.imgNum.config(text="Image {}/{}".format(self.currentImg + 1, len(self.imgList)))

    def prevImageKeybind(self, event):
        if self.currentImg == 0:
            return
        self.clearBboxes()
        self.currentImg -= 1
        self.loadImage()
        self.imgNum.config(text="Image {}/{}".format(self.currentImg + 1, len(self.imgList)))

    def saveDir(self):
        self.saveFolder = filedialog.askdirectory(initialdir = "/", title = "Select Image Directory")

    def getFolderName(self):
        self.imgFolder = filedialog.askdirectory(initialdir = "/", title = "Select Image Directory")
        self.loadDir()
        self.imgNum.config(text="Image {}/{}".format(self.currentImg + 1, len(self.imgList)))

    def setBBoxNameInput(self, textbox):
        result = textbox.get("1.0","end")
        self.bboxName = result

    def loadDir(self):
        # self.imageList = glob.iglob(self.imgFolder + '**/*.jpg', recursive=True)
        # self.imageList = sorted(self.imageList)
        self.imgList = []
        for filename in os.listdir(self.imgFolder):
            if(filename.endswith(".jpg") or filename.endswith(".png")):
                self.imgList.append(filename)
        if len(self.imgList) == 0:
            print("No jpg or png photos in dir")
            return
        self.loadImage()
        
    #Draw BBox Commands
    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        tempId = self.mainPanel.create_rectangle(self.x, self.y, 1, 1, outline="green", width=5)
        self.bboxIdList.append(tempId)

    def on_move_press(self, event):
        curX, curY = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.mainPanel.coords(self.bboxIdList[len(self.bboxIdList) - 1], self.start_x, self.start_y, curX, curY)
    
    def mouse_move(self, event):
        self.mouseXY.config(text = "Mouse x, y ({}, {})".format(event.x, event.y))

    def on_button_release(self, event):
        self.mousex = event.x
        self.mousey = event.y
        print(type(self.mousex))
        print(type(self.start_x))
        if(self.start_x <= self.mousex):
            xmin = self.start_x
            xmax = self.mousex
        else:
            xmin = self.mousex
            xmax = self.start_x
        if(self.start_y <= self.mousey):
            ymin = self.start_y
            ymax = self.mousey
        else:
            ymin = self.mousey
            ymax = self.start_y
        self.bboxName = simpledialog.askstring("Input", "Bounding Box Name", parent = window)
        if self.bboxName is None:
            self.mainPanel.delete(self.bboxIdList[len(self.bboxIdList) - 1])
            self.bboxIdList.pop()
            print(self.bboxIdList)
            return
        self.bboxList.append([self.bboxName, xmin / self.imgW * self.orgW, ymin / self.imgH * self.orgH, xmax / self.imgW * self.orgW, ymax / self.imgH * self.orgH])
        self.listbox.insert(tk.END, self.bboxName)

    def loadImage(self):
        imageName = self.imgList[self.currentImg]
        img = Image.open(self.imgFolder + "/" + imageName)
        self.orgW = img.width
        self.orgH = img.height
        if(img.height < img.width):
            self.imgW = 1000
            self.imgRatio = float(img.width) / 1000
            self.imgH = img.height / self.imgRatio
        else:
            self.imgH = 1000
            self.imgRatio = float(img.height) / 1000
            self.imgW = img.width / self.imgRatio
        img = img.resize((int(self.imgW), int(self.imgH)), Image.ANTIALIAS)
        self.tkimg = ImageTk.PhotoImage(img)
        self.mainPanel.config(width = max(self.tkimg.width(), 400), height = max(self.tkimg.height(), 400))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=tk.NW)
        self.drawAIBoxes()

    def drawAIBoxes(self):
        bboxes = self.tfBoxes.getBBoxData(self.imgFolder + "/" + self.imgList[self.currentImg])
        for bbox in bboxes:
            (self.bboxName, xmin, xmax, ymin, ymax) = bbox
            tempId = self.mainPanel.create_rectangle(xmin * self.imgW, ymin * self.imgH, xmax * self.imgW, ymax * self.imgH, outline="green", width = 5)
            self.bboxIdList.append(tempId)
            self.bboxList.append([self.bboxName, xmin * self.orgW, ymin * self.orgH, xmax * self.orgW, ymax * self.orgH])
            self.listbox.insert(tk.END, self.bboxName)

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)

    def clearBboxes(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def clearBboxesKeybind(self, event):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []

    def bboxSelect(self, event):
        self.revertColors(self)
        selection = self.listbox.curselection()
        print(self.bboxIdList)
        print(selection)
        if len(selection) != 1 :
            return
        idx = int(selection[0])
        rectangle = self.bboxIdList[idx]
        self.mainPanel.itemconfig(rectangle, outline="yellow")

    def revertColors(self, event):
        for bbox in self.bboxIdList:
            self.mainPanel.itemconfig(bbox, outline="green")
        return

    def saveXML(self):
        self.createXML = CreateXmlFile(self.saveFolder)
        filename = self.imgList[self.currentImg]
        self.createXML.generateXML(self.imgFolder, filename, self.bboxList)
        return

    def saveXMLKeyBind(self, event):
        self.createXML = CreateXmlFile(self.saveFolder)
        filename = self.imgList[self.currentImg]
        self.createXML.generateXML(self.imgFolder, filename, self.bboxList)
        return

    def goToImg(self):
        imgNum = int(self.imgEntry.get())
        self.currentImg = imgNum
        self.loadImage()
        self.imgNum.config(text="Image {}/{}".format(self.currentImg, len(self.imgList)))
        
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.parent = parent
        self.frame = tk.Frame(parent)

        self.tfBoxes = GetTFBBoxes(PATH_TO_MODEL_DIR, ['powercell']) # The list should be the label map
        
        self.mousex = 0
        self.mousey = 0

        self.x = self.y = 0

        self.start_x = None
        self.start_y = None

        #Images for Buttons Declarations
        self.next_image_photo = tk.PhotoImage(file=os.path.join(scriptLoc, "Images/Right_Arrow.png"))
        self.next_image_photo = self.next_image_photo.subsample(3, 3)

        self.prev_image_photo = tk.PhotoImage(file=os.path.join(scriptLoc, "Images/Left_Arrow.png"))
        self.prev_image_photo = self.prev_image_photo.subsample(3, 3)

        self.folder_photo = tk.PhotoImage(file=os.path.join(scriptLoc, "Images/Folder.png"))
        self.folder_photo = self.folder_photo.subsample(27, 27)

        #Button Declarations
        self.nextImgButton = tk.Button(window, text="Next Image", font=("ariel", 8), image=self.next_image_photo, command=self.nextImage, compound=tk.TOP)
        self.nextImgButton.grid(row=0, column=0)
        self.previousImgButton = tk.Button(window, text="Previous Image", font=("ariel", 8), image=self.prev_image_photo, command=self.prevImage, compound=tk.TOP)
        self.previousImgButton.grid(row=1, column=0)
        self.openDirButton = tk.Button(window, text="Open Dir", font=("ariel", 8), image=self.folder_photo, command=self.getFolderName, compound=tk.TOP)
        self.openDirButton.grid(row=2, column=0)
        self.saveDirButton = tk.Button(window, text="Save Dir", font=("ariel", 8), image=self.folder_photo, command=self.saveDir, compound=tk.TOP)
        self.saveDirButton.grid(row=3, column=0)
        self.saveXMLButton = tk.Button(window, text="Save XML", font=("ariel", 8), command=self.saveXML)
        self.saveXMLButton.grid(row=4, column=0)
        self.deleteBboxButton = tk.Button(window, text="Delete Bbox", font=("ariel", 8), command=self.delBBox, compound=tk.TOP)
        self.deleteBboxButton.grid(row=1, column=3)
        self.clearBboxButton = tk.Button(window, text="Clear Bboxes", font=("ariel", 8), command=self.clearBboxes, compound=tk.TOP)
        self.clearBboxButton.grid(row=2, column=3)
        self.resetAiBboxes = tk.Button(window, text="Reset Bounding Boxes", font=("ariel", 8), command=self.drawAIBoxes)
        self.resetAiBboxes.grid(row=3, column=3)

        #Canvas Declaration
        self.mainPanel = tk.Canvas(window, cursor='tcross')
        self.mainPanel.bind("<ButtonPress-1>", self.on_button_press)
        self.mainPanel.bind("<B1-Motion>", self.on_move_press)
        self.mainPanel.bind("<Motion>", self.mouse_move)
        self.mainPanel.bind("<ButtonRelease-1>", self.on_button_release)
        self.mainPanel.grid(row=0, column=1, rowspan=5)
        self.mouseXY = tk.Label(window, text="Mouse x, y ({}, {})".format(self.mousex, self.mousey))
        self.mouseXY.grid(row = 0, column = 3)
        self.imgNum = tk.Label(window, text="Image {}/{}".format(self.currentImg + 1, len(self.imgList)))
        self.imgNum.grid(row=4, column=3)

        #Bbox List
        self.bboxListTitle = tk.Label(window, text="Bounding Boxes:", height=1)
        self.bboxListTitle.grid(row = 0, column = 2)
        self.listbox = tk.Listbox(window, width = 22, height = 22)
        self.listbox.bind("<ButtonPress-1>", self.bboxSelect)
        self.listbox.grid(row = 1, column = 2, rowspan=4)

        #Go To Image Button
        self.GoToImageButton = tk.Frame(window)
        self.goToImgButtonLbl = tk.Label(self.GoToImageButton, text="Go to Img No.:", font=("ariel", 8))
        self.goToImgButtonLbl.grid(row=0, column=0)
        self.imgEntry = tk.Entry(self.GoToImageButton, width=5)
        self.imgEntry.grid(row=0, column=1)
        self.goButton = tk.Button(self.GoToImageButton, text="Go", font=("ariel", 8), command=self.goToImg)
        self.goButton.grid(row=0, column=2)
        self.GoToImageButton.grid(row=4, column=4)

        #Keybinds
        window.bind("<Control-s>", self.saveXMLKeyBind)
        window.bind("<Key-d>", self.nextImageKeybind)
        window.bind("<Key-a>", self.prevImageKeybind)
        window.bind("<Key-c>", self.clearBboxesKeybind)

if __name__ == '__main__':
    mainApp = MainApplication(window)
    window.resizable(width = True, height = True)
    window.mainloop()
