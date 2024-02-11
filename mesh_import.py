import numpy as np
import pandas as pd

from itertools import product
from scipy.interpolate import griddata



def file_import(file_path):
    df = pd.read_csv(file_path, sep=';')
    return df

#need to add methods for grid formation
def create_grid(
        x: pd.Series,
        y: pd.Series,
        z_param: pd.Series,
        grid_step_x: int = 100,
        grid_step_y: int = 100,
        method: str = 'linear',
        ) -> pd.DataFrame:
    
    grid_size = 1
    grid_step_x = round((x.max()-x.min())/grid_size)
    grid_step_y = round((y.max()-y.min())/grid_size)
    print(grid_step_x)
    print(grid_step_y)
    
    x_coord_range = np.linspace(x.min(), x.max(), grid_step_x)
    y_coord_range = np.linspace(y.min(), y.max(), grid_step_y)

    XY = list(product(x_coord_range, y_coord_range))
    XY = np.asarray(XY)

    interpolation = griddata(
            points=(x.values, y.values),
            values=z_param.values,
            xi=XY,
            method=method
            )

    df = pd.DataFrame(columns=["x", "y", z_param.name], )
    df["x"] = XY[:, 0]
    df["y"] = XY[:, 1]
    df[z_param.name] = interpolation

    return df


def re_mesh(file_path):
    df = file_import(file_path)
    df.drop('z', axis = 'columns')
    column_name = list(df.columns)[-1]
    df_mkm = df * 10e6
    df_mkm[column_name] = df[column_name]
    df_meshed = create_grid(df_mkm['x'], df_mkm['y'], df_mkm[column_name])
    return df_meshed