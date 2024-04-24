"""Module providing a functionality of converting pdf to text."""

import re
import sys
from functools import cache
from collections import OrderedDict
from pypdf import PdfReader


class PDFP:
    """Processor PDF

    """

    # (\d\.(?:\d*\.){0,}) (\p{L}+ \p{L}*){0,}\W+(\d \s?\d?)
    menu_pattern = r'(\d\..?\.) (\S+ \.) \W+(\d\s?\d?)'
    table_of_content = list()

    def __init__(self, path: str = "") -> None:
        self.pdf_source = path
        self._content_table = OrderedDict()

    def run(self):
        self.reader = PdfReader(self.pdf_source)
        self.gen_content_table(self.get_text(2, 1))

    def set_source(self, path: str):
        self.pdf_source = path

    def gen_content_table(self, text: str) -> None:
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

        table_of_content = sorted(content_table, key=lambda x: x[page])
        for item in table_of_content:
            self._content_table[item[chapter]] = item

    def _chapter_diapason(self, chapter: str):
        chapter, title, page = 0, 1, 2
        chapter_metadata = self.table_of_content[chapter]
        chapter_metadata_next = self.table_of_content[chapter + 1]
        return {chapter_metadata[page], chapter_metadata_next[page]}

    @cache
    def chapter_length(self, chapter):
        pg_start, pg_end = self._chapter_diapason(chapter)
        return pg_end - pg_start

    def get_text(self, start_page: int, sheets: int = 0) -> str:
        """_summary_

        Args:
            start_page (int, optional): page number that looking for. Defaults to 0 that mean first page.
            sheets (int, optional): number of sheets. Defaults to 0.
        Returns:
            str: raw text of pdf file
        """
        text = ''
        for page in range(start_page - 1, start_page + sheets):
            text += self.reader.pages[page].extract_text()
        return text

    @cache
    def _get_metadata_by_id(self, id: int | str) -> list:
        if str == type(id):
            return self._content_table[id]
        kees = [key for key in self._content_table.keys()]
        return self._content_table[kees[id]]

    def _get_next_chapter_metadata(self, chapter: str) -> str:
        kees = [key for key in self._content_table.keys()]
        index = kees.index(chapter)
        # todo check the end of file
        return self._content_table[kees[index + 1]]

    def get_context(self):
        return self._content_table.values()
    @cache
    def get_chapter(self, chapter: str | None = None) -> str:
        """
        todo get fuzzy logic for name or index of chapter
        Args:
            chapter (int, optional): _description_. Defaults to 1.
        """
        chapter_metadata = self._get_metadata_by_id(chapter if chapter else 0)
        chapter_metadata_next = self._get_next_chapter_metadata(chapter_metadata[0])
        pg_start, pg_end = chapter_metadata[2], chapter_metadata_next[2]
        raw_chapter_text_list = ""
        for page in range(pg_start, pg_end):
            raw_chapter_text_list += self.get_text(page)
        return raw_chapter_text_list

    def __iter__(self):
        ch_id, name, page = 0, 1, 2  # ["1.", "Название главы", 12]
        for chapter in range(len(self._content_table) - 1):
            yield self.get_chapter(self._get_metadata_by_id(chapter)[ch_id])

    def isError(self):
        # TODO
        return 0


if __name__ == "__main__":
    print(sys.argv[0])
    pdfpInstance = PDFP()
    pdfpInstance.set_source("""./Sources/Dr.Coffee-f11 .pdf""")
    pdfpInstance.run()
    # table_of_content = pdfpInstance.get_text(1)
    # x = pdfpInstance.gen_content_table(table_of_content)

    #x = pdfpInstance.get_chapter()
    #print(x)

    for chapter_text in pdfpInstance:
        print(chapter_text)
        print('-' * 50)
