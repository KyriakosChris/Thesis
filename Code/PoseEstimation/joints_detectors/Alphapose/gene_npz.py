import ntpath
import os
import shutil

import numpy as np
import torch.utils.data
from progress_Bar.bar import *
from SPPE.src.main_fast_inference import *
from common.utils import calculate_area
from dataloader import DetectionLoader, DetectionProcessor, DataWriter, Mscoco, VideoLoader
from fn import getTime
from opt import opt

args = opt
args.dataset = 'coco'
args.fast_inference = False
args.save_img = True
args.sp = True
if not args.sp:
    torch.multiprocessing.set_start_method('forkserver', force=True)
    torch.multiprocessing.set_sharing_strategy('file_system')



def generate_kpts(video_file):
    final_result, video_name = handle_video(video_file)

    # ============ Changing ++++++++++

    kpts = []
    no_person = []
    for i in range(len(final_result)):
        if not final_result[i]['result']:  # No people
            no_person.append(i)
            kpts.append(None)
            continue

        kpt = max(final_result[i]['result'],
                  key=lambda x: x['proposal_score'].data[0] * calculate_area(x['keypoints']), )['keypoints']

        kpts.append(kpt.data.numpy())

        for n in no_person:
            kpts[n] = kpts[-1]
        no_person.clear()

    for n in no_person:
        kpts[n] = kpts[-1]

    # ============ Changing End ++++++++++
    kpts = np.array(kpts).astype(np.float32)


    return kpts


def handle_video(video_file):
    # =========== common ===============
    args.video = video_file
    base_name = os.path.basename(args.video)
    video_name = base_name[:base_name.rfind('.')]
    # =========== end common ===============

    # =========== video ===============
    dir_name = os.path.dirname(video_file)
    dir_name_split = dir_name[:dir_name.rfind('/')]
    new_dir_name = os.path.join(dir_name_split, 'outputvideo')

    #args.outputpath = f'outputs/alpha_pose_{video_name}'
    args.outputpath = new_dir_name + f'/alpha_pose_{video_name}'

    # if os.path.exists(args.outputpath):
    #     shutil.rmtree(f'{args.outputpath}/vis', ignore_errors=True)
    # else:
    #     os.mkdir(args.outputpath)
    videofile = args.video
    mode = args.mode
    if not len(videofile):
        raise IOError('Error: must contain --video')
    # Load input video
    data_loader = VideoLoader(videofile, batchSize=args.detbatch).start()
    (fourcc, fps, frameSize) = data_loader.videoinfo()
    print('the video is {} f/s'.format(fps))
    # =========== end video ===============
    # Load detection loader
    print('Loading YOLO model..')
    sys.stdout.flush()
    det_loader = DetectionLoader(data_loader, batchSize=args.detbatch).start()
    #  start a thread to read frames from the file video stream
    det_processor = DetectionProcessor(det_loader).start()
    # Load pose model
    pose_dataset = Mscoco()
    if args.fast_inference:
        pose_model = InferenNet_fast(4 * 1 + 1, pose_dataset)
    else:
        pose_model = InferenNet(4 * 1 + 1, pose_dataset)
    #pose_model.cpu()
    pose_model.cuda()
    pose_model.eval()
    runtime_profile = {
        'dt': [],
        'pt': [],
        'pn': []
    }
    # Data writer
    save_path = os.path.join(args.outputpath, 'AlphaPose_' + ntpath.basename(video_file).split('.')[0] + '.avi')

    writer = DataWriter(args.save_video).start()
    print('Start pose estimation...')
    batchSize = args.posebatch
    n = data_loader.length()  # or however many loading slots you want to have
    loading = '.' * n  # for strings, * is the repeat operator
    for i in IncrementalBar('Processing').iter(range(data_loader.length())):

        start_time = getTime()
        with torch.no_grad():
            (inps, orig_img, im_name, boxes, scores, pt1, pt2) = det_processor.read()
            if orig_img is None:
                print(f'{i}-th image read None: handle_video')
                break
            if boxes is None or boxes.nelement() == 0:
                writer.save(None, None, None, None, None, orig_img, im_name.split('/')[-1])
                continue

            ckpt_time, det_time = getTime(start_time)
            runtime_profile['dt'].append(det_time)
            # Pose Estimation

            datalen = inps.size(0)
            leftover = 0
            if datalen % batchSize:
                leftover = 1
            num_batches = datalen // batchSize + leftover
            hm = []
            for j in range(num_batches):
                #inps_j = inps[j * batchSize:min((j + 1) * batchSize, datalen)].cpu()
                inps_j = inps[j * batchSize:min((j + 1) * batchSize, datalen)].cuda()
                hm_j = pose_model(inps_j)
                hm.append(hm_j)
            hm = torch.cat(hm)
            ckpt_time, pose_time = getTime(ckpt_time)
            runtime_profile['pt'].append(pose_time)

            hm = hm.cpu().data
            #hm = hm.cuda().data
            writer.save(boxes, scores, hm, pt1, pt2, orig_img, im_name.split('/')[-1])

            ckpt_time, post_time = getTime(ckpt_time)
            runtime_profile['pn'].append(post_time)

    while writer.running():
        pass            
    writer.stop()
    final_result = writer.results()

    return final_result, video_name


