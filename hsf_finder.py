import tkinter
import customtkinter as ctk
from PIL import Image
from constants import Constants
import pyautogui
from time import sleep
from PIL import ImageTk,ImageGrab
import numpy as np
from math import pow
from modules.windowcapture import WindowCapture

class Interface(ctk.CTk):
    def __init__(self,title):
        super().__init__()
        self.title(title)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.attributes('-fullscreen',True)

class InstructionFrame(ctk.CTkFrame):
    count = 0
    def __init__(self,master):
        super().__init__(master,fg_color="transparent")
        self.master = master
        instruction_str =  """1. Open brawl stars on bluestacks, select the brawler that you wish use and go to the training ground.
        \n2. Take a screenshot after proceeding. You can use up scroll wheel to zoom into the image and assist with drawing the line.
        \n3. Draw a line from the middle of the player tag to the middle of the bottom circle as shown on the right
        \n4. Calculate HSF and modify it on constants.py"""
        title = ctk.CTkLabel(self,text="HSF Finder",font=("Arial Bold",25))
        instruction_textbox = ctk.CTkTextbox(self,font=("Arial",17),width=400,height=250)
        proceed_button = ctk.CTkButton(self,text="Proceed",height=50,font=("Arial Bold",20),command=self.goto_hsf_frame,fg_color="#00C04B",hover_color="#008631")
        exit_button = ctk.CTkButton(self,text="Exit",height=50,font=("Arial Bold",20),command=self.exit,fg_color="#FF474C",hover_color="#AA2F33")
        gif_file_path = "control\\hsf_resize.gif"   
        im = Image.open(gif_file_path)        
        self.frame_count = im.n_frames
        self.frames = [tkinter.PhotoImage(file=gif_file_path,format = 'gif -index %i' %(i)) for i in range(self.frame_count)]
        self.canvas = tkinter.Canvas(self,width=im.size[0],height=im.size[1])
        
        self.message = tkinter.StringVar()
        message_label = ctk.CTkLabel(self,textvariable=self.message,font=("Arial Bold", 12))

        title.grid(row=1,column=0,padx=10,pady=10,sticky="W")
        instruction_textbox.grid(row=2,column=0,padx=10,columnspan=2)
        instruction_textbox.insert(ctk.END, instruction_str)
        instruction_textbox.configure(state="disabled")
        exit_button.grid(row=3,column=0,padx=10,pady=15)
        proceed_button.grid(row=3,column=1,padx=10,pady=15)
        self.canvas.grid(row=2,column=2,padx=10,pady=10)
        self.after(0, self.update, 0)

        message_label.grid(row=4,column=0,columnspan=2,padx=10,pady=10)
    
    def update(self,index):
        frame = self.frames[index]
        index += 1
        if index == self.frame_count:
            index = 0
        self.canvas.create_image(0, 0, image=frame, anchor="nw")
        self.after(100, self.update, index)
    
    def goto_hsf_frame(self):
        try:
            wincap = WindowCapture(Constants.window_name)
            self.place_forget()
            hsf = HeightScaleFactorFrame(root,self,wincap)
            hsf.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        except Exception:
            self.count +=1
            if self.count <= 1:
                self.message.set("Please open bluestacks and try again!")
            else:
                self.message.set("""Please open bluestacks and try again!
                                    \nIf you have bluestacks open please go 
                                    \nto constants.py and change the window 
                                    \nname to the name located on the top 
                                    \nleft corner of bluestacks.""")
    
    def exit(self):
        self.master.destroy()

