        # def click():
        #     if is_float(Xinput.get()) and is_float(Yinput.get()) and is_float(Zinput.get()) and self.file_name != '' and self.folder_name != '':
        #         X = float(Xinput.get())
        #         Y = float(Yinput.get())
        #         Z = float(Zinput.get())
        #         positions = (X,Y,Z)
        #         basename = os.path.basename(self.file_name)
        #         video_name = basename[:basename.rfind('.')]
        #         bvhpath = f'{self.folder_name}/{video_name}/{video_name}.bvh'
        #         videoplayer.destroy()
        #         PositionEdit(bvhpath,positions)
        #         done.config(text ="Edit completed successfully")
                
        # def is_float(element):
        #     try:
        #         float(element)
        #         return True
        #     except ValueError:
        #         return False
                
        # def open_file(offsetx,offsety):
        #     global videoplayer
        #     openbtn.config(state="disabled")
        #     videoplayer = TkinterVideo(master=window, scaled=True, pre_load=False)
        #     videoplayer.load(r"{}".format(file))
        #     videoplayer.place(x=0+offsetx, y=600, height=480, width=700)
        #     videoplayer.play()

        # def playAgain():
        #     videoplayer.play()
        
        # def Reset(offsetx,offsety):

        #     videoplayer.destroy()
        #     open_file(offsetx,offsety)

        # def PauseVideo():
        #     videoplayer.pause()
            
        # def buttonSmooth(file):
        #     Smoothbutton.config(state="disabled")
        #     fastsmooth(file)
        #     messagebox.showinfo(title="Filter Info", message="Filtering more than once may not improve further the results")
        #     Smoothbutton.config(state="normal")