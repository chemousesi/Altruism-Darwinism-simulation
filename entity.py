

class Entity:

    def __init__(self, pos) :

        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def getX(self):
        return self.x
    def getY(self):
        return self.y
    
    def set_pos(self):

        self.x = self.pos[0]
        self.y = self.pos[1]