class Buffer:
    """
    Some implementation of system control version. Used for user changes rollback.
    We provide text of chapter and there should be ability to save raw version
    """
    def __init__(self, context: list) -> None:
        self.__buffer = dict()
        self.__buffer_ref = dict()
        self.__midas_context = context.copy()
        self.chapter_focus = ""

    def update(self, text: str, chapter: str = None) -> None:
        if chapter is None:
            self.__buffer[self.chapter_focus] = text
        self.__buffer[chapter] = text

    def get(self, chapter: str) -> str:
        # todo add try exception handling here
        return self.__buffer[chapter]

    def reset(self, chapter: str) -> None:
        self.__buffer[id] = self.__buffer_ref[id]

