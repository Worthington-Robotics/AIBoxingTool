class CreateXmlFile:
    def __init__(self, savedir):
        self.savedir = savedir

    def generateXML(self, filedir, filename, objects):
        text = ""
        for bbox in objects:
            # Get elements from list of stuff
            classnum = bbox[0]
            xmin = bbox[1]
            ymin = bbox[2]
            xmax = bbox[3]
            ymax = bbox[4]
            # create the line of text
            lineText = (str(classnum) + " " +
                    str(xmin) + " " +
                    str(ymin) + " " +
                    str(xmax) + " " +
                    str(ymax)
                    )
            # Check if text is empty, if so, no newline
            if text == "": text += lineText
            else: text += ("\n" + lineText)

        with open(self.savedir + "/" + filename[:len(filename) - 4] + ".txt", "w") as f:
            f.write(text)