import cv2


video_path = 'D:\\tuc\\Github\\Thesis\\Code\\PoseEstimation\\inputvideo\\mocap2.mp4'
cap = cv2.VideoCapture(video_path)

new_path = video_path.split(".")[0] + 'resized' +'.mp4'
print(new_path)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(new_path,fourcc, 30, (1920,1080))

while True:
    ret, frame = cap.read()
    if ret == True:
        b = cv2.resize(frame,(1920,1080),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        out.write(b)
    else:
        break
    
cap.release()
out.release()
cv2.destroyAllWindows()