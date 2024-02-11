import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from simulation import sim

class Sperm:
    
    def __init__(self, mesh, coordinates: float = None , angle: float = None):
        self.mesh = mesh
        self.angle = angle
        self.start_coordinates = coordinates
        self.history = {'x': [], 'y': []}
    
    def __str__(self) -> str:
        return f'Angle = {self.angle}, Coordinates = {self.start_coordinates}'

    def up_mesh(self, mesh):
        self.mesh = mesh
    
    def rnd_coord_from_mesh(self):
        x = random.randint(self.mesh['x'].min(), self.mesh['x'].max())
        y = random.randint(self.mesh['y'].min(), self.mesh['y'].max())
        self.start_coordinates = (x, y)
        #random coordinates from mesh nodes
        pass

    def rnd_coord_around_point(self, coord, dis):
        x = random.randint(coord[0]-dis, coord[0]+dis) + random.random()
        y = random.randint(coord[1]-dis, coord[1]+dis) + random.random()
        self.start_coordinates = (x, y)
    
    def rnd_angle(self):
        self.angle = random.random() * 360
        #random angle

    def simulation(self, steps = 10):
        if self.start_coordinates == None or self.angle == None :
            #maybe ADD other methods, so it can generate random state automatically
            raise ValueError('Enter coordinates or angle before simulation')
        self.history = {'x': [], 'y': []}
        angle = np.pi / 180 * self.angle 
        sim(self.start_coordinates, angle, self.mesh, self.history, steps)
        #function from sim module
    
    def plot(self):
        #plot history, raise error if history is empty
        fig, ax = plt.subplots()
        ax.plot(self.history['x'], self.history['y'])
        ax.plot(self.start_coordinates[0], self.start_coordinates[1], 'ro')
        ax.set(xlim = (self.mesh['x'].min(), self.mesh['x'].max()), ylim = (self.mesh['y'].min(), self.mesh['y'].max()))
        return plt.show()

#Sperm group class to generate big amount of particles

class SpermGroup:
    
    def __init__(self, amount, mesh):
        self.amount = amount
        self.sperm_list = [Sperm(mesh) for i in range(amount)]
        self.generation_method = 'None'
        self.mesh = mesh
    
    def __str__(self) -> str:
        df = pd.DataFrame(columns=['Start coordinates', 'Angle'])
        for sperm in self.sperm_list:
            sperm_dict = {'Start coordinates': sperm.start_coordinates, 'Angle': sperm.angle}
            df.append(sperm_dict, ignore_index = True)
        return df

    def gen_around_point(self, coord, dis):
        for sperm in self.sperm_list:
            sperm.rnd_angle()
            sperm.rnd_coord_around_point(coord, dis)

    def gen_in_mesh(self):
        for sperm in self.sperm_list:
            sperm.rnd_angle()
            sperm.rnd_coord_from_mesh()
            
        
    def simulation(self, steps = 10, info  = 0):
        """
        Description:
        :param int info: Showing additional information during simulation, 
        1 - for information, other state - no information
        """
        counter = 0
        for sperm in self.sperm_list:
            if info == 1:
                print(f'Start simulation {counter}')
            counter+=1
            sperm.simulation(steps)
    
    def plot(self):
        fig, ax = plt.subplots()
        for sperm in self.sperm_list:
            ax.plot(sperm.history['x'], sperm.history['y'])
            ax.plot(sperm.start_coordinates[0], sperm.start_coordinates[1], 'ro')
        ax.set(xlim = (self.mesh['x'].min(), self.mesh['x'].max()), ylim = (self.mesh['y'].min(), self.mesh['y'].max()))
        return plt.show()

