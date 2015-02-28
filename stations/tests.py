from django.test import TestCase

from stations.database_import import DatabaseImport


class TestDatabaseImport(TestCase):
    def test_import_stations(self):
        DatabaseImport.import_stations("pmu_definition_gbpa.csv")

    def test_import_signals(self):
        DatabaseImport.import_signals("signal_definition_gbpa.csv")