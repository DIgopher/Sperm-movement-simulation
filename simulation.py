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

    x, y = coord
    aim_column = mesh.aim_column
    dis = mesh.distance

    # if sperm in grid node
    if not (mesh.mesh.query(f'x=={x} and y=={y}')).empty:
        shear_rate = (mesh.mesh.query(f'x=={x} and y=={y}'))[aim_column]
        return shear_rate

    # if around sperm only 3 or less points
    points_around = mesh.mesh.query(
        f'x>={x-dis} and x<={x+dis} and y>={y-dis} and y<={y+dis}'
        )
    points_around_amount = (points_around.shape)[0]

    if points_around_amount == 0 or points_around_amount == 1 or points_around_amount == 3:
        # print(points_around.shape)
        # print(points_around)
        return None

    if points_around_amount == 2:
        # print(points_around)
        # if min and max on x are not equal -> then interpolation only on x
        if not points_around['x'].min() == points_around['x'].max():
            idx_min = points_around['x'].idxmin()
            idx_max = points_around['x'].idxmax()
            shear_rate = remap(
                float(points_around.loc[idx_min, 'x']),
                float(points_around.loc[idx_max, 'x']),
                float(points_around.loc[idx_min, aim_column]),
                float(points_around.loc[idx_max, aim_column]),
                x
                )
            return shear_rate
        
        if not points_around['y'].min() == points_around['y'].max():
            idx_min = points_around['y'].idxmin()
            idx_max = points_around['y'].idxmax()
            shear_rate = remap(
                float(points_around.loc[idx_min, 'y']),
                float(points_around.loc[idx_max, 'y']),
                float(points_around.loc[idx_min, aim_column]),
                float(points_around.loc[idx_max, aim_column]),
                y
                )
            return shear_rate
    # if DF with 2 rows

    # if min and max on y are not equal -> then interpolation only on y
    # If with 1 row? - mb it's near the node??
    # print(near_nodes)

    x_max_y_max = points_around.query(f'x>={x} and y>={y}')
    x_max_y_min = points_around.query(f'x>={x} and y<={y}')
    x_min_y_min = points_around.query(f'x<={x} and y<={y}')
    x_min_y_max = points_around.query(f'x<={x} and y>={y}')

    # if not (x_min_y_min.empty and x_min_y_min.empty)
    y_min = remap(
                float(x_min_y_min['x'].iloc[0]),
                float(x_max_y_min['x'].iloc[0]),
                float(x_min_y_min[aim_column].iloc[0]),
                float(x_max_y_min[aim_column].iloc[0]),
                x
                )

    y_max = remap(
                float(x_min_y_max['x'].iloc[0]),
                float(x_max_y_max['x'].iloc[0]),
                float(x_min_y_max[aim_column].iloc[0]),
                float(x_max_y_max[aim_column].iloc[0]),
                x
                )

    shear_rate = remap(
                    float(x_min_y_min['y'].iloc[0]),
                    float(x_min_y_max['y'].iloc[0]),
                    y_min,
                    y_max,
                    y
                    )

    return shear_rate


def angle_step(
        angle: float,
        shear_rate: float,
        par_a: float = 0.07,
        noise: float = 0
        ) -> float:
    # turn to new angle
    step_angle = -1 * par_a * shear_rate * np.sin(angle)
    angle += step_angle
    return angle


def movement_step(
                  angle: float, coord: tuple, step_size: int,
                  noise_power: float = 5, noise: bool = True
                  ) -> tuple[float, float]:
    # move to new point
    x, y = coord
    delta_x = -np.cos(angle) * step_size
    delta_y = np.sin(angle) * step_size
    noise_x = 0
    noise_y = 0
    if noise:
        shift = np.random.normal(scale=noise_power)
        noise_x = np.cos(np.pi/2-angle) * shift
        noise_y = np.sin(np.pi/2-angle) * shift
    x = x + delta_x + noise_x
    y = y + delta_y + noise_y
    coord = (x, y)
    return coord


# Add or not another function to step?
def sim(
        coord: tuple[float, float], angle: float, mesh: MeshGrid, 
        history: dict, steps: int, step_size: int = 10,
        noise_power: float = 5, noise: bool = True
        ) -> dict:
    history['x'].append(coord[0])
    history['y'].append(coord[1])
    par_a = 0.07
    for step in range(steps):
        shear_rate = find_sr(coord, mesh)
        if shear_rate is None:
            print(f'Simulation stopped on step {step}')
            print(coord)
            return history
        angle = angle_step(angle, shear_rate, par_a)
        coord = movement_step(angle, coord, step_size, noise_power, noise)
        history['x'].append(coord[0])
        history['y'].append(coord[1])

    return history
