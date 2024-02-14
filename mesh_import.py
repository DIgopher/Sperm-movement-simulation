import numpy as np
import pandas as pd

from itertools import product
from scipy.interpolate import LinearNDInterpolator


def txt_to_dict(file_path: str) -> tuple[dict, dict, int, int]:
    """
    Convert txt file, that was exported from comsol
    to dictionary with addition description

    Output: tuple(decription dictionary, dictionary with data,
    number of dimentions, number of expressions)

    At the moment column names may by wrong,
    because it split lines by whitespaces
    """
    descrp = {}
    dict = {}
    with open(file_path) as f:
        for line in f:
            row = line.split()
            # print(row)
            if row[0] == '%':
                if row[1] == 'x':
                    dim = int(descrp['Dimension:'][0])
                    exp = int(descrp['Expressions:'][0])
                    descrp['Columns:'] = row[1:]
                    table = [[] for i in row[1:dim+exp+1]]
                    # table = {i:[] for i in row[1:dim+exp+1]}
                else:
                    descrp[row[1]] = row[2:]
            else:
                for i in range(dim+exp):
                    table[i].append(float(row[i]))
    for i in range(dim+exp):
        dict[descrp['Columns:'][i]] = table[i]

    return descrp, dict, dim, exp


def file_import(file_path):
    df = pd.read_csv(file_path, sep=';')
    return df


# need to add methods for grid formation
def create_grid(
        x: pd.Series,
        y: pd.Series,
        z_param: pd.Series,
        grid_step_x: int = 100,
        grid_step_y: int = 100,
        grid_size: float = 1
        ) -> tuple:

    grid_size = 1
    grid_step_x = round((x.max()-x.min())/grid_size)
    grid_step_y = round((y.max()-y.min())/grid_size)
    print(grid_step_x)
    print(grid_step_y)

    x_coord_range = np.linspace(x.min(), x.max(), grid_step_x)
    y_coord_range = np.linspace(y.min(), y.max(), grid_step_y)

    XY = list(product(x_coord_range, y_coord_range))
    XY = np.asarray(XY)

    interpolator = LinearNDInterpolator(
            points=(x.values, y.values),
            values=z_param.values,
            )

    Z = interpolator(XY[:, 0], XY[:, 1])
    df = pd.DataFrame(columns=["x", "y", z_param.name], )
    df["x"] = XY[:, 0]
    df["y"] = XY[:, 1]
    df[z_param.name] = Z

    return df, interpolator


def re_mesh(file_path):
    df = file_import(file_path)
    df.drop('z', axis='columns')
    column_name = list(df.columns)[-1]
    df_mkm = df * 10e5
    df_mkm[column_name] = df[column_name]
    df_meshed = create_grid(df_mkm['x'], df_mkm['y'], df_mkm[column_name])
    # delete NaN values from grid
    not_nan = ~df_meshed[column_name].isnull()
    df_without_nan = df_meshed.loc[not_nan]
    return df_without_nan
