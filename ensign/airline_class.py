class Flight:

    def __init__(self, icao24):
        self.icao24 = icao24
        self.origin_airport_icao = "Unknown"
        self.destination_airport_icao = "Unknown"
        self.scheduled_departure = "Unknown"
        self.scheduled_arrival = "Unknown"
        self.actual_departure = "Unknown"
        self.estimated_arrival = "Unknown"
        self.historical_flight_time = "Unknown"
        self.historical_delay = "Unknown"

    # taken from Ensign database
    def store_ensign_data(self, flight):
    
        self.callsign = flight['callsign']
        self.airline_icao = flight['callsign'][:3]
        self.origin_country = flight['origin_country']
        self.time_position = flight['time_position']
        self.last_contact = flight['last_contact']
        self.longitude = flight['longitude']
        self.latitude = flight['latitude']
        self.geo_altitude = flight['geo_altitude']
        self.on_ground = flight['on_ground']
        self.true_track = flight['true_track']
        self.velocity = flight['velocity']
        self.vertical_rate = flight['vertical_rate']
        self.sensors = flight['sensors']
        self.barometric_altitude = flight['barometric_altitude']
        self.transponder_code = flight['transponder_code']
        self.special_purpose_indicator = flight['special_purpose_indicator']
        self.position_source = flight['position_source']
        self.category = flight['category']
        self.airline = ""

    def store_fr24_data(self, instance):
        self.origin_airport_icao = instance['origin_airport_icao']
        self.destination_airport_icao = instance['destination_airport_icao']
        self.scheduled_departure = instance['scheduled_departure']
        self.scheduled_arrival = instance['scheduled_arrival']
        self.actual_departure = instance['actual_departure']
        self.estimated_arrival = instance['estimated_arrival']
        self.historical_flight_time = instance['historical_flight_time']
        self.historical_delay = instance['historical_delay']