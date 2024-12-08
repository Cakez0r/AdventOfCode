from typing import Optional, Self


class TextGrid:
    lines: tuple[str]

    def __init__(self, lines):
        self.lines = lines
    
    @classmethod
    def from_file(cls, path:str, strip:bool = True) -> Self:
        with open(path) as f:
            lines = f.readlines()
            if strip:
                lines = [l.strip() for l in lines]
            
            return cls(lines)

    def __getitem__(self, index: tuple[int,int]) -> Optional[str]:
        ret = None
        try:
            if index[0] >= 0 and index[1] >= 0:
                return self.lines[index[1]][index[0]]
        except:
            pass
