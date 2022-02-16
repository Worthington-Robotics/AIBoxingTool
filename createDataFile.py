import xml.etree.ElementTree as ET
from xml.dom import minidom
from PIL import Image

class CreateXmlFile:
    def __init__(self, savedir):
        self.savedir = savedir

    def generateXML(self, filedir, filename, objects):
        img = Image.open(filedir + "/" + filename)
        imgWidth, imgHeight = img.size
        
        annotation = ET.Element('annotation')

        xmlfilename = ET.SubElement(annotation, 'filename')
        xmlfilename.text = filename

        source = ET.SubElement(annotation, 'source')
        database = ET.Element('database')
        database.text = 'Unknown'
        source.append(database)

        size = ET.SubElement(annotation, 'size')
        width = ET.SubElement(size, 'width').text = str(imgWidth)
        height = ET.SubElement(size, 'height').text = str(imgHeight)
        depth = ET.SubElement(size, 'depth').text = '3'

        ET.SubElement(annotation, 'segmented').text = '0'

        for object in objects:
            
            xmlObject = ET.SubElement(annotation, 'object')

            name = ET.SubElement(xmlObject, 'name')
            name.text = str(object[0])

            ET.SubElement(xmlObject, 'pose').text = 'unspecified'

            bndbox = ET.SubElement(xmlObject, 'bndbox')
            
            xmin = ET.SubElement(bndbox, 'xmin')
            xmin.text = str(int(object[1]))
            xmin = ET.SubElement(bndbox, 'ymin')
            xmin.text = str(int(object[2]))
            ymin = ET.SubElement(bndbox, 'xmax')
            ymin.text = str(int(object[3]))
            ymax = ET.SubElement(bndbox, 'ymax')
            ymax.text = str(int(object[4]))

            ET.SubElement(xmlObject, 'truncated').text = '0'
            ET.SubElement(xmlObject, 'difficult').text = '0'

        tree = ET.ElementTree(annotation)

        xmlstr = minidom.parseString(ET.tostring(annotation)).toprettyxml(indent="    ")
        with open(self.savedir + "/" + filename[:len(filename) - 4] + ".xml", "w") as f:
            f.write(xmlstr[23:])