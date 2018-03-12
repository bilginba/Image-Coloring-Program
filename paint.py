""""
    Author: Batuhan Bilgin
    Last Modified: 3/6/2018
    Version: 1.0
    Description: COMP 204 Project#1
"""
import PIL.Image
from PIL import ImageTk
from tkinter.colorchooser import *
from tkinter.filedialog import *
import random


root = Tk()
root.title("Online Coloring")
root.geometry("1600x800")
root.configure(background='LightSkyBlue1')
root.attributes('-fullscreen', True)

label = 0
row_size = 0
column_size = 0
label_values = None
pixel_values = None
target_image = None
img = None
pix = []
palette_pix = []
color_palette_image = None
color_palette_label = None
palette_row_size = 0
palette_column_size = 0


# Path selection
def open_file():
    path = askopenfilename(parent=root, filetypes=(("PNG File", "*.png"), ("JPEG File", "*.jpeg"), ("JPG File", "*.jpg")),
                           title="Select File")
    image_operation(path)
    eight_connected_labeling(pixel_values, label_values, column_size, row_size)


# Image process steps
def image_operation(path):
    global target_image
    global row_size
    global column_size
    global pix
    global pixel_values
    global label_values
    global img

    # if the path is not given return
    try:
        if path is not None:

            fp = open(path, "rb")
            target_image= PIL.Image.open(fp) # Opens image with the selected path
            if target_image.size > (1000,1000): # Resizes image if it is bigger than (1000,1000)=(width,height)
                target_image = target_image.resize((1000,1000))
            render = ImageTk.PhotoImage(target_image)

            pix = target_image.load() # Reach pixel values of the image
            row_size, column_size = target_image.size

            # Creates image label if there is no image label on the screen. Otherwise, destroys the old label and
            # creates new image label
            if img is None:
                img = Label(root, image=render)
                img.image = render
                img.place(x=800, y=500, anchor="center")

                img.bind("<Button-1>", paint_coordinates)
            else:
                img.destroy()
                img = Label(root, image=render)
                img.image = render
                img.place(x=800, y=500, anchor="center")

                img.bind("<Button-1>", paint_coordinates)


            for i in range(row_size):
                for j in range(column_size):
                    pix[i, j] = vanish_noises_from_pixel(pix[i, j])


            pixel_values = [[0 for x in range(column_size)] for y in range(row_size)]
            for i in range(row_size):
                for j in range(column_size):
                    pixel_values[i][j] = convert_to_binary_value(pix[i, j])

            # Makes the edges of pixel_values to black
            for i in range(row_size):
                for j in range(column_size):
                    if i == 0 or j == 0 or i == row_size - 1 or j == column_size - 1:
                        pixel_values[i][j] = 0

            # Makes the edges of label_values to black
            label_values = [[0 for x in range(column_size)] for y in range(row_size)]
            for i in range(row_size):
                for j in range(column_size):
                    label_values[i][j] = 0
    except:
        return


# If pixel has white color it returns 1, otherwise it returns 0
def convert_to_binary_value(rgbValues):
    if len(rgbValues) == 4:
        r, g, b, o = rgbValues
    else:
        r, g, b = rgbValues
    average = (r + g + b) / 3
    if average == 255:
        return 1  # means white
    return 0  # means black


# Makes the pix values black or white. It removes all pixel colors except black and white.
def vanish_noises_from_pixel(rgbValues):
    if len(rgbValues) == 4:
        r, g, b, o = rgbValues
    else:
        r, g, b = rgbValues
    average = (r + g + b) / 3
    if average > 200:
        return 255, 255, 255
    return 0, 0, 0


"""
    LABELING ALGORITHM
    ----------------------------------------------------------------------------------------------------
    If the current pixel value is white 
        if only one pixel is white
            set current label to neighbor's label
        else if two pixels are white
            if the labels are equal
                set current label to one of the neighbor's label
            else
                set current label to same neighbor's label
                look all pixel and change labels which are not the selected neighbor to neighbor's label 
        else if three pixels are white
            if the labels are equal
                set current label to one of the neighbor's label
            else
                set current label to same neighbor's label
                look all pixel and change labels which are not the selected neighbor to neighbor's label 
        else
            increase the label value
            set current label to label value
    else 
        set black pixels label value to 1
    ----------------------------------------------------------------------------------------------------
"""


