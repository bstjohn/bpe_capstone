import json


class QueryToJsonConverter:
    def __init__(self, query_name, start_date_time, end_date_time, stations, conditions):
        self.query_name = query_name
        self.start_date_time = start_date_time
        self.end_date_time = end_date_time
        self.stations = stations
        self.conditions = conditions