class HeightScaleFactorFrame(ctk.CTkFrame):
    line =None
    counter = 0
    zoom_counter = 0
    is_brawler_present = False
    def __init__(self,master,instruction_frame,wincap):
        super().__init__(master,fg_color="transparent")
        self.master = master
        self.instruction_frame = instruction_frame
        self.wincap = wincap
        # get window dimension
        self.windowSize = self.wincap.get_dimension()
        self.scale = (1222+687)/(self.wincap.w + self.wincap.h)
        self.max_width = int(0.2*self.wincap.w)*self.scale
        self.max_height = int(0.4*self.wincap.h)*self.scale
        self.zoom_increment = 0.1
        # canvas
        self.canvas_width = 3*self.max_width
        self.canvas_height = 3*self.max_height
        self.canvas = tkinter.Canvas(self,width= self.canvas_width,
                                     height=self.canvas_height,bg="white")
        # combobox
        combobox_label = ctk.CTkLabel(self,text="Zoom")
        self.zoom = ctk.StringVar()
        zoom_combobox = ctk.CTkComboBox(self,values=["1 (zoom level)","2 (zoom level)","3 (zoom level)"],variable=self.zoom,state="readonly")
        zoom_combobox.set("2 (zoom level)")

        # buttons
        button_height = 50
        screenshot_button = ctk.CTkButton(self,text="Take screenshot",height=button_height,font=("Arial Bold",15),
                                          command=self.take_screenshot)
        reset_button = ctk.CTkButton(self,text="Reset line",height=button_height,font=("Arial Bold",15),
                                     command=self.delete_line)
        confirm_button = ctk.CTkButton(self,text="Caculate HSF",height=button_height,font=("Arial Bold",15),
                                       command=self.caculate_hsf)
        back_button = ctk.CTkButton(self,text="Return to instruction",height=button_height,font=("Arial Bold",15),
                                       command=self.goback)
        # message
        hsf_label = ctk.CTkLabel(self,text="HeightScaleFactor: ",font=("Arial Bold", 20))
        self.hsf = tkinter.StringVar()
        hsf_out_label = ctk.CTkLabel(self,textvariable=self.hsf,font=("Arial", 20))
        self.message = tkinter.StringVar()
        message_label = ctk.CTkLabel(self,textvariable=self.message,font=("Arial Bold", 12),text_color="red")
        
        # first row
        message_label.grid(row=1, column=0,columnspan=10, pady=5, padx=10,sticky="W")
        # second row
        button_row = 2
        reset_button.grid(row=button_row, column=0, pady=5, padx=10,sticky="W")
        screenshot_button.grid(row=button_row, column=1, pady=5, padx=10,sticky="W")
        confirm_button.grid(row=button_row, column=2, pady=5, padx=10,sticky="W")
        back_button.grid(row=button_row, column=10, pady=5, padx=10,sticky="E")
        
        # combobox_label.grid(row=button_row+1, column=1,columnspan=2, pady=5, padx=20, sticky="WS")
        zoom_combobox.grid(row=button_row+2, column=10,columnspan=2, pady=5,sticky="N")
        hsf_label.grid(row=button_row+1, column=0,rowspan=2, pady=5,sticky="E")
        hsf_out_label.grid(row=button_row+1, column=1,rowspan=2,pady=5,sticky="W")
        self.canvas.grid(row=button_row+3, column=0, columnspan=11, pady=5)
        self.canvas.old_coords = None
        
        # binding
        self.canvas.bind('<ButtonPress-3>', self.draw_single_line)
        self.canvas.bind("<MouseWheel>",self.zoom_with_scroll)
        zoom_combobox.bind('<<ComboboxSelected>>', self.reset_all)
       
    def zoom_with_scroll(self,event):
        # scroll up
        if event.delta > 0:
            self.zoom_counter +=1
            self.canvas.delete("all")
            self.line = None
            img_w,img_h = self.img.size
            zoom_size = 1 + self.zoom_increment
            zoom_w = int(zoom_size*img_w)
            zoom_h = int(zoom_size*img_h)
            self.img = self.img.resize((zoom_w,zoom_h))
            
            if img_w > self.canvas_width and img_h > self.canvas_height:
                resize_w, resize_h = self.img.size
                midpoint = (int(resize_w/2), int(resize_h/2))
                topleft = self.subtract_tuple(midpoint,(img_w/2,img_h/2))
                bottomright = self.add_tuple(midpoint,(img_w/2,img_h/2))
                self.img = self.img.crop(topleft+bottomright)

            # convert the screenshot to a tkinter format
            screenshot = ImageTk.PhotoImage(self.img)
            image1 = tkinter.Label(self, image=screenshot)
            image1.image = screenshot
            # put image on the canvas
            self.canvas.create_image(int(self.canvas_width/2),int(self.canvas_height/2),
                                    anchor=tkinter.CENTER,image=screenshot)

    def take_screenshot(self,delay=0.25):
        self.is_brawler_present = False
        self.zoom_counter = 0
        #delete everything on the canvas
        self.canvas.delete("all")
        self.line = None
        # set target window
        self.wincap.set_window()
        # add a delay for the screenshot
        sleep(delay)
        # take a screenshot
        screenshot_region = (self.wincap.offset_x,self.wincap.offset_y,
                             self.wincap.w+self.wincap.offset_x,
                             self.wincap.h+self.wincap.offset_y)
        
        screenshot =  ImageGrab.grab(screenshot_region)
        zoom_size = int(float(self.zoom.get().replace(" (zoom level)","")))
        midpoint = (int(self.wincap.offset_x+self.wincap.w/2), int((self.wincap.h/2)- self.wincap.offset_y))
        topleft = self.subtract_tuple(midpoint,tuple([(4-zoom_size)*x for x in(self.max_width/2,self.max_height/2)]))
        bottomright = self.add_tuple(midpoint,tuple([(4-zoom_size)*x for x in(self.max_width/2,self.max_height/2)]))
        screenshot_cropped = screenshot.crop(topleft+bottomright)
        width, height = screenshot_cropped.size

        self.img = screenshot_cropped_resize = screenshot_cropped.resize((int(zoom_size*width),int(zoom_size*height))) 
        # convert the screenshot to a tkinter format
        screenshot = ImageTk.PhotoImage(screenshot_cropped_resize)
        image1 = tkinter.Label(self, image=screenshot)
        image1.image = screenshot
        # put image on the canvas
        self.canvas.create_image(int(self.canvas_width/2),int(self.canvas_height/2),
                                anchor=tkinter.CENTER,image=screenshot)
        sleep(delay)
        # go back to tkinter window
        self.focus_force()
        # press a random key to release the button
        pyautogui.press("a")

    def draw_single_line(self,event):
        self.x, self.y = event.x, event.y
        if self.counter%2 ==0:
            self.canvas.delete(self.line)
            self.line = None
        elif self.canvas.old_coords:
            self.x1, self.y1 = self.canvas.old_coords
            self.line = self.canvas.create_line(self.x, self.y, self.x1, self.y1, width=5,fill="red")
        self.canvas.old_coords = self.x, self.y
        self.counter += 1
    
    def caculate_hsf(self):
        if self.line:
            hsf = abs(self.y-self.y1)/(self.windowSize[1]*int(self.zoom.get().replace(" (zoom level)",""))*pow(1+self.zoom_increment,self.zoom_counter))
            hsf = round(hsf,3)
            self.hsf.set(hsf)
            self.message.set(" ")
        else:
            display_str = "Cannot calculate HSF, please right click to draw the line."
            self.message.set(display_str)

    def delete_line(self):
        self.canvas.old_coords = None
        self.canvas.delete(self.line)
        self.line = None
        self.hsf.set("")
    
    def reset_all(self,event):
        self.delete_line()
        self.canvas.delete("all")

    def subtract_tuple(self,tup1,tup2):
        return tuple(np.subtract(tup1, tup2))

    def add_tuple(self,tup1,tup2):
        return tuple(map(sum, zip(tup1, tup2)))

    def goback(self):
        self.place_forget()
        self.instruction_frame.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

if __name__ == '__main__':
    root = Interface("Height Scale Factor Finder")
    instruct = InstructionFrame(root)
    instruct.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
    root.mainloop()