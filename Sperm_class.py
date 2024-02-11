

class Sperm:
    def __init__(self, mesh, coordinates: float = None , angle: float = None):
        self.mesh = mesh
        self.angle = angle
        self.start_coordinates = coordinates
        self.history = [{'x': [], 'y': []}]
    def mesh(self, mesh):
        self.mesh = mesh
    def simulation(self, steps):
        for t in range(1,steps):
            print('step')
        #function from sim module


print('finish')