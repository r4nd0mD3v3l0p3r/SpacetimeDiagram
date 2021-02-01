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


class LorentzTransformations:
    def transform(self, x, t, velocity):
        gamma = self.__gamma(velocity)
        return gamma * (- velocity * t + x), gamma * (t - velocity * x)

    @staticmethod
    def __gamma(velocity):
        return 1 / math.sqrt(1 - velocity * velocity)