7
# Labeling Process
def eight_connected_labeling(pixel_values, label_values, column_size, row_size):
    global label
    label = 2
    for i in range(1, row_size - 1):
        for j in range(1, column_size - 1):
            p_u = pixel_values[i - 1][j]
            p_l = pixel_values[i][j - 1]
            p_ul = pixel_values[i - 1][j - 1]
            p_ur = pixel_values[i - 1][j + 1]

            l_l = label_values[i][j - 1]
            l_ul = label_values[i - 1][j - 1]
            l_u = label_values[i - 1][j]
            l_ur = label_values[i - 1][j + 1]

            if pixel_values[i][j] == 1: # If the pixel is white
                if p_l == 1 and p_ul == 0 and p_u == 0 and p_ur == 0:  # 1000
                    label_values[i][j] = l_l
                elif p_l == 0 and p_ul == 1 and p_u == 0 and p_ur == 0:  # 0100
                    label_values[i][j] = l_ul
                elif p_l == 0 and p_ul == 0 and p_u == 1 and p_ur == 0:  # 0010
                    label_values[i][j] = l_u
                elif p_l == 0 and p_ul == 0 and p_u == 0 and p_ur == 1:  # 0001
                    label_values[i][j] = l_ur
                elif p_l == 1 and p_ul == 1 and p_u == 0 and p_ur == 0:  # 1100
                    if l_l == l_ul:
                        label_values[i][j] = l_ul
                    else:
                        label_values[i][j] = l_ul
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_l:
                                    label_values[m][n] = l_ul
                elif p_l == 0 and p_ul == 1 and p_u == 1 and p_ur == 0:  # 0110
                    if l_ul == l_u:
                        label_values[i][j] = l_ul
                    else:
                        label_values[i][j] = l_ul
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_u:
                                    label_values[m][n] = l_ul
                elif p_l == 0 and p_ul == 0 and p_u == 1 and p_ur == 1:  # 0011
                    if l_u == l_ur:
                        label_values[i][j] = l_u
                    else:
                        label_values[i][j] = l_u
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_ur:
                                    label_values[m][n] = l_u
                elif p_l == 1 and p_ul == 0 and p_u == 1 and p_ur == 0:  # 1010
                    if l_l == l_u:
                        label_values[i][j] = l_u
                    else:
                        label_values[i][j] = l_u
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_l:
                                    label_values[m][n] = l_u
                elif p_l == 0 and p_ul == 1 and p_u == 0 and p_ur == 1:  # 0101
                    if l_ul == l_ur:
                        label_values[i][j] = l_ul
                    else:
                        label_values[i][j] = l_ul
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_ur:
                                    label_values[m][n] = l_ul
                elif p_l == 1 and p_ul == 0 and p_u == 0 and p_ur == 1:  # 1001
                    if l_l == l_ur:
                        label_values[i][j] = l_ur
                    else:
                        label_values[i][j] = l_ur
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_l:
                                    label_values[m][n] = l_ur
                elif p_l == 0 and p_ul == 1 and p_u == 1 and p_ur == 1:  # 0111
                    if l_ul == l_u == l_ur:
                        label_values[i][j] = l_ul
                    else:
                        label_values[i][j] = l_ul
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_u or label_values[m][n] == l_ur:
                                    label_values[m][n] = l_ul
                elif p_l == 1 and p_ul == 1 and p_u == 1 and p_ur == 0:  # 1110
                    if l_l == l_ul == l_u:
                        label_values[i][j] = l_ul
                    else:
                        label_values[i][j] = l_ul
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_l or label_values[m][n] == l_u:
                                    label_values[m][n] = l_ul
                elif p_l == 1 and p_ul == 1 and p_u == 0 and p_ur == 1:  # 1101
                    if l_l == l_ul == l_ur:
                        label_values[i][j] = l_ul
                    else:
                        label_values[i][j] = l_ul
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_l or label_values[m][n] == l_ur:
                                    label_values[m][n] = l_ul
                elif p_l == 1 and p_ul == 0 and p_u == 1 and p_ur == 1:  # 1011
                    if l_l == l_u == l_ur:
                        label_values[i][j] = l_u
                    else:
                        label_values[i][j] = l_u
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_l or label_values[m][n] == l_ur:
                                    label_values[m][n] = l_u
                elif p_l == 1 and p_ul == 1 and p_u == 1 and p_ur == 1:  # 1111
                    if l_l == l_ul == l_u == l_ur:
                        label_values[i][j] = l_ul
                    else:
                        label_values[i][j] = l_ul
                        for m in range(0, i + 1):
                            for n in range(0, column_size - 1):
                                if label_values[m][n] == l_l or label_values[m][n] == l_u or label_values[i][j] == l_ur:
                                    label_values[m][n] == l_ul
                else:
                    label_values[i][j] = label
                    label += 1
            else:
                label_values[i][j] = 1


