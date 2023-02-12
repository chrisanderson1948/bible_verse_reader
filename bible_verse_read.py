import io
import regex
from tkinter.filedialog import askopenfilename


class HbDataExt:
    """
    To extract verses from Hebrew Bible Text files
    """
    r = regex.compile(r"\d+")  # set up regex to look for digits in the lines of text
    s = regex.compile("xxxx  Chapter")  # set up regex to find chapter number & verses number

    def __init__(self, chapter, verse_1, verse_2, filepath):
        self.chapter = chapter
        self.verse_1 = verse_1
        self.verse_2 = verse_2
        self.filepath = filepath

    def get_file(self):
        with io.open(self.filepath, "r", encoding="UTF-8") as f:
            return f.readlines()

    def get_chap_verse(self): # returns list of chapter and total verses in the chapter
        content = self.get_file()
        for i in range(len(content)):
            u = self.s.findall(content[i])  # locate chapter number and total verses
            if u == ["xxxx  Chapter"]:
                v = self.r.findall(content[i])  # extract chapter number and verses number in chapter
                if v[0] == self.chapter:
                    return v

    def get_verse_1(self):
        return self.verse_1

    def get_verse_2(self):
        return self.verse_2

    def get_chapter(self):
        return self.chapter

    def get_book(self):
        raw_book = filepath.rsplit('/', 1)  # from file path split off 'book-name'.txt
        return raw_book[1]


filepath = askopenfilename()  # filedialog to retrieve book required
chapter = input("Please enter Chapter: ")  # user i/p
verse_1 = input("Now enter start verse: ")  # user i/p
verse_2 = input("Now enter end verse: ")  # user i/p

hbdataext = HbDataExt(chapter, verse_1, verse_2, filepath)

part_fp = "C:\\Users\\44779\\OneDrive\\biblical hebrew\\Genesis Analysis\\"

book = hbdataext.get_book().replace(".txt", "")
chap_verse = hbdataext.get_chap_verse()
print('This is chapter', chap_verse[0], "of", book)
print('')
print("there are",chap_verse[1], "verses")

fd = hbdataext.get_file()
r = regex.compile(r"\d+")  # set up regex to look for 'chapter: verse' in the lines of text

for verse in range(int(verse_1), (int(verse_2) + 1)):
    for i in range(len(fd)):  # loop to find chapter and verse required by the user
        t = r.findall(fd[i])
        if t == [str(verse), chapter]:  # if chapter and verse are found
            verse_line = regex.findall(r"\w+", fd[i])
            filename = part_fp + book + "_" + chapter + "_" + str(verse) + " .txt"  # create filename for output text
            # file
            with open(filename, 'a', encoding="utf-8") as f:  # open a file for output
                f.write('\n'.join(verse_line))  # write data one word/line, to produce a column
