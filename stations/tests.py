# Bonneville Power Adminstration Front-End
# Copyright (C) 2015  Brady St. John
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, US$
#
from django.test import TestCase

from stations.database_import import DatabaseImport


class TestDatabaseImport(TestCase):
    def test_import_stations(self):
        DatabaseImport.import_stations("pmu_definition_gbpa.csv")

    def test_import_signals(self):
        DatabaseImport.import_signals("signal_definition_gbpa.csv")