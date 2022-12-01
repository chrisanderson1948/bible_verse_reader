import io
import regex
from tkinter.filedialog import askopenfilename


class HBVerseExtractor:
    """
    To extract verses from Hebrew Bible Text files
    """
    r = regex.compile(r"\d+")  # set up regex to look for digits in the lines of text
    s = regex.compile("xxxx  Chapter")  # set up regex to chapter number & verses number

    def __init__(self, chapter, verse, filepath):
        self.chapter = chapter
        self.verse = verse
        self.filepath = filepath

    def get_file(self):
        with io.open(self.filepath, "r", encoding="UTF-8") as f:
            return f.readlines()

    def chapter_data(self):
        with io.open(self.filepath, "r", encoding="UTF-8") as f:
            content = f.readlines()
        for i in range(len(content)):
            u = self.s.findall(content[i])  # locate chapter number and total verses
            if u == ["xxxx  Chapter"]:
                v = self.r.findall(content[i])  # extract chapter number and verses number in chapter
                if v[0] == self.chapter:
                    return v[0], v[1]


filepath = askopenfilename()  # filedialog to retrieve book required
raw_book = filepath.rsplit('/', 1)  # from file path split off 'book-name'.txt
book = raw_book[1].replace(".txt", "")  # leave only the 'book-name'

chapter = input("Please enter Chapter: ")
verse = input("Now enter verse: ")

a_verse = HBVerseExtractor(chapter, verse, filepath)
book_data = a_verse.chapter_data()
print('this is chapter', book_data[0], "of", book)
print('')
print("there are", book_data[1], "verses")

fd = a_verse.get_file()
r = regex.compile(r"\d+")  # set up regex to look for 'chapter: verse' in the lines of text
part_fp = "C:\\Users\\44779\\OneDrive\\biblical hebrew\\Genesis Analysis\\"


for i in range(len(fd)):  # loop to find chapter and verse required by the user
    t = r.findall(fd[i])
    if t == [verse, chapter]:  # if chapter and verse are found
        verse_line = regex.findall(r"\w+", fd[i])
        filename = part_fp + book + "_" + chapter + "_" + verse + " .txt"  # create filename for output text file
        with open(filename, 'a', encoding="UTF-8") as f:  # open a file for output
            f.write('\n'.join(verse_line))  # write data one word/line, to produce a column

