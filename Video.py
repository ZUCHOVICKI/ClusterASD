import cv2
import os

from functools import cmp_to_key

def isnum (num):
    try:
        int(num)
        return True
    except:
        return False
 
#Numerically sorts filenames
def image_sort (x,y):
    x = int(x.split(".")[0])
    y = int(y.split(".")[0])
    return x-y

def CreateVideo(name):

 
     # Arguments
    dir_path = r'C:\Users\emili\Desktop\ClusterASD\Images\ImgFiltros/'+name+"Filtros"
    ext = 'jpg'
    output = name+"video.mp4"

    images = []
    for f in os.listdir(dir_path):
        print(f)
        if f.endswith(ext):
            images.append(f)
    
    int_name = images[0].split(".")[0]
    if isnum(int_name):
        images = sorted(images, key=cmp_to_key(image_sort))

    # Determine the width and height from the first image
    image_path = os.path.join(dir_path, images[0])
    frame = cv2.imread(image_path)
    cv2.imshow('video',frame)
    height, width, channels = frame.shape

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # Be sure to use lower case
    out = cv2.VideoWriter(output, fourcc, 20.0, (width, height))

    for image in images:

        image_path = os.path.join(dir_path, image)
        frame = cv2.imread(image_path)

        out.write(frame) # Write out frame to video

        cv2.imshow('video',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break

    # Release everything if job is finished
    out.release()
    cv2.destroyAllWindows()

    print("The output video is {}".format(output))

    os.replace(r"C:\Users\emili/"+output,r"C:\Users\emili\Desktop\ClusterASD\Videos/"+output)