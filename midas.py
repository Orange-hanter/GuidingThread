"""Module providing a functionality of converting pdf to text."""


import re
import sys

from pypdf import PdfReader


class PDFP:
    """PDF processor class

    """

    # (\d\.(?:\d*\.){0,}) (\p{L}+ \p{L}*){0,}\W+(\d \s?\d?)
    menu_pattern = r'(\d\..?\.) (\S+ \.) \W+(\d\s?\d?)'
    table_of_content = list()

    def __init__(self, path: str) -> None:
        self.pdf_source = path
        self.reader = PdfReader(self.pdf_source)
        self.gen_content_table(self.get_text(2, 1))

    def gen_content_table(self, text: str) -> list:
        """return content table for future parsing

        Args:
            text (str): raw text of content menu
        Returns:
            str: _description_
        """
        matches = re.findall(self.menu_pattern, text)
        matches = [list(item) for item in matches]

        chapter, title, page = 0, 1, 2
        content_table = []
        for item in matches:
            item[page] = int(item[page].replace(" ", ""))
            content_table.append(item)

        self.table_of_content = sorted(content_table, key=lambda x: x[page])

    def chapter_diapazone(self, chapter):
        chapter, title, page = 0, 1, 2
        chapter_metadata = self.table_of_content[chapter]
        # veeeery unoptimized, my bad
        chapter_metadata_next = self.table_of_content[chapter + 1]
        return {chapter_metadata[page], chapter_metadata_next[page]}

    def chapter_lenght(self, chapter):
        pg_start, pg_end = self.chapter_diapazone(chapter)
        return pg_end - pg_start

    def get_text(self, start_page: int, sheets: int = 0) -> str:
        """_summary_

        Args:
            page (int, optional): page number that looking for. Defaults to 0 that mean first page.

        Returns:
            str: raw text of pdf file
        """
        text = ''
        for page in range(start_page - 1, start_page + sheets):
            text += self.reader.pages[page].extract_text()
        return text

    def get_chapter(self, chapter: int = 1):
        """todo get fuzzy logic for name or index of chapter

        Args:
            chapter (int, optional): _description_. Defaults to 1.
        """
        chapter_metadata = self.table_of_content[chapter]
        # veeeery unoptimized, my bad
        chapter_metadata_next = self.table_of_content[chapter + 1]
        pg_start, pg_end = chapter_metadata[2], chapter_metadata_next[2]
        raw_chapter_text_list = []
        for page in range(pg_start, pg_end):
            raw_chapter_text_list.append(self.get_text(page))
        return raw_chapter_text_list

    def __iter__(self):
        num, name, page = 0, 1, 2
        # ["cha", "Название главы", 12]
        for chapter in range(len(self.table_of_content) - 1):
            start_page = self.table_of_content[chapter][page]
            end_page = self.table_of_content[chapter + 1][page] - start_page
            yield self.get_text(start_page, end_page)


if __name__ == "__main__":
    print(sys.argv[0])
    pdfpInstance = PDFP("""./Sources/Dr.Coffee-f11 .pdf""")

    # table_of_content = pdfpInstance.get_text(1)
    # x = pdfpInstance.gen_content_table(table_of_content)

    # x = pdfpInstance.get_chapter(2)
    for text in pdfpInstance:
        print(text)
        print('-'*50)
