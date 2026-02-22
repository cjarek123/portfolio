"""
CS529

Adrien Clay

Christopher Jarek

Thomas Hynes

Refat Mishuk
"""
class SystemState:
    '''
    Simple helper to standardize state management during the learning process
    '''
    def __init__(self, x, v):
        self.x = x
        self.v = v

    
    def get_state(self):
        return (self.x, self.v)
    
    def __str__(self):
        return f"({self.x}, {self.v})"