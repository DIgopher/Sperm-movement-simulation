import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mesh_import import *


class MeshGrid:
    """
    Properties:

    .imported_mesh - mesh from txt file

    .mesh - mesh after interpolation

    .description - description from top of txt file

    .dimentions - number of dimentions, pointed in txt file

    .expressions - number of expressions, pointed in txt file

    .distance - distance between mesh nodes in remashed grid

    Methods:

    Warning!! work with 1 expression only
    """

    def __init__(self, mesh, description=None, dim=None, exp=None):
        self.imported_mesh = mesh
        self.mesh = None
        self.description: dict = description
        self.dimentions: int = dim
        self.expressions: int = exp
        self.distance: float = None
        self.aim_column = None

    def to_mkm(self):
        column_name = list(self.imported_mesh.columns)[-1]
        df_mkm = self.imported_mesh * 10**6
        df_mkm[column_name] = self.imported_mesh[column_name]
        self.imported_mesh = df_mkm

    def re_meshed(self, dis: float = 1.0):
        # column_name = list(self.imported_mesh.columns)[-1]
        self.distance = dis
        self.mesh = create_grid(
            self.imported_mesh['x'],
            self.imported_mesh['y'],
            self.imported_mesh[self.aim_column],
            grid_size=self.distance
            )
        # delete NaN values from grid
        not_nan = ~self.mesh[self.aim_column].isnull()
        df_without_nan = self.mesh.loc[not_nan]
        self.mesh = df_without_nan

    def aim_initial(self):
        self.aim_column = list(self.imported_mesh.columns)[-1]
        #initial_target_name

    def to_2_dim(self):
        self.imported_mesh.drop('z', axis='columns')

    def plot(self):
        plt.scatter(self.mesh['x'], self.mesh['y'], c=self.mesh.iloc[:, -1])


def process_file(
        filepath : str, dis=1, to_dim=True,
        to_mkm=True, re_mesh=True, plot=False
        ) -> MeshGrid:
    """
    Description:

    Create object class <MeshGrid> from txt file

    Change to to dim, transfer to mkm and remeshed

    Warning! work with 1 expression
    """
    description, mesh_dict, dim, exp = txt_to_dict(filepath)
    mesh_df = pd.DataFrame(mesh_dict)
    mesh = MeshGrid(mesh_df, description, dim, exp)
    mesh.aim_initial()
    if to_dim:
        mesh.to_2_dim()
    if to_mkm:
        mesh.to_mkm()
    if re_mesh:
        mesh.re_meshed(dis)
    if plot == 'finish':
        mesh.plot()
    elif plot == 'start_finish':
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))
        axs[0].scatter(mesh.imported_mesh['x'],
                       mesh.imported_mesh['y'], c=mesh.imported_mesh.iloc[:, -1])
        axs[0].set_title('Before')
        axs[1].scatter(mesh.mesh['x'], mesh.mesh['y'], c=mesh.mesh.iloc[:, -1])
        axs[1].set_title('After')
    return mesh