# Clears the paint made by user
def clean_paint():
    global row_size
    global column_size
    global label_values
    global pixel_values

    # if there is no image, return
    try:
        if target_image is not None:
            for i in range(1, row_size - 1):
                for j in range(1, column_size - 1):
                    if pixel_values[i][j] != 0:
                        target_image.putpixel((i, j), (255, 255, 255, 1))
                        pix[i, j] = (255, 255, 255, 1)
            newimage = ImageTk.PhotoImage(target_image)
            img.configure(image=newimage)
            img.image = newimage
    except:
        return


# Saves file to selected path
def save_file():
    global target_image
    savepath = asksaveasfilename(filetypes=(("PNG File", "*.png"), ("JPG File", "*.jpg")),
                                 defaultextension=".png",
                                 title="Select File")

    # if there is no image or path, return
    try:
        if savepath is not None:
            if target_image is not None:
                target_image.save(savepath)
    except:
        return


# Color picker widget
def get_color_from_color_chooser():
    global color
    chosen_color = askcolor()

    # if there is no chosen color, return
    try:
        if chosen_color is not None:
            old_color_string = str(chosen_color)
            color_string = old_color_string.replace("(", "").replace(")", "")
            color_string = re.sub(', \'.*', '', color_string)
            r, g, b = color_string.split(", ")
            r = int(float(r))
            g = int(float(g))
            b = int(float(b))
            color = (r, g, b)
            selected_color(color)

    except:
        return


