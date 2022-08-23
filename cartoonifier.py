#import the libraries
import cv2 as cv
import matplotlib.pyplot as plt 
import easygui
import sys
import os
import tkinter as tk
#from tkinter import filedialog
from tkinter import *
#Making the main window
top=tk.Tk()
top.geometry('400x400')
top.title('cartonnify your img')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))

def upload():
    imagpath=easygui.fileopenbox()
    cartonnify(imagpath)
def cartonnify(imagpath):  
    OriginalImag=cv.imread(imagpath)
    if  OriginalImag is None:
        print('no imag was found , choose the fille properly')
        sys.exit()
    # to plot the imag using matplotlib 
    OriginalImag1=cv.cvtColor(OriginalImag,cv.COLOR_BGR2RGB)
    resized1=cv.resize(OriginalImag1,(960, 540))
    #transform our img to grayscal for apply or processing 
    GrayImag=cv.cvtColor(OriginalImag,cv.COLOR_BGR2GRAY)
    resized2=cv.resize(GrayImag,(960, 540))
    #blur the img using the medianBlur to strongly remove the noise and the detail if the imag
    BlurredImag=cv.medianBlur(GrayImag,5)
    resized3=cv.resize(BlurredImag,(960, 540))
    #retreive  the egdes
    ImagEdg=cv.adaptiveThreshold(BlurredImag,255,cv.ADAPTIVE_THRESH_MEAN_C,cv.THRESH_BINARY,9,9)
    resized4=cv.resize(ImagEdg,(960, 540))
    #get the base of the cartoon effect
    Bilimg=cv.bilateralFilter(OriginalImag,9,300,300)
    resized5=cv.resize(Bilimg,(960, 540))
    # the cartonnified img
    CartonImg=cv.bitwise_and(Bilimg,Bilimg,mask= ImagEdg)
    resized6=cv.resize(CartonImg,(960, 540))
    list_of_img=[resized1,resized2,resized3,resized4,resized5,resized6]
    lise_of_name=['OriginalImag','GrayImag',' BlurredImag','ImagEdg','Bilimg','CartonImg']
    fig,axes=plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for name ,img , axe in zip(lise_of_name,list_of_img,axes.flat):
        axe.imshow(img, cmap='gray')
        axe.set_title(name)
    
    #Making a Save button in the main window
    save1=Button(top,text="Save cartoon image",command=lambda:save(resized6, imagpath),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    plt.show()
#Functionally of save button  
def save(resized6, imagpath):
    #saving an image using imwrite()
    newName=os.path.splitext(imagpath)[0]+' '+ 'cartoonified '
    path1 = os.path.dirname(imagpath)
    extension=os.path.splitext(imagpath)[1]
    path = os.path.join(path1, newName+extension)
    cv.imwrite(path, cv.cvtColor(resized6, cv.COLOR_RGB2BGR))
    I = "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)       

#Making the Cartoonify button in the main window
upload=Button(top,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)     
#Main function to build the tkinter window
top.mainloop()