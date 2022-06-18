
def remove_TPose(input):
    T_Pose = "0 0 0 -1 0 0 -1 0 0 0 0 -1 0 0 -1 0 -1 0 1 0 0 0 0 -1 0 0 -1 0 -1 0 0 0 1 0 0 1 0 0 1 0 0 1 1 0 0 1 0 0 1 0 0 1 0 0 -1 0 0 -1 0 0 -1 0 0 -1 0 0"
    with open(input) as f:
        data = f.readlines()
    
    f.close()
    for i in range(len(data)): 
        if T_Pose in data[i]:
            data[i]= ""
            data[i-2] = data[i-2].split(" ")[0] + " " + str(int(data[i-2].split(" ")[1])-1) + "\n"
            break  
        i+=1
    try:
        file = open(input, 'wt')
        for line in data:
                file.write(str(line))
        file.close()
    except:
        print("Unable to write to file")    

remove_TPose("D:\\tuc\\Github\\Thesis\\BVH\cxk\\cxk.bvh")