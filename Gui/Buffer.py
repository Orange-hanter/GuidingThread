class Buffer:
    """
    Some implementation of system control version. Used for user changes rollback.
    We provide text of chapter and there should be ability to save raw version
    """
    def __init__(self, context: list) -> None:
        self.__buffer = dict()
        self.__buffer_ref = dict()
        # TODO поменять схему обновления на ссылку на источник в мидасе, с копией получается не реактивно
        self.__midas_context = context
        self.__chapter_focus = ""

    def init(self, text: str, chapter: str | None = None) -> None:
        self.__buffer[chapter] = text
        self.__buffer_ref[chapter] = text

    def update_focused(self, text):
        self.__buffer[self.__chapter_focus] = text

    def change_focus(self, chapter: str):
        self.__chapter_focus = chapter

    def focused_chapter(self):
        return self.__chapter_focus

    def get(self, chapter: str) -> str:
        # todo add try exception handling here
        return self.__buffer[chapter]

    def get_focused(self):
        return self.get(self.__chapter_focus)

    def reset(self, chapter: str) -> None:
        self.__buffer[chapter] = self.__buffer_ref[chapter]

    def reset_focused(self) -> None:
        self.reset(self.__chapter_focus)
