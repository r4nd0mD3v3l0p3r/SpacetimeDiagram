# Spacetime Diagram
# Copyright (C) 2021  r4nd0md3v3l0p3r

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import math

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axisartist import Subplot, SubplotHost
from mpl_toolkits.axisartist.grid_helper_curvelinear import GridHelperCurveLinear

from lorentz_transformations import LorentzTransformations
from show_hide_annotations import ShowHideAnnotations
from utils import input_file
from world_lines_plotter import WorldLinesPlotter

plt.rcParams["toolbar"] = "toolmanager"


class SpacetimeDiagram:
    def __init__(self):
        input_data = input_file()
        self.fig = plt.figure()
        self.velocity = float(input_data["movingObserver"]["velocity"])
        self.fig_suptitle = input_data["diagram"]["title"]
        self.gamma = 1 / math.sqrt(1 - self.velocity * self.velocity)
        self.world_lines_plotter = WorldLinesPlotter()
        self.showOPrime = bool(input_data["diagram"]["showOPrime"])
        self.lorentz_transformations = LorentzTransformations()

    def plot(self):
        self.fig.suptitle(self.fig_suptitle)
        self.fig.canvas.set_window_title("Spacetime diagram")

        self.__spacetime_diagram_o_frame()
        plt.legend(loc=1)

        if self.showOPrime:
            self.__spacetime_diagram_o_prime_frame()
            plt.legend(loc=1)

        self.fig.canvas.manager.toolmanager.add_tool("Show", ShowHideAnnotations, gid='customgroup',
                                                     event_annotations=self.world_lines_plotter.event_annotations)
        self.fig.canvas.manager.toolbar.add_tool("Show", "navigation", 1)

        plt.show()

    def __spacetime_diagram_o_frame(self):
        # from (x',t') to (x,t)
        def tr(x_prime, t_prime):
            x_prime, t_prime = np.asarray(x_prime), np.asarray(t_prime)
            return self.lorentz_transformations.transform(x_prime, t_prime, -self.velocity)

        # form (x,t) to (x',t')
        def inv_tr(x, t):
            x, t = np.asarray(x), np.asarray(t)
            return self.lorentz_transformations.transform(x, t, self.velocity)

        grid_helper = GridHelperCurveLinear((tr, inv_tr))
        ax = Subplot(self.fig, 1, 2, 1, grid_helper=grid_helper) if self.showOPrime \
            else Subplot(self.fig, 1, 1, 1, grid_helper=grid_helper)
        self.fig.add_subplot(ax)

        ax.set_xlabel("x", loc="center")
        ax.set_ylabel("t", loc="center")

        # O' x axis
        ax.axis["x1"] = x1 = ax.new_floating_axis(1, 0)
        x1.label.set_text("x'")

        # O' t axis
        ax.axis["t1"] = t1 = ax.new_floating_axis(0, 0)
        t1.label.set_text("t'")

        self.__add_x_and_y_axis(ax)
        ax.format_coord = self.__format_coord_o_frame

        self.__remove_ticks(ax, x1, t1)

        self.world_lines_plotter.plot(plt, ax, self.velocity)

    def __spacetime_diagram_o_prime_frame(self):
        # from (x,t) to (x',t')
        def tr(x_prime, t_prime):
            x_prime, t_prime = np.asarray(x_prime), np.asarray(t_prime)
            return self.lorentz_transformations.transform(x_prime, t_prime, self.velocity)

        # form (x',t') to (x,t)
        def inv_tr(x, t):
            x, t = np.asarray(x), np.asarray(t)
            return self.lorentz_transformations.transform(x, t, -self.velocity)

        grid_helper = GridHelperCurveLinear((tr, inv_tr))
        ax = SubplotHost(self.fig, 1, 2, 2, grid_helper=grid_helper)
        self.fig.add_subplot(ax)

        ax.set_xlabel("x'", loc="center")
        ax.set_ylabel("t'", loc="center")

        # O x axis
        ax.axis["x1"] = x1 = ax.new_floating_axis(0, 0)
        x1.label.set_text("x")

        # O t axis
        ax.axis["t1"] = t1 = ax.new_floating_axis(1, 0)
        t1.label.set_text("t")

        self.__add_x_and_y_axis(ax)
        ax.format_coord = self.__format_coord_o_prime_frame

        self.__remove_ticks(ax, x1, t1)

        self.world_lines_plotter.transform_and_plot(plt, ax, self.velocity)

    def __format_coord_o_frame(self, x, t):
        x_prime, t_prime = self.lorentz_transformations.transform(x, t, self.velocity)

        return "x:{x:0.2f}, t:{t:0.2f}  x':{x_prime:0.2f}, t':{t_prime:0.2f}".format(x=x, t=t, x_prime=x_prime,
                                                                                     t_prime=t_prime)

    def __format_coord_o_prime_frame(self, x_prime, t_prime):
        x, t = self.lorentz_transformations.transform(x_prime, t_prime, -self.velocity)

        return "x':{x_prime:0.2f}, t':{t_prime:0.2f}  x:{x:0.2f}, t:{t:0.2f}".format(x_prime=x_prime,
                                                                                     t_prime=t_prime, x=x,
                                                                                     t=t)

    # this method draw extra axis that intersect the floating ones in the center
    @staticmethod
    def __add_x_and_y_axis(ax):
        ax.axhline(y=0, color="black", lw=0.9)
        ax.axvline(x=0, color="black", lw=0.9)

    @staticmethod
    def __remove_ticks(ax, x1, t1):
        ax.axis["top"].toggle(ticks=False, ticklabels=False)
        ax.axis["left"].toggle(ticks=False, ticklabels=False)
        ax.axis["right"].toggle(ticks=False, ticklabels=False)
        ax.axis["bottom"].toggle(ticks=False, ticklabels=False)
        x1.toggle(ticks=False, ticklabels=False)
        t1.toggle(ticks=False, ticklabels=False)
