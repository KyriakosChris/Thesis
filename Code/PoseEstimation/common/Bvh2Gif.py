import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, writers

def vis_3d_keypoints_sequence(
    keypoints_sequence, skeleton, azimuth,
    fps=30, elev=15, output_file=None
):
    kps_sequence = keypoints_sequence
    x_max, x_min = np.max(kps_sequence[:, :, 0]), np.min(kps_sequence[:, :, 0])
    y_max, y_min = np.max(kps_sequence[:, :, 1]), np.min(kps_sequence[:, :, 1])
    z_max, z_min = np.max(kps_sequence[:, :, 2]), np.min(kps_sequence[:, :, 2])
    radius = max(x_max - x_min, y_max - y_min, z_max - z_min) / 2

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.view_init(elev=elev, azim=azimuth)
    ax.set_xlim3d([-radius, radius])
    ax.set_ylim3d([-radius, radius])
    ax.set_zlim3d([0, 2 * radius])

    initialized = False
    lines = []

    def update(frame):
        nonlocal initialized

        if not initialized:
            root = skeleton.root
            stack = [root]
            while stack:
                parent = stack.pop()
                p_idx = skeleton.keypoint2index[parent]
                p_pos = kps_sequence[0, p_idx]
                for child in skeleton.children[parent]:
                    if skeleton.keypoint2index.get(child, -1) == -1:
                        continue
                    stack.append(child)
                    c_idx = skeleton.keypoint2index[child]
                    c_pos = kps_sequence[0, c_idx]
                    if child in skeleton.left_joints:
                        color = 'b'
                    elif child in skeleton.right_joints:
                        color = 'r'
                    else:
                        color = 'k'
                    line = ax.plot(
                        xs=[p_pos[0], c_pos[0]],
                        ys=[p_pos[1], c_pos[1]],
                        zs=[p_pos[2], c_pos[2]],
                        c=color, marker='.', zdir='z'
                    )
                    lines.append(line)
            initialized = True
        else:
            line_idx = 0
            root = skeleton.root
            stack = [root]
            while stack:
                parent = stack.pop()
                p_idx = skeleton.keypoint2index[parent]
                p_pos = kps_sequence[frame, p_idx]
                for child in skeleton.children[parent]:
                    if skeleton.keypoint2index.get(child, -1) == -1:
                        continue
                    stack.append(child)
                    c_idx = skeleton.keypoint2index[child]
                    c_pos = kps_sequence[frame, c_idx]
                    if child in skeleton.left_joints:
                        color = 'b'
                    elif child in skeleton.right_joints:
                        color = 'r'
                    else:
                        color = 'k'
                    lines[line_idx][0].set_xdata([p_pos[0], c_pos[0]])
                    lines[line_idx][0].set_ydata([p_pos[1], c_pos[1]])
                    lines[line_idx][0].set_3d_properties( [p_pos[2], c_pos[2]]) 
                    line_idx += 1

    anim = FuncAnimation(
        fig=fig, func=update, frames=kps_sequence.shape[0], interval=1000 / fps
    )

    if output_file:
        output_file = Path(output_file)
        if not output_file.parent.exists():
            os.makedirs(output_file.parent)
        if output_file.suffix == '.mp4':
            Writer = writers['ffmpeg']
            writer = Writer(fps=fps, metadata={}, bitrate=3000)
            anim.save(output_file, writer=writer)
        elif output_file.suffix == '.gif':
            anim.save(output_file, dpi=80, writer='imagemagick')
        else:
            raise ValueError(f'Unsupported output format.'
                             f'Only mp4 and gif are supported.')

    return anim
