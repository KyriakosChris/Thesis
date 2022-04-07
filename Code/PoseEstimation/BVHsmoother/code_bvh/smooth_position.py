import numpy as np
import freqfilter
import bvh
import sys
import args
import spacefilter
import angle

class smooth:

    def __init__(self,smooth_type):
        ARGS = args.get()
        INPUT = ARGS["-i"]
        OUTPUT = ARGS["-o"]
        FILTER = ARGS["--filter"]

        if FILTER == "butterworth":
            ORDER = int(ARGS["--order"])
            U0 = int(ARGS["--u0"])
            BORDER = int(ARGS["--border"])
        if FILTER == "gaussian":
            SIGMA = int(ARGS["--sigma"])
            BORDER = int(ARGS["--border"])
        if FILTER == "average":
            M = int(ARGS["-m"])

        bvh_file = bvh.read_file(INPUT)
        if smooth_type == 'pos':
            for i in range(0, 3):
                v = bvh_file["POSITIONS"][:,i]
                if FILTER == "average": bvh_file["POSITIONS"][:,i] = spacefilter.apply_average(v,M)
                else:
                    f = freqfilter.fft(v,BORDER)
                    if FILTER == "gaussian": fil = freqfilter.gaussian_filter(len(f),SIGMA)
                    if FILTER == "butterworth": fil = freqfilter.butter_worth_filter(len(f),U0,ORDER)
                    ff = freqfilter.apply_filter(f,fil)
                    iff = freqfilter.ifft(ff,BORDER)
                    bvh_file["POSITIONS"][:,i] = np.real(iff)

            bvh.write_file(OUTPUT,bvh_file)

        if smooth_type == 'rot':
            for j in range(len(bvh_file["ROTATIONS"][0,:,0])):
                for i in range(3):
                    v = angle.floats_to_degrees(bvh_file["ROTATIONS"][:,j,i])
                    p = angle.degrees_to_polars(v)
                    if FILTER == "average": f_filtered = spacefilter.apply_average(p, M)
                    else:
                        f = freqfilter.fft(p,BORDER)
                        if FILTER == "gaussian": fil = freqfilter.gaussian_filter(len(f), SIGMA)
                        if FILTER == "butterworth": fil = freqfilter.butter_worth_filter(len(f), U0, ORDER)
                        f_filtered = freqfilter.apply_filter(f,fil)
                        f_filtered = freqfilter.ifft(f_filtered,BORDER)
                    p = angle.complexes_to_polars(f_filtered)
                    nv = angle.polars_to_degrees(p)
                    bvh_file["ROTATIONS"][:,j,i] = nv

            bvh.write_file(OUTPUT, bvh_file)

ARGS = args.get()
INPUT = ARGS["-i"]
OUTPUT = ARGS["-o"]
FILTER = ARGS["--filter"]
if FILTER == "butterworth":
    ORDER = int(ARGS["--order"])
    U0 = int(ARGS["--u0"])
    BORDER = int(ARGS["--border"])
if FILTER == "gaussian":
    SIGMA = int(ARGS["--sigma"])
    BORDER = int(ARGS["--border"])
if FILTER == "average":
    M = int(ARGS["-m"])

bvh_file = bvh.read_file(INPUT)

for i in range(0, 3):
    v = bvh_file["POSITIONS"][:,i]
    if FILTER == "average": bvh_file["POSITIONS"][:,i] = spacefilter.apply_average(v,M)
    else:
        f = freqfilter.fft(v,BORDER)
        if FILTER == "gaussian": fil = freqfilter.gaussian_filter(len(f),SIGMA)
        if FILTER == "butterworth": fil = freqfilter.butter_worth_filter(len(f),U0,ORDER)
        ff = freqfilter.apply_filter(f,fil)
        iff = freqfilter.ifft(ff,BORDER)
        bvh_file["POSITIONS"][:,i] = np.real(iff)

bvh.write_file(OUTPUT,bvh_file)
