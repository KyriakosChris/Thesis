import sys

import torch
import torch._utils
import torch.nn as nn
import torch.utils.data
import torch.utils.data.distributed

from Alphapose.SPPE.src.models.FastPose import createModel
from Alphapose.SPPE.src.utils.img import flip, shuffleLR

try:
    torch._utils._rebuild_tensor_v2
except AttributeError:
    def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
        tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
        tensor.requires_grad = requires_grad
        tensor._backward_hooks = backward_hooks
        return tensor
    torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2

class InferenNet_fast(nn.Module):
    def __init__(self, kernel_size, dataset):
        super(InferenNet_fast, self).__init__()

        #model = createModel().cpu()
        model = createModel().cuda()
        model.load_state_dict(torch.load('Alphapose/models/sppe/duc_se.pth',map_location=torch.device('cpu')))
        model.eval()
        self.pyranet = model

        self.dataset = dataset

    def forward(self, x):
        out = self.pyranet(x)
        out = out.narrow(1, 0, 17)

        return out
