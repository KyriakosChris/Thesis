# Thesis Abstrack
Motion capture methods are either very expensive to acquire or of poorer quality. Thus, we propose an innovative method that will give access to everyone that has an above-average computer, to generate for free their single-person digital motion clips.  Recently, many researchers try to use neural networks that will estimate the 3D human pose from a single video. In our approach, we decided to use three different well-known pre-trained models, the first two to find the 2D pose estimation from each frame of the video, and the other to convert these 2D poses into 3D poses. Then, we estimated the position of the human per frame, by calculating the depth of the person in the image. The combination of the 3D poses and the position is the motion data that we wanted to find. Then, by importing these data into a Skeleton that contains all the estimated bones, we can create a  Bio-vision Hierarchy (BVH) file, that can be imported into the 3D computer graphics software tool-set. At this point, the generated BVH file contains noise from the neural networks, so we propose using some filters to remove this noise without affecting the motion data information. Furthermore, we converted the raw python code into a Windows Application to create a very friendly user environment. Finally, we created some functions inside this application so that the user can visually, and edit the results from the BVH files. 

# How to run 
