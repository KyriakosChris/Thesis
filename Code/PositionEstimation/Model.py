from mmcv import collect_env
# Check Pytorch installation
import torch, torchvision
# Check MMDetection installation
import mmdet
# Check mmcv installation
from mmcv.ops import get_compiling_cuda_version, get_compiler_version
import mmcv
from mmcv.runner import load_checkpoint
from mmdet.apis import inference_detector, show_result_pyplot
from mmdet.models import build_detector
from tqdm import tqdm
import cv2
import numpy as np
import glob
import os
def poly(model, path):
  poly = []
  vidcap = cv2.VideoCapture(path)
  success, img = vidcap.read()
  while success:
    if img is None:
      continue
    # Use the detector to do inference
    result = inference_detector(model, img)
    success, img = vidcap.read()
    # Let's plot the result
    labels = [
        np.full(bbox.shape[0], i, dtype=np.int32)
        for i, bbox in enumerate(result)
    ]
    #print(labels[0])
    if len(labels[0]) == 0:
      poly.append('skip')
      continue
    else:
      labels = labels[0][0]

    r = result[0][0]
    bbox_int = []
    if labels == 0:
      for i, bbox in enumerate(r):
          bbox_int.append(bbox.astype(np.int32))
      poly.append([[bbox_int[0], bbox_int[1]], [bbox_int[0], bbox_int[3]],
              [bbox_int[2], bbox_int[3]], [bbox_int[2], bbox_int[1]]])
  return poly

def compute(model,videopath):

    pos = poly(model,videopath)
    pos = list(pos)
    # Create a VideoCapture object and read from input file
    cap = cv2.VideoCapture(videopath)
    
    # Check if camera opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video  file")
    
    # Read until video is completed
    count = 0
    bvh_pos = []
    while(cap.isOpened()):
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:
            if pos[count] == 'skip':
                count+=1
                continue
            x0 = pos[count][0][0]
            y0 = pos[count][0][1]
            x1 = pos[count][1][0]
            y1 = pos[count][1][1]
            x2 = pos[count][2][0]
            y2 = pos[count][2][1]
            x3 = pos[count][3][0]
            y3 = pos[count][3][1]
            x = ((((x0+x2)/2) + ((x1+x3)/2))/2)
            y = ((((y0+y2)/2) + ((y1+y3)/2))/2)
            A = (x2 - x0)*(y2 - y0)
            z = np.log2(A)
            bvh_pos.append((x,y,z))
            
            image = cv2.circle(frame, (int(x),int(y)), radius=10, color=(0, 0, 255), thickness=-1)
            image  = cv2.rectangle(frame, (x0,y0), (x2,y2), color=(0, 255, 0), thickness =1)
            # Display the resulting frame
            cv2.imshow('Frame', image)
            count +=1
            # Press Q on keyboard to  exit
            if cv2.waitKey(16) & 0xFF == ord('q'):
                break

        # Break the loop
        else: 
            break
    
    # When everything done, release 
    # the video capture object
    cap.release()
    
    # Closes all the frames
    cv2.destroyAllWindows()
    bvh_pos = np.array(bvh_pos)
    #np.save('videoPos',bvh_pos)
    return bvh_pos

def BVHedit(file,videopath,positions):
    basename = os.path.basename(videopath)
    video_name = basename[:basename.rfind('.')]
    new_dir_name = "D:\\tuc\\Github\\Thesis\\Code\\Output\\Videos"
    path = f'{new_dir_name}/{video_name}.bvh'

    positions = positions / 20
    data = open(file, 'r')
    Lines = data.readlines()
    motion = False
    Edited = []
    counter = 0
    firstline = True
    bvh = []
    for n,line in enumerate(Lines) :

        if ( line.__contains__('Frame Time:')):
            motion = True
            Edited.append(line)
            continue
        if motion :
            pos = line.split(" ")
            l = ''
            pos  = [float(i) for i in pos]
            if firstline:
                firstline = False
                xyz = pos[0:3] + positions[0]
                y = pos[1]

            for i in range(0,3): 
                pos[i] = positions[counter][i] - xyz[i]
                bvh.append[pos]
                # if i ==1:
                #     pos[i] = y -pos[i]
                #     pos[i] *=2000
                #     pos[i] += y 
                # else :
                #     pos[i] *=2000

            counter +=1
            for n,i in enumerate(pos):
                if n == len(pos) -1:
                    l += str(i) + '\n'
                else:
                    l += str(i) + ' '
            Edited.append(l)
        else:
            Edited.append(line)
    try:
        geeky_file = open(file, 'wt')
        frame=0
        for line in Edited:
                geeky_file.write(str(line))
        geeky_file.close()
    except:
        print("Unable to write to file")
    return bvh

def videoPath(videopath,extension):
    basename = os.path.basename(videopath)
    video_name = basename[:basename.rfind('.')]
    new_dir_name = "D:\\tuc\\Github\\Thesis\\Code\\Output\\Videos"
    path = f'{new_dir_name}/{video_name}{extension}'
    return path


def printVideo(out,path,name):
    basename = os.path.basename(name)
    video_name = basename[:basename.rfind('.')]
    new_dir_name = "D:\\tuc\\Github\\Thesis\\Code\\Output\\Videos"
    out_path = f'{new_dir_name}/{video_name}.mp4'
    img_array = []
    files = []
    #path = "C:\\Users\\msi\\Desktop\\VideoTo3dPoseAndBvh\\outputs\\outputvideo\\alpha_pose_desert\\vis\\*.jpg"
    folder = path.split('*')[0]
    counter = 0
    for filename in tqdm(glob.glob(path)):
        name= str(folder + str(counter) + '.jpg')
        files.append(name)
        counter+=1
    for filename in tqdm(files):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    
    
    out = cv2.VideoWriter(out_path,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()


    
def check():
    collect_env()
    print(torch.__version__, torch.cuda.is_available())
    print(mmdet.__version__)
    print(get_compiling_cuda_version())
    print(get_compiler_version())

def Cocomodel():
        # Choose to use a config and initialize the detector
    config = 'configs/faster_rcnn/faster_rcnn_r50_caffe_fpn_mstrain_3x_coco.py'
    # Setup a checkpoint file to load
    checkpoint = 'checkpoints/faster_rcnn_r50_caffe_fpn_mstrain_3x_coco_20210526_095054-1f77628b.pth'

    # Set the device to be used for evaluation
    device='cuda:0'

    # Load the config
    config = mmcv.Config.fromfile(config)
    # Set pretrained to be None since we do not need pretrained model here
    config.model.pretrained = None

    # Initialize the detector
    model = build_detector(config.model)

    # Load checkpoint
    checkpoint = load_checkpoint(model, checkpoint, map_location=device)

    # Set the classes of models for inference
    model.CLASSES = checkpoint['meta']['CLASSES']

    # We need to set the model's cfg for inference
    model.cfg = config

    # Convert the model to GPU
    model.to(device)
    # Convert the model into evaluation mode
    model.eval()
    return model

def detector(model,img):
    return inference_detector(model, img)

def show(model, img, result, score_thr):
    return show_result_pyplot(model, img, result, score_thr)
