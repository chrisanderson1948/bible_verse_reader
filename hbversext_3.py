import io
import tkinter as tk
from tkinter import ttk, font
from tkinter import filedialog
import regex
from ctypes import windll

windll.shcore.SetProcessDpiAwareness(1)

r = regex.compile(r"\d+")  # set up regex to look for digits in the lines of text
s = regex.compile("xxxx  Chapter")  # set up regex to find chapter number & verses number
# part_fp = "C:\\Users\\44779\\OneDrive\\biblical hebrew\\Genesis Analysis\\"  # directory for verse files


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
        self.v_total = tk.IntVar()
        self.outfile_dir = tk.StringVar()
        bk_entry = tk.Entry(self, textvariable=self.book_entry)
        bk_entry.grid(row=0, column=1, sticky="W", padx=15, pady=5)
        book_label = ttk.Label(self, text="Select Book")
        book_label.grid(row=0, column=0, sticky="W", padx=5, pady=5)

        chap_label = ttk.Label(self, text="Chapter")
        chap_label.grid(row=1, column=0, sticky="W", padx=5, pady=5)
        beg_label = ttk.Label(self, text="Start Verse")
        beg_label.grid(row=2, column=0, sticky="W", padx=5, pady=5)
        end_label = ttk.Label(self, text="End Verse")
        end_label.grid(row=3, column=0, sticky="W", padx=5, pady=5)
        # v_tot_label = ttk.Label(self, text="Last Chapter Verse")
        # v_tot_label.grid(row=4, column=0, sticky="W", padx=5, pady=5)

        # the extra 'self.' prefixes are necessary to get the spin boxes to update, using config. method in
        # get_verse_total()

        self.ch_sp_box = ttk.Spinbox(self, from_=1, to=100, textvariable=self.chapter, command=self.get_verse_total)
        self.ch_sp_box.grid(row=1, column=1, sticky="W", padx=15, pady=5)

        self.vbeg_sp_box = ttk.Spinbox(self, from_=1, to=100, textvariable=self.v_begin)
        self.vbeg_sp_box.grid(row=2, column=1, sticky="W", padx=15, pady=5)

        self.vend_sp_box = ttk.Spinbox(self, from_=1, to=100, textvariable=self.v_end, command=self.validate_vend)
        self.vend_sp_box.grid(row=3, column=1, sticky="W", padx=15, pady=5)

        bk_button = ttk.Button(self, text="Select Book", command=self.show_book)
        bk_button.grid(row=0, column=2, sticky="W", padx=15, pady=5)

        self.fgen_button = ttk.Button(self, text="Create Files", state='disabled', command=self.f_gen, )
        self.fgen_button.grid(row=3, column=2, sticky="W", padx=15, pady=5)

    def show_book(self):
        a = filedialog.askopenfilename()  # create list from filepath
        b = filedialog.askdirectory()  # create directory for output files
        # select filename.txt, a[1], and remove the .txt extension
        self.book_entry.set(a)  # set book_entry to required book
        self.outfile_dir.set(b)  # write directory string for output files to outfile_dir

    def get_verse_total(self):
        with io.open(self.book_entry.get(), "r", encoding="UTF-8") as f:  # open book file
            bk_text = f.readlines()  # read file into bk_text variable
        for i in range(0, len(bk_text)):
            u = s.findall(bk_text[i])  # locate chapter number and total verses
            if u == ["xxxx  Chapter"]:
                z = r.findall(bk_text[i])  # extract chapter number and verses number in chapter
                if z[0] == self.chapter.get():
                    self.v_total.set(z[1])
                    self.vbeg_sp_box.config(to=z[1])
                    self.vend_sp_box.config(to=z[1])

    def validate_vend(self):  # check that last verse number is not less than the first verse number
        if self.v_end.get() >= self.v_begin.get():
            self.fgen_button["state"] = "normal"
        else:
            self.fgen_button["state"] = "disabled"

    def f_gen(self):
        bk_title_raw = self.book_entry.get().rsplit('/', 1)  # retrieve book.txt from filepath
        bk_title = bk_title_raw[1].replace(".txt", "")  # cut off file extension for book title
        with io.open(self.book_entry.get(), "r", encoding="UTF-8") as f:  # open book file
            bk_text = f.readlines()  # read file into bk_text variable
        for verse in range(self.v_begin.get(), self.v_end.get() + 1):  # set up loop to extract required verses
            for i in range(0, len(bk_text)):  # set up loop to search through book for required verses
                t = r.findall(bk_text[i])  # extract current chapter and verse
                if t == [str(verse), self.chapter.get()]:  # test to see these are the requested ones
                    txt2save = regex.findall(r"\w+", bk_text[i])  # if so save verse
                    filename = self.outfile_dir.get()+ "/" + bk_title + "_" + \
                               self.chapter.get() + "_" + str(verse) + ".txt "
                    with open(filename, 'a', encoding="UTF-8") as f:  # open a file for output
                        f.write('\n'.join(txt2save))  # write data one word/line, to produce a column


root = HbVExtract()
font.nametofont("TkDefaultFont").configure(size=15)
ttk.Button(root, text="Exit", command=root.destroy).pack()
root.mainloop()
