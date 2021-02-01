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

from matplotlib.backend_tools import ToolToggleBase


class ShowHideAnnotations(ToolToggleBase):
    image = r"arrow.png"
    default_keymap = "m"
    description = "Show events coordinates on mouse hover (shortcut: m)"
    default_toggled = False

    def __init__(self, *args, gid, event_annotations, **kwargs):
        self.gid = gid
        self.event_annotations = event_annotations
        super().__init__(*args, **kwargs)

    def enable(self, *args):
        for event_annotation in self.event_annotations:
            event_annotation.annotations_enabled = True

    def disable(self, *args):
        for event_annotation in self.event_annotations:
            event_annotation.annotations_enabled = False
