import os
import time
from model_functions.arguments import parse_args
from model_functions.camera import *
from model_functions.generators import UnchunkedGenerator
from model_functions.loss import *
from model_functions.model import *
from model_functions.utils import Timer, evaluate, add_path
import cv2
from numpy import *
import numpy as np
from bvh_skeleton import h36m_skeleton
from usefulTools import CorrectionOfPositions, Calculate_Height
from model_functions.visualize import *
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

metadata = {'layout_name': 'coco', 'num_joints': 17, 'keypoints_symmetry': [[1, 3, 5, 7, 9, 11, 13, 15], [2, 4, 6, 8, 10, 12, 14, 16]]}

add_path()

# record time
def ckpt_time(ckpt=None):
    if not ckpt:
        return time.time()
    else:
        return time.time() - float(ckpt), time.time()


time0 = ckpt_time()

def get_detector_2d(detector_name):
    def get_alpha_pose():
        from Alphapose.gene_npz import generate_kpts as alpha_pose
        return alpha_pose

    detector_map = {
        'alpha_pose': get_alpha_pose
    }

    assert detector_name in detector_map, f'2D detector: {detector_name} not implemented yet!'

    return detector_map[detector_name]()

def main(args):
    detector_2d = get_detector_2d(args.detector_2d)
    assert detector_2d, 'detector_2d should be alpha_pose'
    #args.input_npz = 'keypoints.npy'
    # 2D kpts loads or generate
    if not args.input_npz:
        video_name = args.viz_video
        keypoints = detector_2d(video_name)
    else:
        keypoints =np.load(args.input_npz)  # (N, 17, 2)
    XYZ = []
    poly = []
    for frame in keypoints:
        Xavg = np.average(frame[:,0])
        Yavg = np.average(frame[:,1])
        xmin = min(frame[:,0])
        ymin = min(frame[:,1])
        xmax = max(frame[:,0])
        ymax = max(frame[:,1])
        poly.append((xmin,ymin , xmax , ymax))
        A = (xmax - xmin)*(ymax - ymin)
        Zestimate = np.log2(A)
        XYZ.append((Xavg,Zestimate,Yavg))
    
    #saveVideo(args,poly,XYZ)
    keypoints_symmetry = metadata['keypoints_symmetry']
    kps_left, kps_right = list(keypoints_symmetry[0]), list(keypoints_symmetry[1])
    joints_left, joints_right = list([4, 5, 6, 11, 12, 13]), list([1, 2, 3, 14, 15, 16])

    # normlization keypoints  Suppose using the camera parameter
    keypoints = normalize_screen_coordinates(keypoints[..., :2], w=1000, h=1002)

    model_pos = TemporalModel(17, 2, 17, filter_widths=[3, 3, 3, 3, 3], causal=args.causal, dropout=args.dropout, channels=args.channels,
                              dense=args.dense)

    if torch.cuda.is_available():
        model_pos = model_pos.cuda()
    else:
        model_pos = model_pos.cpu()
    ckpt, time1 = ckpt_time(time0)
    print('-------------- load data spends {:.2f} seconds'.format(ckpt))

    # load trained model
    chk_filename = os.path.join(args.checkpoint, args.resume if args.resume else args.evaluate)
    print('Loading checkpoint', chk_filename)
    checkpoint = torch.load(chk_filename, map_location=lambda storage, loc: storage)  
    model_pos.load_state_dict(checkpoint['model_pos'])

    ckpt, time2 = ckpt_time(time1)
    print('-------------- load 3D model spends {:.2f} seconds'.format(ckpt))

    receptive_field = model_pos.receptive_field()
    pad = (receptive_field - 1) // 2  # Padding on each side
    causal_shift = 0

    input_keypoints = keypoints.copy()
    gen = UnchunkedGenerator(None, None, [input_keypoints],
                             pad=pad, causal_shift=causal_shift, augment=args.test_time_augmentation,
                             kps_left=kps_left, kps_right=kps_right, joints_left=joints_left, joints_right=joints_right)
    prediction = evaluate(gen, model_pos, return_predictions=True, )
    
    # save 3D joint points 

    rot = np.array([0.14070565, -0.15007018, -0.7552408, 0.62232804], dtype=np.float32)
    prediction = camera_to_world(prediction, R=rot, t=0)
    # We don't have the trajectory, but at least we can rebase the height
    prediction[:, :, 2] -= np.min(prediction[:, :, 2])

    prediction_copy = np.copy(prediction)
    write_standard_bvh(args.viz_output,prediction_copy) 
    bvh_file = write_smartbody_bvh(args.viz_output,prediction_copy)

    XYZ = np.array(XYZ)
    x0 = XYZ[0][0]
    z0 = XYZ[0][1]
    y0 = prediction[0,0,2] + XYZ[0][2]
    for frame in range(prediction.shape[0]):
        prediction[frame][0][0] = x0-XYZ[frame][0]   # X
        prediction[frame][0][1] = z0-XYZ[frame][1]   # Z
        prediction[frame][0][2] = y0-XYZ[frame][2]   # Y
    # rebase the height
    base_Y = Calculate_Height(bvh_file)

    # Adding some adjustments...
    prediction[:, 0, 0] /= (args.height + args.width)*0.3
    prediction[:, 0, 1] /= (args.height + args.width)*0.3
    prediction[:, 0, 2] /= (args.height + args.width)*0.3
    prediction[:, 0, 1] -= np.min(prediction[:, 0, 1]) - base_Y
    CorrectionOfPositions(bvh_file,prediction)
    video_file = os.path.join( args.new_folder,"3d_pose.mp4")
    create_video(bvh_file, video_file)

    ckpt, time3 = ckpt_time(time2)
    print('-------------- generate reconstruction 3D data spends {:.2f} seconds'.format(ckpt))

    return prediction


    
