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

import numpy as np
from scipy.spatial import cKDTree

from lorentz_transformations import LorentzTransformations


class EventAnnotation:
    hover_distance = 1

    def __init__(self, plt, ax, x_coordinates, t_coordinates, v, x_prime_frame=False):
        self.ax = ax

        self.annotation = self.ax.annotate(
            '', xy=(0, 0), ha='left',
            xytext=(-20, 20), textcoords='offset points', va='bottom',
            bbox=dict(
                boxstyle='round,pad=0.5', fc='yellow', alpha=1),
            arrowprops=dict(
                arrowstyle='->', connectionstyle='arc3,rad=0'))
        self.annotation.set_visible(False)
        self.annotations_enabled = False

        self.lorentz_transformations = LorentzTransformations()
        self.velocity = v
        self.x_prime_frame = x_prime_frame

        x = np.asarray(x_coordinates, dtype='float')
        t = np.asarray(t_coordinates, dtype='float')
        self.ckdtree = cKDTree(np.column_stack((x_coordinates, t_coordinates)))
        plt.connect('motion_notify_event', self)

    def __call__(self, event):
        if not self.annotations_enabled or event.inaxes != self.ax:
            return

        x, t = event.xdata, event.ydata
        closest_point_candidate = self.ckdtree.query([x, t])

        if closest_point_candidate[0] <= self.hover_distance:
            x, t = self.ckdtree.data[closest_point_candidate[1]]
            self.annotation.xy = x, t
            self.annotation.set_text(self.__format_text(x, t))
            self.annotation.set_visible(True)
            event.canvas.draw()

    def __format_text(self, x, t):
        x_prime, t_prime = self.lorentz_transformations.transform(x, t, self.velocity)

        if self.x_prime_frame:
            return "x':{x_prime:0.2f}, t':{t_prime:0.2f}\nx:{x:0.2f}, t:{t:0.2f}".format(x_prime=x,
                                                                                         t_prime=t, x=x_prime,
                                                                                         t=t_prime)
        else:
            return "x:{x:0.2f}, t:{t:0.2f}\nx':{x_prime:0.2f}, t':{t_prime:0.2f}".format(x=x, t=t, x_prime=x_prime,
                                                                                         t_prime=t_prime)
