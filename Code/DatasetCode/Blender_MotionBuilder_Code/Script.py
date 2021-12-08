##Set Your Root Dir   
root = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_FBX\\"
out = "D:\\tuc\\exam10\\Thesis\\Dataset\\CMU_BVH\\"
##A Simple Function That Will Open A File Within MotionBuilder And Print Out the Take Names
def OpenFileAndListTakes(files):
    from pyfbsdk import FBApplication, FBSystem
    ##Open .fbx file
    FBApplication().FileOpen(files)
    #Export the .bvh file
    bvh_path = out+"\\"+files.split(".fbx")[0].split("\\")[6]+".bvh"
    FBApplication().FileExport(bvh_path)
     
'''
Below is a simple example on how to search a folder (the "root" variable listed above) for ".fbx" files
'''
##Creat A Function That Will Search The Root Dir for .fbx Files    
def ListFolderContent():
    import sys,os
    path = os.path.join(root, "targetdirectory")
    for path, subdirs, files in os.walk(root):
        ##Added Variables For Folders That We Want to Omit
        '''
        MotionBuilder Can Automatically Create (Backups And Media) folders, by skipping them it will allow us to not process unwanted data
        '''
        lFBM = ".fbm"
        lBck = ".bck"
        ##If The Folder Or Sub Folder Contains ".fbm" or ".bck" Within It
        if lFBM in path or lBck in path:
            pass
        ##If The Folder Or Sub Folder Does Not Contain ".fbm" or ".bck" Within It
        else:
            for name in files:
                ##Set A Variable To Isolate Each Files Extention
                extension = os.path.splitext(name)[1]
                ##Define What To Do With Files That Have The Extention ".fbx"
                if extension == ".fbx":
                    lfbxfile = os.path.join(path, name)
                    '''
                    This is where you state what you want to do to the .fbx file found.
                    '''
                    OpenFileAndListTakes(lfbxfile)
                ##Define What To Do With Files Found That Have Another Extention    
                else:
                    pass
 
##Run Function
ListFolderContent()