from typing import Optional
class lodderError(Exception):
    def __init__(self,message:str,source:Optional[str]=None):
        super().__init__(message)
        self.source = source
    def __str__(self):
        if self.source:
            return f"Error loading from {self.source}:{super().__str__()}"
        return super().__str__()