# According to coordinates selects color value
def get_color_from_palette(event):
    global color_palette_image
    global color_palette_label
    global palette_pix
    global palette_row_size
    global palette_column_size
    global color

    # if there is no color_palette_image, return
    try:
        if color_palette_image is not None:
            for i in range(1, palette_row_size - 1):
                for j in range(1, palette_column_size - 1):
                    # FIRST ROW
                    if 37 >= event.x >= 12 and 37 >= event.y >= 12:
                        color = (0, 0, 0)
                    elif 87 >= event.x >= 62 and 37 >= event.y >= 12:
                        color = (128, 64, 0)
                    elif 137 >= event.x >= 112 and 37 >= event.y >= 12:
                        color = (253, 0, 0)
                    elif 187 >= event.x >= 162 and 37 >= event.y >= 12:
                        color = (254, 106, 0)
                    elif 237 >= event.x >= 212 and 37 >= event.y >= 12:
                        color = (255, 216, 0)
                    elif 287 >= event.x >= 262 and 37 >= event.y >= 12:
                        color = (0, 255, 1)
                    # SECOND ROW
                    elif 37 >= event.x >= 12 and 87 >= event.y >= 62:
                        color = (84, 84, 84)
                    elif 87 >= event.x >= 62 and 87 >= event.y >= 62:
                        color = (64, 30, 0)
                    elif 137 >= event.x >= 112 and 87 >= event.y >= 62:
                        color = (128, 0, 1)
                    elif 187 >= event.x >= 162 and 87 >= event.y >= 62:
                        color = (128, 52, 0)
                    elif 237 >= event.x >= 212 and 87 >= event.y >= 62:
                        color = (128, 107, 0)
                    elif 287 >= event.x >= 262 and 87 >= event.y >= 62:
                        color = (1, 127, 1)
                    # THIRD ROW
                    elif 37 >= event.x >= 12 and 137 >= event.y >= 112:
                        color = (168, 168, 168)
                    elif 87 >= event.x >= 62 and 137 >= event.y >= 112:
                        color = (1, 255, 255)
                    elif 137 >= event.x >= 112 and 137 >= event.y >= 112:
                        color = (0, 148, 254)
                    elif 187 >= event.x >= 162 and 137 >= event.y >= 112:
                        color = (0, 38, 255)
                    elif 237 >= event.x >= 212 and 137 >= event.y >= 112:
                        color = (177, 0, 254)
                    elif 287 >= event.x >= 262 and 137 >= event.y >= 112:
                        color = (255, 0, 110)
                    # FOURTH ROW
                    elif 37 >= event.x >= 12 and 187 >= event.y >= 162:
                        color = (255, 255, 255)
                    elif 87 >= event.x >= 62 and 187 >= event.y >= 162:
                        color = (1, 127, 126)
                    elif 137 >= event.x >= 112 and 187 >= event.y >= 162:
                        color = (0, 73, 126)
                    elif 187 >= event.x >= 162 and 187 >= event.y >= 162:
                        color = (0, 18, 128)
                    elif 237 >= event.x >= 212 and 187 >= event.y >= 162:
                        color = (89, 0, 128)
                    elif 287 >= event.x >= 262 and 187 >= event.y >= 162:
                        color = (127, 0, 55)
                    else:
                        return
        selected_color(color)

    except:
        pass


# Paint targeted area with mouse interaction
def paint_coordinates(event):
    global pix
    global pixel_values
    global label_values
    global row_size
    global column_size
    global color
    global target_image
    global img

    # if there is no image and no color, return
    try:
        if target_image is not None:
            if color is not None:
                for i in range(1, row_size - 1):
                    for j in range(1, column_size - 1):
                        if pixel_values[i][j] != 0:
                            if label_values[i][j] == label_values[event.x][event.y]:
                                if pix[i, j] != color:
                                    pix[i, j] = color
    except:
        return

    new_image = ImageTk.PhotoImage(target_image)
    img.configure(image=new_image)
    img.image = new_image


# colors the pixels randomly
def color_randomly():
    global pix
    global pixel_values
    global label_values
    global row_size
    global column_size
    global color
    global label
    global target_image

    for k in range(0, label):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        for i in range(1, row_size - 1):
            for j in range(1, column_size - 1):
                if (pixel_values[i][j] == 1):
                    if (label_values[i][j] == k):
                        color = r, g, b
                        pix[i, j] = color

    random_colored_image = ImageTk.PhotoImage(target_image)
    img.configure(image=random_colored_image)
    img.image = random_colored_image


# generates and displays palette
def generate_palette():
    global color_palette_image
    global color_palette_label
    global palette_pix
    global palette_row_size
    global palette_column_size

    color_palette_image = PIL.Image.open("palette_menu/colorpalette.png")
    rendered_palette = ImageTk.PhotoImage(color_palette_image)

    palette_pix = color_palette_image.load()
    palette_row_size, palette_column_size = color_palette_image.size

    color_palette_label = Label(root, image=rendered_palette, borderwidth=2, relief="solid")
    color_palette_label.image = rendered_palette
    color_palette_label.place(rely=0, relx=1.0, x=0, y=0, anchor=NE)

    color_palette_label.bind("<Button-1>", get_color_from_palette)


# Shows current selected color
def selected_color(color):
    hex_color = '#%02x%02x%02x' % color
    if color > (153, 153, 153):
        selected_color = Label(root, bg=hex_color, width=12, height=2, text="Selected Color", fg='black', borderwidth=2,
                               relief="solid")
    else:
        selected_color = Label(root, bg=hex_color, width=12, height=2, text="Selected Color", fg="white", borderwidth=2,
                               relief="solid")
    selected_color.grid(row=12, column=0)


