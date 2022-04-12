import os
import time

from common.arguments import parse_args
from common.camera import *
from common.generators import UnchunkedGenerator
from common.loss import *
from common.model import *
from common.utils import Timer, evaluate, add_path
import cv2
from numpy import *
import numpy as np
from bvh_skeleton import h36m_skeleton,cmu_skeleton
from Bvh2Gif import *
from Model import *


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
        from joints_detectors.Alphapose.gene_npz import generate_kpts as alpha_pose
        return alpha_pose

    # def get_hr_pose():
    #     from joints_detectors.hrnet.pose_estimation.video import generate_kpts as hr_pose
    #     return hr_pose

    # def open_pose():
    #     from joints_detectors.openpose.main import generate_kpts as op_pose
    #     return op_pose

    detector_map = {
        'alpha_pose': get_alpha_pose,
        # 'hr_pose': get_hr_pose,
        # 'open_pose': open_pose
    }

    assert detector_name in detector_map, f'2D detector: {detector_name} not implemented yet!'

    return detector_map[detector_name]()


class Skeleton:
    def parents(self):
        return np.array([-1, 0, 1, 2, 0, 4, 5, 0, 7, 8, 9, 8, 11, 12, 8, 14, 15])

    def joints_right(self):
        return [1, 2, 3, 9, 10]

def main(args):
    # 第一步：检测2D关键点
    detector_2d = get_detector_2d(args.detector_2d)
    assert detector_2d, 'detector_2d should be in ({alpha, hr, open}_pose)'

    # 2D kpts loads or generate
    if not args.input_npz:
        video_name = args.viz_video
        keypoints = detector_2d(video_name)
    else:
        npz = np.load(args.input_npz)
        keypoints = npz['kpts']  # (N, 17, 2)
    #keypoints = np.load('keypoints.npy')
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
    checkpoint = torch.load(chk_filename, map_location=lambda storage, loc: storage)  # 把loc映射到storage
    model_pos.load_state_dict(checkpoint['model_pos'])

    ckpt, time2 = ckpt_time(time1)
    print('-------------- load 3D model spends {:.2f} seconds'.format(ckpt))

    #  Receptive field: 243 frames for args.arc [3, 3, 3, 3, 3]
    receptive_field = model_pos.receptive_field()
    pad = (receptive_field - 1) // 2  # Padding on each side
    causal_shift = 0

    print('Rendering...')
    input_keypoints = keypoints.copy()
    gen = UnchunkedGenerator(None, None, [input_keypoints],
                             pad=pad, causal_shift=causal_shift, augment=args.test_time_augmentation,
                             kps_left=kps_left, kps_right=kps_right, joints_left=joints_left, joints_right=joints_right)
    prediction = evaluate(gen, model_pos, return_predictions=True, )

    # save 3D joint points 
    #np.save('outputs/test_3d_output.npy', prediction, allow_pickle=True)

    rot = np.array([0.14070565, -0.15007018, -0.7552408, 0.62232804], dtype=np.float32)
    prediction = camera_to_world(prediction, R=rot, t=0)
    # We don't have the trajectory, but at least we can rebase the height
    prediction[:, :, 2] -= np.min(prediction[:, :, 2])

    prediction_copy = np.copy(prediction)
    write_standard_bvh(args.viz_output,prediction_copy) 
    bvh_file = write_smartbody_bvh(args.viz_output,prediction_copy)


    
    gif_file = os.path.join( args.new_folder,"3d_pose.mp4")
    ani = vis_3d_keypoints_sequence(
        keypoints_sequence=prediction,
        skeleton=h36m_skeleton.H36mSkeleton(),
        azimuth=np.array(45., dtype=np.float32),
        fps=60,
        output_file=gif_file
    )
    
    #HTML(ani.to_jshtml())
    XYZ = np.array(XYZ)
    x0 = XYZ[0][0]
    z0 = XYZ[0][1]
    y0 = prediction[0,0,2] + XYZ[0][2]
    for frame in range(prediction.shape[0]):
        prediction[frame][0][0] = x0-XYZ[frame][0]   # X
        prediction[frame][0][1] = z0-XYZ[frame][1]   # Z
        prediction[frame][0][2] = y0-XYZ[frame][2]   # Y
    base_Y = Calculate_Height(bvh_file)
    # rebase the height
    prediction[:, 0, 1] -= np.min(prediction[:, 0, 1]) - base_Y
    PositionsEdit(bvh_file,prediction, False)

    ckpt, time3 = ckpt_time(time2)
    print('-------------- generate reconstruction 3D data spends {:.2f} seconds'.format(ckpt))

    # ckpt, time4 = ckpt_time(time3)
    # print('total spend {:2f} second'.format(ckpt))

    
def inference_video(video_path, output_path, detector_2d):
    """
    Do image -> 2d points -> 3d points to video.
    :param detector_2d: used 2d joints detector. Can be {alpha_pose, hr_pose}
    :param video_path: relative to outputs
    :return: None
    """
    args = parse_args()

    args.detector_2d = detector_2d
    new_dir_name = output_path
    basename = os.path.basename(video_path)
    video_name = basename[:basename.rfind('.')]
    
    args.viz_video = video_path
    args.viz_output = f'{new_dir_name}/{video_name}.mp4'
    args.new_folder = f'{new_dir_name}/{video_name}'

    args.evaluate = 'pretrained_h36m_detectron_coco.bin'

    with Timer(video_path):
        main(args)


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
            cv2.imshow('Frame', image)
            # Press Q on keyboard to  exit
            if cv2.waitKey(16) & 0xFF == ord('q'):
                break

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
    :param outbvhfilepath: 输出bvh动作文件路径
    :param prediction3dpoint: 预测的三维关节点
    :return:
    '''

    # 将预测的点放大100倍
    for frame in prediction3dpoint:
        for point3d in frame:
            point3d[0] *= 100
            point3d[1] *= 100
            point3d[2] *= 100

            # 交换Y和Z的坐标
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
    cmuskeleton = h36m_skeleton.H36mSkeleton()
    cmuskeleton.poses2bvh(prediction3dpoint,output_file=bvhfileName)
    # human36m_skeleton = h36m_skeleton.H36mSkeleton()
    # human36m_skeleton.poses2bvh(prediction3dpoint,output_file=bvhfileName)

# 将3dpoint转换为SmartBody的bvh格式并输出到outputs/outputvideo/alpha_pose_视频名/bvh下
def write_smartbody_bvh(outbvhfilepath,prediction3dpoint):
    '''
    :param outbvhfilepath: 输出bvh动作文件路径
    :param prediction3dpoint: 预测的三维关节点
    :return:
    '''

    # 将预测的点放大100倍
    for frame in prediction3dpoint:
        for point3d in frame:
            # point3d[0] *= 100
            # point3d[1] *= 100
            # point3d[2] *= 100

            # 交换Y和Z的坐标
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
    cmuskeleton = h36m_skeleton.H36mSkeleton()
    cmuskeleton.poses2bvh(prediction3dpoint,output_file=bvhfileName)
    # SmartBody_skeleton = smartbody_skeleton.SmartBodySkeleton()
    # SmartBody_skeleton.poses2bvh(prediction3dpoint,output_file=bvhfileName)
    return bvhfileName

if __name__ == '__main__':
    inference_video('outputs/inputvideo/kunkun_cut_one_second.mp4',"D:\\tuc\\Github\\Thesis\\BVH" , 'alpha_pose')

