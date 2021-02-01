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

from event_annotation import EventAnnotation
from lorentz_transformations import LorentzTransformations
from utils import input_file


class WorldLinesPlotter:
    def __init__(self):
        self.lorentz_transformations = LorentzTransformations()
        self.world_lines = []
        self.event_annotations = []
        input_data = input_file()

        for input_world_line in input_data["worldLines"]:

            # remove whitespaces
            events = " ".join(input_world_line["events"].split())

            world_line_x = []
            world_line_t = []

            for event in events.split("),"):
                event = event.replace("(", "").replace(")", "")
                x, t = event.split(",")
                world_line_x.append(float(x))
                world_line_t.append(float(t))

            self.world_lines.append(WorldLine(input_world_line["label"], world_line_x, world_line_t))

    def plot(self, plt, axes, v):
        for world_line in self.world_lines:
            axes.plot(world_line.x_coordinates, world_line.t_coordinates, label=world_line.label)
            self.event_annotations.append(
                EventAnnotation(plt, axes, world_line.x_coordinates, world_line.t_coordinates, v))

    def transform_and_plot(self, plt, axes, v):

        for world_line in self.world_lines:
            transformed_xs = []
            transformed_ts = []

            # apply Lorentz transformations
            for x, t in zip(world_line.x_coordinates, world_line.t_coordinates):
                transformed_x, transformed_t = self.lorentz_transformations.transform(x, t, v)
                transformed_xs.append(transformed_x)
                transformed_ts.append(transformed_t)

            axes.plot(transformed_xs, transformed_ts, label=world_line.label)
            self.event_annotations.append(EventAnnotation(plt, axes, transformed_xs, transformed_ts, -v, True))


class WorldLine:
    def __init__(self, label, x_coordinates, t_coordinates):
        self.label = label

        # all the x coordinates of the world line
        self.x_coordinates = x_coordinates

        # all the t coordinates of the world line
        self.t_coordinates = t_coordinates
