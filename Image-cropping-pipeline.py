
# coding: utf-8

# In[213]:


import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import matplotlib.image as mpimg
import os
import glob


# In[266]:


class data_loader(object):
    def __init__(self,images_directory):
        self.paths=os.listdir(images_directory) #individual paths for each image. directory where the images are located is needed
        self.images_data_list = {index:plt.imread(images_directory+path) for index,path in zip(range(0,len(self.paths)),self.paths)} # This is a list of numpy arrays for each of the images
        self.cropped_data={}
        self.stiched_data={}
        self.row_crop_range= [i for i in range(0,2449,306)]
        self.col_crop_range= [j for j in range(0,2449,306)]

    def crop_single_image(self,image_number):
        self.cropped_data[image_number]=[] # list of cropped images. Assume images 2448*2448*3
        i_crop = self.row_crop_range
        j_crop = self.col_crop_range
        counter=0
        image=self.images_data_list[image_number]
        for col in range(0,7):
            for row in range(0,7):
                temp = image[i_crop[row]:i_crop[row+2],j_crop[col]:j_crop[col+2],:]
                mpimg.imsave("image number %s part %s.png"%(image_number,counter), temp)
                self.cropped_data[image_number].append(temp)
                counter=counter+1

    def crop_all_images(self):
        for image_number in self.images_data_list.keys():
            self.crop_single_image(image_number)
            
    def stich_single_image(self,image_number):
        stiched = np.zeros((2448,2448,3))
        counter=0
        i_crop = self.row_crop_range
        j_crop = self.col_crop_range
        for col in range(0,7):
            for row in range(0,7):
                temp=self.cropped_data[image_number][counter]
                stiched[i_crop[row]:i_crop[row+2],j_crop[col]:j_crop[col+2],:]=stiched[i_crop[row]:i_crop[row+2],j_crop[col]:j_crop[col+2],:] + temp
                counter=counter+1

        stiched[306:2142,306:2142,:]=stiched[306:2142,306:2142,:]//4
        stiched[0:306,306:2142,:]=stiched[0:306,306:2142,:]//2
        stiched[2142:2448,306:2142,:]=stiched[2142:2448,306:2142,:]//2
        stiched[306:2142,0:306,:]=stiched[306:2142,0:306,:]//2
        stiched[306:2142,2142:2448,:]=stiched[306:2142,2142:2448,:]//2
        mpimg.imsave("stiched %s.png"%(image_number), stiched)
        self.stiched_data[image_number]=stiched
        
    def stich_all_images(self):
        for image_number in self.cropped_data.keys():
            self.stich_single_image(image_number)


# In[267]:


direc = "/home/native/projects/ML536/FinalProject/foo/"
d = data_loader(direc)
d.crop_all_images()
d.stich_all_images()
