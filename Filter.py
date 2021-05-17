
from PIL import Image
from PIL import ImageFilter
from PIL.ImageFilter import *
import os


def CreatePath(name):
    outPath = r"C:\Users\emili\Desktop\ClusterASD\Images\ImgFiltros/"+name+"Filtros/"

    os.makedirs(outPath, exist_ok=True)


def ImageFilter(path, name):

    # path of the folder containing the raw images
    inPath = path

    # path of the folder that will contain the modified image

    outPath = r"C:\Users\emili\Desktop\ClusterASD\Images\ImgFiltros/"+name+"Filtros/"

    for imagePath in os.listdir(inPath):

        inputPath = os.path.join(inPath, imagePath)
        simg = Image.open(inputPath)

        fullOutPath = os.path.join(outPath, imagePath)
        # fullOutPath contains the path of the output
        # image that needs to be generated
        simg.rotate(90).filter(ModeFilter(size=9)).save(fullOutPath)
        
        simg.close()
        print(fullOutPath)
