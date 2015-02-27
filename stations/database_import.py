from stations.models import Station, Signal

class DatabaseImport:
    """Defines methods for importing signals or stations from a file into the db."""

    @staticmethod
    def import_stations(file):
        """
        Imports stations listed in a file to the database.
        :param file: The file with the stations.
        """
        with open(file) as f:
            for line in f:
                fields = line.split(",")
                pmu_id = fields[1].replace("[", "").replace("]", "").replace("\"", "")  # convert "[0x84e0]" to 0x84e0
                pmu_id = int(pmu_id, 0)
                new_station = Station(
                    PMU_ID=pmu_id,
                    PMU_Company=fields[2].replace("\"", ""),
                    PMU_Name_Raw=fields[3].replace("\"", ""),
                    PMU_Name_Short=fields[4].replace("\"", ""),
                    PMU_Name_Long=fields[5].replace("\"", ""),
                    PMU_Set=fields[6].replace("\"", ""),
                    PMU_Channel=fields[7].replace("\"", ""),
                    PMU_Type=fields[8].replace("\"", ""),
                    PMU_Voltage=int(fields[9].replace("\"", ""))
                )
                new_station.save()
                print(new_station)

    @staticmethod
    def import_signals(file):
        """
        Imports signals listed in a file to the database.
        :param file: The file with the signals.
        """
        with open(file) as f:
            count = 0
            for line in f:
                fields = line.split(",")
                signal_pmu_id = fields[2].replace("[", "").replace("]", "").replace("\"", "")  # convert "[0x84e0]" to 0x84e0
                signal_pmu_id = int(signal_pmu_id, 0)

                try:
                    signal_pmu_id = Station.objects.filter(PMU_ID=signal_pmu_id)[0]
                except IndexError:
                    print("No station associated with this signal: " + str(signal_pmu_id))
                    count += 1
                    continue
                new_signal = Signal(
                    Signal_ID=fields[1],
                    Signal_PMU_ID=signal_pmu_id,
                    Signal_Index=int(fields[3].replace("\"", "")),
                    Signal_Name_Raw=fields[4].replace("\"", ""),
                    Signal_Name_Short=fields[5].replace("\"", ""),
                    Signal_Name_Group=fields[6].replace("\"", ""),
                    Signal_Name_Long=fields[7].replace("\"", ""),
                    Signal_Type=fields[8].replace("\"", ""),
                    Signal_Asset=fields[9].replace("\"", ""),
                    Signal_Voltage=int(fields[10].replace("\"", "")),
                    Signal_Circuit=int(fields[11].replace("\"", "")),
                    Signal_Unit=fields[12].replace("\"", ""),
                    Signal_Phase=fields[13].replace("\"", "").replace("\n", "")
                )
                new_signal.save()
                print(new_signal)
            print(count)