import io
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import regex

# improve dpi in windows10
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)

except:
    pass

r = regex.compile(r"\d+")  # set up regex to look for digits in the lines of text
s = regex.compile("xxxx  Chapter")  # set up regex to find chapter number & verses number
part_fp = "C:\\Users\\44779\\OneDrive\\biblical hebrew\\Genesis Analysis\\"  # directory for verse files


class HbVExtract(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bible Verse Extractor")
        UserInputFrame(self).pack()


class UserInputFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        # StringVars holding book, chapter, begin verse and end verse
        self.book_entry = tk.StringVar()
        self.chapter = tk.StringVar()
        self.v_begin = tk.IntVar()
        self.v_end = tk.IntVar()
        self.v_total = tk.StringVar()

        bk_entry = tk.Entry(self, textvariable=self.book_entry)
        bk_entry.grid(row=0, column=1, sticky="W", padx=15, pady=5)

        book_label = ttk.Label(self, text="Select Book")
        book_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)

        chap_label = ttk.Label(self, text="Select Chapter")
        chap_label.grid(row=1, column=0, sticky="W", padx=5, pady=5)

        beg_label = ttk.Label(self, text="Select Start Verse")
        beg_label.grid(row=2, column=0, sticky="W", padx=5, pady=5)

        end_label = ttk.Label(self, text="Select End Verse")
        end_label.grid(row=3, column=0, sticky="W", padx=5, pady=5)

        ch_sp_box = ttk.Spinbox(self, from_=1, to=20, textvariable=self.chapter)
        ch_sp_box.grid(row=1, column=1, sticky="W", padx=15, pady=5)

        vbeg_sp_box = ttk.Spinbox(self, from_=1, to=20, textvariable=self.v_begin)
        vbeg_sp_box.grid(row=2, column=1, sticky="W", padx=15, pady=5)

        vend_sp_box = ttk.Spinbox(self, from_=1, to=20, textvariable=self.v_end)
        vend_sp_box.grid(row=3, column=1, sticky="W", padx=15, pady=5)

        bk_button = ttk.Button(self, text="Select Book", command=self.show_book)
        bk_button.grid(row=0, column=2, sticky="W", padx=15, pady=5)

        fgen_button = ttk.Button(self, text="Create Files", command=self.f_gen)
        fgen_button.grid(row=3, column=2, sticky="W", padx=15, pady=5)

    def show_book(self):
        a = filedialog.askopenfilename()  # create list from filepath
        # select filename.txt, a[1], and remove the .txt extension
        self.book_entry.set(a)  # set book_entry to required book

    # def getbook(self):
    #    print(f"You have selected, {self.book_entry.get()}")

    def f_gen(self):
        bk_title_raw = self.book_entry.get().rsplit('/', 1)  # retrieve book.txt from filepath
        bk_title = bk_title_raw[1].replace(".txt", "")  # cut off file extension for book title
        with io.open(self.book_entry.get(), "r", encoding="UTF-8") as f:  # open book file
            bk_text = f.readlines()  # read file into bk_text variable
        for verse in range(self.v_begin.get(), self.v_end.get() + 1):  # set up loop to extract required verses
            for i in range(len(bk_text)):  # set up loop to search through book for required verses
                t = r.findall(bk_text[i])  # extract current chapter and verse
                if t == [str(verse), self.chapter.get()]:  # test to see these are the requested ones
                    txt2save = regex.findall(r"\w+", bk_text[i])  # if so save verse
                    filename = part_fp + bk_title + "_" + self.chapter.get() + "_" + str(verse) + ".txt"
                    with open(filename, 'a', encoding="utf-8") as f:  # open a file for output
                        f.write('\n'.join(txt2save))  # write data one word/line, to produce a column


root = HbVExtract()
ttk.Button(root,text="exit",command=root.destroy).pack()
root.mainloop()
