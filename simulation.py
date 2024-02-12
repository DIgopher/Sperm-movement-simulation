import numpy as np
import pandas as pd
from lerp import remap
from Mesh_class import MeshGrid


def find_sr(coord: tuple, mesh: MeshGrid) -> float:
    """
    Description: find shear rate in point that is not in the node

    coord : tuple(), len = 2

    mesh : MeshGrid class that was remeshed

    """

    x , y = coord
    aim_column = mesh.aim_column
    dis = mesh.distance

    if not (mesh.mesh.query(f'x=={x} and y=={y}')).empty:
        shear_rate = (mesh.mesh.query(f'x=={x} and y=={y}'))[aim_column]
        return shear_rate
    
    
    if not (mesh.mesh.query(f'x>={x-dis} and x<={x+dis} and y>={y-dis} and y<={y+dis}').shape)[0] == 4:
        print(mesh.mesh.query(f'x>={x-dis} and x<={x+dis} and y>={y-dis} and y<={y+dis}').shape)
        print(mesh.mesh.query(f'x>={x-dis} and x<={x+dis} and y>={y-dis} and y<={y+dis}'))
        return None
    
    #print(near_nodes)
    
    x_max_y_max = mesh.mesh.query(f'x>={x} and x<={x+dis} and y>={y} and y<={y+dis}')
    x_max_y_min = mesh.mesh.query(f'x>={x} and x<={x+dis} and y>={y-dis} and y<={y}')
    x_min_y_min = mesh.mesh.query(f'x>={x-dis} and x<={x} and y>={y-dis} and y<={y}')
    x_min_y_max = mesh.mesh.query(f'x>={x-dis} and x<={x} and y>={y} and y<={y+dis}')
    y_min = remap(float(x_min_y_min['x'].iloc[0]), 
                     float(x_max_y_min['x'].iloc[0]), 
                     float(x_min_y_min[aim_column].iloc[0]), 
                     float(x_max_y_min[aim_column].iloc[0]), 
                     x)
    #need property - aim column - value 
    
    y_max = remap(float(x_min_y_max['x'].iloc[0]), 
                     float(x_max_y_max['x'].iloc[0]), 
                     float(x_min_y_max[aim_column].iloc[0]), 
                     float(x_max_y_max[aim_column].iloc[0]), 
                     x)
    
    shear_rate = remap(float(x_min_y_min['y'].iloc[0]), 
                       float(x_min_y_max['y'].iloc[0]), 
                       y_min, 
                       y_max, 
                       y)
    return shear_rate


def angle_step(angle: float, shear_rate: float, par_a: float = 0.07, noise: float = 0) -> float:
    #turn to new angle
    step_angle = -1 * par_a * shear_rate * np.sin(angle)
    angle += step_angle
    return angle


def movement_step(angle: float, coord: tuple, step_size: float, noise = 0) -> float:
    #move to new point
    x , y = coord
    delta_x = -np.cos(angle) * step_size
    delta_y = np.sin(angle) * step_size
    x = x + delta_x
    y = y + delta_y
    coord = (x,y)
    return coord


#Add or not another function to step?
def sim(coord: tuple, angle: float, mesh: MeshGrid, history: dict, steps: int) -> dict:
    history['x'].append(coord[0])
    history['y'].append(coord[1])
    par_a = 0.07
    step_size = 10
    for step in range(steps):
        shear_rate = find_sr(coord, mesh)
        if shear_rate == None:
            print(f'Simulation stopped on step {step}')
            print(coord)
            return history
        angle = angle_step(angle, shear_rate, par_a)
        coord = movement_step(angle, coord, step_size)
        history['x'].append(coord[0])
        history['y'].append(coord[1])

    return history