import os


import threading
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from tkinter import Frame, Button, Entry, Label, Tk

class Example(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background='white')
        self.directory = None
        self.text_directory = None
        self.parent = parent
        self.create_topic_menu()

    def create_topic_menu(self):
        self.text_directory = Label(text='Папка', font="ARIAL 15")
        self.text_directory.place(x=0, y=0, width=350, height=24)

        self.directory = Entry()
        self.directory.place(x=0, y=25, width=350, height=50)
        self.directory.insert(0, '/Users/kirill201/Desktop/Новая папка 3')

        self.btn_download = Button(text='Добавить водный знак', command=self.watermark)
        self.btn_download.place(x=0, y=75, height=50, width=350)

    def watermark(self):
        a = threading.Thread(target=watermark_photo,
                             args=(self.directory.get(),),
                             daemon=True
        )
        a.start()

def watermark_photo(directory):

    new_dir = directory+'_changed'
    watermark = Image.open('logo_c.png').convert('RGBA')
    if not os.path.isdir(new_dir):
        os.mkdir(new_dir)
    print(new_dir)

    for dirpath, dirnames, filenames in os.walk(directory):
        # перебрать каталоги
        new_dirpath = dirpath
        print(new_dirpath)
        if not os.path.isdir(new_dirpath):
            os.mkdir(new_dirpath)
        for dirname in dirnames:
            if not os.path.isdir(new_dir+"/"+dirname):
                os.mkdir(new_dir+"/"+dirname)
        # # перебрать файлы
        for filename in filenames:
            if not filename.startswith('.'):
                with open(os.path.join(dirpath, filename)):
                    base_image = Image.open(os.path.join(dirpath, filename))
                    width, height = base_image.size

                    transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))
                    transparent.paste(base_image, (0, 0))
                    transparent.paste(watermark, (0, 0), mask=watermark)
                    transparent.save(os.path.join(new_dir + "/" + dirpath.split('/')[-1], filename))




def startapp():
    root = Tk()
    root.title('g1car.com')
    root.geometry("350x130+0+0")
    root.resizable(False, False)
    Example(root)
    root.mainloop()

if __name__ == '__main__':
    startapp()
