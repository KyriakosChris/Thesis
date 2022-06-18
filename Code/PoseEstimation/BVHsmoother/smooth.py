import numpy as np
import cv2
import BVHsmoother.code_bvh.freqfilter as freqfilter
import BVHsmoother.code_bvh.bvh as bvh
import BVHsmoother.code_bvh.spacefilter as spacefilter
import BVHsmoother.code_bvh.angle as angle

class smooth:

    def __init__(self, filename, out , filter ,order , border, uo , mean , sigma ):
        INPUT = filename
        OUTPUT = out
        FILTER = filter
        ORDER  = order
        BORDER = border 
        U0 = uo
        SIGMA = sigma
        M = mean
        if M is not None:
            if (M%2 ==0): # M must be odd number
                M+=1
        bvh_file = bvh.read_file(INPUT)
        for i in range(0, 3):
            v = bvh_file["POSITIONS"][:,i]
            if FILTER == "average": bvh_file["POSITIONS"][:,i] = spacefilter.apply_average(v,M)
            #if FILTER == "average": bvh_file["POSITIONS"][:,i] =cv2.medianBlur(v, M)
            else:
                f = freqfilter.fft(v,BORDER)
                if FILTER == "gaussian": fil = freqfilter.gaussian_filter(len(f),SIGMA)
                if FILTER == "butterworth": fil = freqfilter.butter_worth_filter(len(f),U0,ORDER)
                ff = freqfilter.apply_filter(f,fil)
                iff = freqfilter.ifft(ff,BORDER)
                bvh_file["POSITIONS"][:,i] = np.real(iff)

        bvh.write_file(OUTPUT,bvh_file)
        bvh_file = bvh.read_file(INPUT)
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