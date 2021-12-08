# coding: utf-8
## bvh parser sample script
import bvh_parser as bp

if __name__ == "__main__":
	# parse bvh file
	bvh_parser = bp.bvh("D:\\tuc\\exam10\\Thesis\\Dataset\\07_06.bvh")
	# print first frame motion data
	print(bvh_parser.motions[0])