def input_video(video_path, output_path, detector_2d):
    """
    Do image -> 2d points -> 3d points to video.
    :param detector_2d: used 2d joints detector. Can be alpha_pose
    :param video_path: relative to outputs
    :return: None
    """
    args = parse_args()
    vid = cv2.VideoCapture(video_path)
    args.height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    args.width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
    args.detector_2d = detector_2d
    new_dir_name = output_path
    basename = os.path.basename(video_path)
    video_name = basename[:basename.rfind('.')]
    
    args.viz_video = video_path
    args.viz_output = f'{new_dir_name}/{video_name}.mp4'
    args.new_folder = f'{new_dir_name}/{video_name}'

    args.evaluate = 'pretrained_h36m_detectron_coco.bin'

    with Timer(video_path):
        return main(args)


def saveVideo(args,poly,xyz):
    cap = cv2.VideoCapture(args.viz_video)
    # Check if video opened successfully
    if (cap.isOpened()== False): 
        print("Error opening video  file")
    images = []
    count = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            image = cv2.circle(frame, (int(xyz[count][0]),int(xyz[count][2])), radius=4, color=(0, 0, 255), thickness=-1)
            image  = cv2.rectangle(frame, (int(poly[count][0]),int(poly[count][1])), (int(poly[count][2]),int(poly[count][3])), color=(0, 255, 0), thickness =1)
            # Display the resulting frame
            images.append(image)
            count+=1
            height, width, layers = frame.shape
            size = (width,height)

        # Break the loop
        else: 
            break
    cap.release()
    path = f'{args.new_folder}/Positionsvideo.mp4'
    out = cv2.VideoWriter(path,cv2.VideoWriter_fourcc(*'DIVX'), 60, size)
    for i in range(len(images)):
        out.write(images[i])
    out.release()


def write_standard_bvh(outbvhfilepath,prediction3dpoint):
    '''
    :param outbvhfilepath: 
    :param prediction3dpoint: 
    :return:
    '''

    for frame in prediction3dpoint:
        for point3d in frame:
            point3d[0] *= 100
            point3d[1] *= 100
            point3d[2] *= 100

            #X = point3d[0]
            #Y = point3d[1]
            #Z = point3d[2]

            #point3d[0] = -X
            #point3d[1] = Z
            #point3d[2] = Y

    dir_name = os.path.dirname(outbvhfilepath)
    basename = os.path.basename(outbvhfilepath)
    video_name = basename[:basename.rfind('.')]
    bvhfileDirectory = os.path.join(dir_name,video_name)
    if not os.path.exists(bvhfileDirectory):
        os.makedirs(bvhfileDirectory)
    bvhfileName = os.path.join(dir_name,video_name,"{}.bvh".format(video_name))
    human36m_skeleton = h36m_skeleton.H36mSkeleton()
    human36m_skeleton.poses2bvh(prediction3dpoint,output_file=bvhfileName)


def write_smartbody_bvh(outbvhfilepath,prediction3dpoint):



    for frame in prediction3dpoint:
        for point3d in frame:
            # point3d[0] *= 100
            # point3d[1] *= 100
            # point3d[2] *= 100

            X = point3d[0]
            Y = point3d[1]
            Z = point3d[2]

            point3d[0] = -X
            point3d[1] = Z
            point3d[2] = Y

    dir_name = os.path.dirname(outbvhfilepath)
    basename = os.path.basename(outbvhfilepath)
    video_name = basename[:basename.rfind('.')]
    bvhfileDirectory = os.path.join(dir_name,video_name)
    if not os.path.exists(bvhfileDirectory):
        os.makedirs(bvhfileDirectory)
    bvhfileName = os.path.join(dir_name,video_name,"{}.bvh".format(video_name))
    human36m_skeleton = h36m_skeleton.H36mSkeleton()
    human36m_skeleton.poses2bvh(prediction3dpoint,output_file=bvhfileName)
    return bvhfileName

if __name__ == '__main__':
    input_video('outputs/inputvideo/kunkun_cut_one_second.mp4',"D:\\tuc\\Github\\Thesis\\BVH" , 'alpha_pose')

