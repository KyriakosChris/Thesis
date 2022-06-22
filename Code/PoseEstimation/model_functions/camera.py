# Copyright (c) 2018-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import numpy as np
from model_functions.quaternion import qrot, qinverse
from model_functions.utils import wrap

# Normalize so that all the keypoints are mapped into [-1, 1], while preserving the aspect ratio
# we found it in stackexchange:  https://gamedev.stackexchange.com/questions/75758/how-do-i-convert-screen-coordinates-to-between-1-and-1
def normalize_screen_coordinates(X, w, h):
    assert X.shape[-1] == 2

    return (X - (w / 2, h / 2)) / (w / 2, h / 2)


def image_coordinates(X, w, h):
    assert X.shape[-1] == 2

    # Reverse camera frame normalization
    return (X * (w / 2, h / 2)) + (w / 2, h / 2)


def world_to_camera(X, R, t):
    Rt = wrap(qinverse, R)  # Invert rotation
    return wrap(qrot, np.tile(Rt, (*X.shape[:-1], 1)), X - t)  # Rotate and translate


def camera_to_world(X, R, t):
    return wrap(qrot, np.tile(R, (*X.shape[:-1], 1)), X) + t


