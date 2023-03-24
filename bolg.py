
import tkinter as tk
import cv2
import numpy as np
import mss
from PIL import Image
from PIL import ImageTk



reference_images = [
    {"img": cv2.imread("/Users/MilesC/Desktop/bolg/image1.jpg", cv2.IMREAD_GRAYSCALE)},
]
fallback_img = cv2.imread("/Users/MilesC/Desktop/bolg/image2.jpg")
fallback_img = cv2.resize(fallback_img, None, fx=2, fy=2)

root = tk.Tk()
root.overrideredirect(True)
root.attributes('-topmost', True)
root.attributes('-alpha', 0.9)

label = tk.Label(root)
root.geometry('104x104+1400+600')
label.pack()

def update_label():
    
    with mss.mss() as sct:
        
        screen = np.array(sct.grab({"top": 680, "left": 1100, "width": 400, "height": 300})) #area of my buff bar

    
    gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    
    found = []
    for reference in reference_images:
        result = cv2.matchTemplate(gray, reference['img'], cv2.TM_CCOEFF_NORMED)
        threshold = 0.99
        loc = np.where(result >= threshold)
        if len(loc[0]) > 0:
            found.append(reference)

    if found:
        
        found_img = screen[loc[0][0]:loc[0][0]+reference['img'].shape[0]+25, 
                   loc[1][0]-29:loc[1][0]+reference['img'].shape[1]]

        
        found_img = cv2.resize(found_img, None, fx=2, fy=2)
        found_img = cv2.cvtColor(found_img, cv2.COLOR_BGR2RGB)
        found_img = Image.fromarray(found_img)
        found_img = ImageTk.PhotoImage(found_img)
        
        label.config(image=found_img)
        label.image = found_img
    else:
        
        fallback_img_pil = cv2.cvtColor(fallback_img, cv2.COLOR_BGR2RGB)
        fallback_img_pil = Image.fromarray(fallback_img_pil)
        fallback_img_pil = ImageTk.PhotoImage(fallback_img_pil)
        
        label.config(image=fallback_img_pil)
        label.image = fallback_img_pil

    

    
    root.after(200, update_label)


root.after(200, update_label)


root.mainloop()