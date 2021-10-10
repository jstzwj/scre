import cython

@cython.cclass
class SourceLocation:
    def __init__(self, source: str, offset: int) -> None:
        self._source: str = source
        self._offset: int = offset

    @property
    def source(self) -> str:
        return self._source

    @property
    def offset(self) -> int:
        return self._offset
