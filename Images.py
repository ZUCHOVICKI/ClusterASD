
import cv2
import os
  


def VideoToImage(path,names):

    dirs = r'C:\Users\emili\Desktop\ClusterASD\Images/'
    
    cam = cv2.VideoCapture(path)
    
    try:
        
        
        if not os.path.exists(r'C:\Users\emili\Desktop\ClusterASD\Images'):
            os.makedirs(r'C:\Users\emili\Desktop\ClusterASD\Images')

        if not os.path.exists(r'C:\Users\emili\Desktop\ClusterASD\Images\ImgFiltros'):
            os.makedirs(r'C:\Users\emili\Desktop\ClusterASD\Images\ImgFiltros')
        os.makedirs(dirs+names,exist_ok=True)
    
   
    except OSError:
        print ('Error: Creating directory of data')

    currentframe = 0
    
    while(True):
        
       
        ret,frame = cam.read()
    
        if ret:
           
            name = dirs+names +'/'+ str(currentframe) + '.jpg'
            print ('Creating...' + name)
    
            
            cv2.imwrite(name, frame)
    
            
            currentframe += 1
        else:
            break
    
    
    cam.release()
    cv2.destroyAllWindows()