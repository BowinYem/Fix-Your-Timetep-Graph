class Position:
    def __init__(self, x : float , y : float):
        self.x = x
        self.y = y

    def __mul__(self, Scalar):
        return Position(self.x * Scalar, self.y * Scalar)
    
    def __add__(self, other):
        return Position(self.x + other.y, self.y + other.y)
