from typing import Optional


class TextGrid:
    lines: tuple[str]
    width: int
    height: int

    def __init__(self, lines: list[str], strip: bool = True):
        self.lines = [l.strip() for l in lines] if strip else lines

        if not all(len(l) == len(self.lines[0]) for l in self.lines):
            raise Exception("Bad shape")

        self.width = len(self.lines[0])
        self.height = len(self.lines)
    
    def find(self, char: str) -> Optional[tuple[int, int]]:
        for x in range(self.width):
            for y in range(self.height):
                if self[x,y] == char:
                    return (x,y)

    @classmethod
    def from_file(cls, path:str, strip:bool = True) -> "TextGrid":
        with open(path) as f:
            lines = f.readlines()
            return cls(lines)

    def __getitem__(self, index: tuple[int,int]) -> Optional[str]:
        try:
            if index[0] >= 0 and index[1] >= 0:
                return self.lines[index[1]][index[0]]
        except:
            pass
    
    def __setitem__(self, index: tuple[int,int], val: str) -> Optional[str]:
        ret = None
        try:
            if index[0] >= 0 and index[1] >= 0:
                l = self.lines[index[1]]
                self.lines[index[1]] = l[:index[0]] + val + l[index[0]+1:]
        except:
            pass
