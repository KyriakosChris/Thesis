# Copyright (c) 2018-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

import numpy as np
from model_functions.quaternion import qrot, qinverse
from model_functions.utils import wrap


def normalize_screen_coordinates(X, w, h):
    assert X.shape[-1] == 2

    # Normalize so that [0, w] is mapped to [-1, 1], while preserving the aspect ratio
    return X / w * 2 - [1, h / w]


def normalize_screen_coordinates_new(X, w, h):
    assert X.shape[-1] == 2

    return (X - (w / 2, h / 2)) / (w / 2, h / 2)


def image_coordinates_new(X, w, h):
    assert X.shape[-1] == 2

    # Reverse camera frame normalization
    return (X * (w / 2, h / 2)) + (w / 2, h / 2)


def image_coordinates(X, w, h):
    assert X.shape[-1] == 2

    # Reverse camera frame normalization
    return (X + [1, h / w]) * w / 2


def world_to_camera(X, R, t):
    Rt = wrap(qinverse, R)  # Invert rotation
    return wrap(qrot, np.tile(Rt, (*X.shape[:-1], 1)), X - t)  # Rotate and translate


def camera_to_world(X, R, t):
    return wrap(qrot, np.tile(R, (*X.shape[:-1], 1)), X) + t


