
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report
from sklearn import metrics
import warnings
warnings.filterwarnings('ignore')


from tkinter import *
from PIL import Image,ImageTk
global root
root = Tk()
root.title('TERRORIST ATTACK PREDICTION')
root.geometry('1500x750')
img=Image.open("a.jpg")
img=img.resize((1500,750))
bg=ImageTk.PhotoImage(img)

import joblib

# Load the trained model from the file
rfc_loaded = joblib.load('decision_tree_model.pkl')
lbl=Label(root,image=bg)
lbl.place(x=0,y=0)

label = Label( root, text = 'TERRORIST ATTACK PREDICTION',font=('arial',24,'bold'),bd=20,background="#CDD954")
label.place(x=300,y=10)



label_1 = Label(root, text ='month',font=("Helvetica", 18),background="#CDD954")
label_1.place(x=300,y=100)
    
Entry_1= Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_1.place(x=600,y=100)



label_2 = Label(root, text ='Date',font=("Helvetica", 16),background="#CDD954")
label_2.place(x=300,y=160)
    
Entry_2 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_2.place(x=600,y=160)

label_2 = Label(root, text ='Date',font=("Helvetica", 16),background="#CDD954")
label_2.place(x=300,y=220)
    
Entry_3 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_3.place(x=600,y=220)


label_4 = Label(root, text ='latitude',font=("Helvetica", 18),background="#CDD954")
label_4.place(x=300,y=290)
    
Entry_4= Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_4.place(x=600,y=290)



label_5 = Label(root, text ='longitude',font=("Helvetica", 18),background="#CDD954")
label_5.place(x=300,y=350)
    
Entry_5 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_5.place(x=600,y=350)



label_6 = Label(root, text ='multiple',font=("Helvetica", 18),background="#CDD954")
label_6.place(x=300,y=400)
    
Entry_6 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_6.place(x=600,y=400)

label_9 = Label(root, text ='attackType',font=("Helvetica", 18),background="#CDD954")
label_9.place(x=300,y=500)
    
Entry_9 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_9.place(x=600,y=500)


label_11 = Label(root, text ='targetType',font=("Helvetica", 18),background="#CDD954")
label_11.place(x=300,y=550)
    
Entry_11 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_11.place(x=600,y=550)


label_12 = Label(root, text ='individual',font=("Helvetica", 18),background="#CDD954")
label_12.place(x=300,y=600)
    
Entry_12 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_12.place(x=600,y=600)

label_13 = Label(root, text ='weaponType',font=("Helvetica", 18),background="#CDD954")
label_13.place(x=300,y=650)
    
Entry_13 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_13.place(x=600,y=650)


label_14 = Label(root, text ='nkill',font=("Helvetica", 18),background="#CDD954")
label_14.place(x=300,y=700)
    
Entry_14 = Entry(root,font=("Helvetica", 18),justify=CENTER)
Entry_14.place(x=600,y=700)

def acc():
    image = Image.open("result.jpg")
    image = image.resize((300, 300), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(image)  
    global panel1
    panel1 = Button(root10, image=img,command=close_acc)
    panel1.image = img
    panel1.place(x=575,y=220)
def clear_out():
    out_img.destroy()
    output.configure(text="")
    Entry_1.delete(0,END)
    Entry_2.delete(0,END)
    Entry_4.delete(0,END)
    Entry_5.delete(0,END)
    Entry_6.delete(0,END)
    Entry_9.delete(0,END)
    Entry_11.delete(0,END)
    Entry_12.delete(0,END)
    Entry_13.delete(0,END)
    Entry_14.delete(0,END)    
    

def predict():
    month = Entry_1.get()
    date = Entry_2.get()
    latitude =Entry_4.get()
    longitude =Entry_5.get()
    multiple =Entry_6.get()  
    attackType = Entry_9.get()
    targetType = Entry_11.get()
    individual = Entry_12.get()
    weaponType =Entry_13.get()
    nkill =Entry_14.get()
    out = rfc_loaded.predict([[month, date,latitude, longitude, multiple, attackType, targetType, individual, weaponType, nkill]])

    text=""
    if out == 1:
        text="The attack based on these features would be successful."
    elif out == 0:
        text="The attack based on these features would NOT be successful."
    output.configure(text=str(text))
    
b1 = Button(root, text = 'predict',font=("Helvetica", 18),background="#CDD954",command = predict)
b1.place(x=800,y=350)
    

output = Label(root,font=("Helvetica", 18),justify=CENTER)
output.place(x=600,y=650)

    
root.mainloop()


#############################################################################################################






