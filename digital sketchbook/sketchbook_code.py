# type: ignore
# ruff: noqa
from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename
from PIL import Image , ImageDraw , ImageTk

import time
window=Tk()
bg_images={}
window.title("celeste's canvas")
window.geometry("500x600")

canvas=Canvas(window,bg="white",height=350,width=450)
canvas.pack(fill=BOTH, expand=True)

button_frame=Frame(window)
button_frame.pack(side=BOTTOM)

tool_frame=Frame(window)
tool_frame.pack(side=LEFT, fill=Y)

brush_size=5
current_color="black"
current_page =1
total_pages = 5

page_label = Label(
    window,
    text=f"Page: {current_page}/{total_pages}",
    font=("Arial", 12)
)
page_label.pack()

sketchbook_data = {
    1:{"lines":[], "image" : None},
    2:{"lines":[], "image" : None},
    3:{"lines":[], "image" : None},
    4:{"lines":[], "image" : None},
    5:{"lines":[], "image" : None}
}
current_stroke = []

last_x, last_y =None, None
def draw(event):
    global last_x, last_y

    if last_x is not None:
        canvas.create_line(last_x,last_y,event.x,event.y,
                           width=brush_size,fill=current_color,
                           capstyle=ROUND,smooth=True)    
        current_stroke.append(
    (
        last_x,last_y,event.x,event.y,
        current_color,brush_size
    )
)
    last_x,last_y = event.x,event.y


def reset(event):
    global last_x, last_y, current_stroke
    if current_stroke:
     sketchbook_data[current_page]["lines"].append(current_stroke)
     current_stroke = []
    last_x=None
    last_y=None

def load_page():
    global bg_images
    page_label.config(text=f"page: {current_page}/{total_pages}")
    canvas.config(width=450)
    canvas.delete("all")

    img_path = sketchbook_data[current_page]["image"]
    if img_path:
        try:
            img = Image.open(img_path)
            img = img.resize((450, 350), Image.Resampling.LANCZOS)
            
            bg_images[current_page] = ImageTk.PhotoImage(img)
            
            canvas.create_image(225, 175, image=bg_images[current_page])
        except Exception as e:
            print("Can not load the image:", e)

for stroke in sketchbook_data[current_page]["lines"]:
        for line in stroke:
            x1,y1,x2,y2,color,size=line
            canvas.create_line(
                x1,y1,x2,y2,
                width=size,
                fill=color,
                capstyle=ROUND,
                smooth=True
            )

def red():
    global current_color
    current_color="red"

Button(button_frame,text="Red",command=red).pack(side=LEFT)

def blue():
    global current_color
    current_color="blue"

Button(button_frame,text="blue",command=blue).pack(side=LEFT)

def green():
    global current_color
    current_color="green"

Button(button_frame,text="green",command=green).pack(side=LEFT)

def black():
    global current_color
    current_color="black"

Button(button_frame,text="black",command=black).pack(side=LEFT)

def eraser():
    global current_color
    current_color="white"

Button(button_frame,text="eraser",command=eraser).pack(side=LEFT)

def clear():
    canvas.delete("all")

Button(button_frame,text='clear',command=clear).pack(side=LEFT)

def small():
    global brush_size
    brush_size = 2

def medium():
    global brush_size
    brush_size = 5

def large():
    global brush_size
    brush_size = 10

Button(tool_frame,text='small',command=small).pack()
Button(tool_frame,text='medium',command=medium).pack()
Button(tool_frame,text='large',command=large).pack()

def choose_color():
    global current_color
    color= askcolor()[1]

    if color:
        current_color = color

Button(tool_frame, text="Color", command=choose_color).pack()

def save():
    file = asksaveasfilename(defaultextension=".png")

    if file:
        image = Image.new("RGB", (500, 450), "white")
        draw_image = ImageDraw.Draw(image)

        for stroke in sketchbook_data[current_page]:
           for line in stroke:
            x1, y1, x2, y2, color, size = line

            draw_image.line(
            (x1, y1, x2, y2),
            fill=color,
            width=size
            )

        image.save(file)
       

Button(tool_frame, text="save", command=save).pack()

def undo():
    if sketchbook_data[current_page]["lines"]:
        sketchbook_data[current_page]["lines"].pop()
    
    load_page()

Button(tool_frame, text="undo", command=undo).pack()

def flip_animation():
    for w in range(450,-1,-30):
       canvas.config(width=w)
       window.update()
       time.sleep(0.01)

    load_page()

    for w in range(0,450,30):
        canvas.config(width=w)
        window.update()
        time.sleep(0.01)

def next_page():
    global current_page, last_x, last_y
    if current_page < total_pages:
        current_page += 1
        last_x, last_y = None, None 
        flip_animation()
    else:
        print("This is the last page")

def prev_page():
    global current_page, last_x, last_y
    if current_page > 1:
        current_page -= 1
        last_x, last_y = None, None  
        flip_animation()
    else:
        print("This is the first page")

Button(tool_frame,text="◀ Prev Page", command=prev_page, bg="#e67e22", fg="white").pack()
Button(tool_frame,text="Next Page ▶", command=next_page, bg="#e67e22", fg="white").pack()

canvas.bind("<B1-Motion>", draw)
canvas.bind("<ButtonRelease-1>", reset)

load_page()
window.mainloop()
