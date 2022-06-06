T_Pose = {
    'Hip': [0, 0, 0],
    'RightHip': [-1, 0, 0],
    'RightKnee': [0, 0, -1],
    'RightAnkle': [0, 0, -1],
    'RightAnkleEndSite': [0, -1, 0],
    'LeftHip': [1, 0, 0],
    'LeftKnee': [0, 0, -1],
    'LeftAnkle': [0, 0, -1],
    'LeftAnkleEndSite': [0, -1, 0],
    'Spine': [0, 0, 1],
    'Thorax': [0, 0, 1],
    'Neck': [0, 0, 1],
    'HeadEndSite': [0, 0, 1],
    'LeftShoulder': [1, 0, 0],
    'LeftElbow': [1, 0, 0],
    'LeftWrist': [1, 0, 0],
    'LeftWristEndSite': [1, 0, 0],
    'RightShoulder': [-1, 0, 0],
    'RightElbow': [-1, 0, 0],
    'RightWrist': [-1, 0, 0],
    'RightWristEndSite': [-1, 0, 0]
}
s = ''
for value in T_Pose.values():
    
    for dir in value:
        s+= str(dir) + ' ' 
print(s[:-1])