class GenerateFile:
    def __init__(self, savedir):
        self.savedir = savedir

    def generateTXT(self, filedir, filename, objects):
        text = ""
        classLookup = ["", "blue-tennis-ball", "red-tennis-ball"]
        for obj in objects:
            (label, minX, minY, maxX, maxY) = obj
            # Get elements from list of stuff
            labelNum = (classLookup.index(label)) if classLookup.index(label) != -1 else 0
            # Generate in format
            lineText = (str(labelNum) + " " +
                    str((maxX + minX) / 2) + " " +
                    str((maxY + minY) / 2) + " " +
                    str(maxX - minX) + " " +
                    str(maxY - minY))
            # Check if text is empty, if so, no newline
            if text == "": text += lineText
            else: text += ("\n" + lineText)

        with open(self.savedir + "/" + filename[:len(filename) - 4] + ".txt", "w") as f:
            f.write(text)