# clears the screen
def empty_page():
    global img
    if img is not None:
        img.destroy()


# button and menu creation
def main():
    palette_background_label = Label(root, width=43, height=100, bg='aquamarine', borderwidth=2, relief="solid", padx=0).place(rely=0, relx=1.0, x=0, y=0, anchor=NE)
    generate_palette()

    buttons_menu = Frame(root)
    buttons_menu.grid(row=0, column=0)


    browse_label_image = PhotoImage(file="button_titles/browse.png")
    random_color_label = Label(buttons_menu, width=90, image=browse_label_image, height=9, bg='LightSkyBlue1').grid(
        row=0, column=0)

    browse_file_image = PhotoImage(file="buttons/file_explorer.png")
    browse_file_button = Button(buttons_menu, width=90, image=browse_file_image, height=90, command=open_file, bg='white').grid(
        row=1, column=0)

    save_label_image = PhotoImage(file="button_titles/save.png")
    save_label = Label(buttons_menu, width=90, image=save_label_image, height=15, bg='LightSkyBlue1').grid(
        row=2, column=0)

    save_image = PhotoImage(file="buttons/save_file.png")
    save_button = Button(buttons_menu, width=90, image=save_image, height=90, command=save_file, bg='white').grid(
        row=3, column=0)

    palette_label_image = PhotoImage(file="button_titles/palette.png")
    palette_label = Label(buttons_menu, width=90, image=palette_label_image, height=9, bg='LightSkyBlue1').grid(
        row=4, column=0)

    palette_image = PhotoImage(file="buttons/palette2.png")
    palette_button = Button(buttons_menu, width=90, image=palette_image, height=90, command=get_color_from_color_chooser, bg='white').grid(
        row=5, column=0)

    random_color_label_image = PhotoImage(file="button_titles/color_randomize.png")
    random_color_label = Label(buttons_menu, width=90, image=random_color_label_image, height=9, bg='LightSkyBlue1').grid(
        row=6, column=0)

    random_coloring_image = PhotoImage(file="buttons/random_coloring_image.png")
    random_color_button = Button(buttons_menu, width=90, image=random_coloring_image, height=90, command=color_randomly,
                               bg='white').grid(
        row=7, column=0)

    clean_label_image = PhotoImage(file="button_titles/clean.png")
    clean_label = Label(buttons_menu, width=90, image=clean_label_image, height=12, bg='LightSkyBlue1').grid(
        row=8, column=0)

    clean_image = PhotoImage(file="buttons/cleanpaint.png")
    clean_button = Button(buttons_menu, width=90, image=clean_image, height=90, command=clean_paint,
                         bg='white').grid(
        row=9, column=0)

    emptypage_label_image = PhotoImage(file="button_titles/empty_page.png")
    emptypage_label = Label(buttons_menu, width=90, image=emptypage_label_image, height=12, bg='LightSkyBlue1').grid(
        row=10, column=0)

    emptypage_image = PhotoImage(file="buttons/newpage.png")
    emptypage_button = Button(buttons_menu, width=90, image=emptypage_image, height=90, command=empty_page,
                         bg='white').grid(
        row=11, column=0)
    menu = Menu(root)
    root.config(menu=menu)

    file = Menu(menu)
    edit = Menu(menu)

    menu.add_cascade(label='File', menu=file)
    menu.add_cascade(label='Edit', menu=edit)

    # FILE COMMANDS
    file.add_command(label='Open', command=open_file)
    file.add_command(label='Save', command=save_file)
    file.add_command(label='Exit', command=lambda: exit())

    # EDIT COMMANDS
    edit.add_command(label='Color Random', command=color_randomly)
    edit.add_command(label='Clean Paint', command=clean_paint)
    edit.add_command(label='New Page', command=empty_page)

    root.mainloop()


if __name__ == '__main__':
    main()
