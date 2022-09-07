class Weather_OBJ:

    def __init__(self) -> None:

        self.name = None

        # Weather data
        self.iconurl = None     # Cloud icon
        self.main = None        # Clouds, sunny etc
        self.description = None # few clouds
        
        # Main data
        self.temp = None        # celsius
        self.feels_like = None  # celsius
        self.temp_min = None    # celsius
        self.temp_max = None    # celsius
        self.pressure = None    # hPa
        self.humidity = None    # %

        # Wind data
        self.wind_speed = None  # m/s
        self.wind_deg = None    # Wind Direction, degrees (49•)
        
        # Cloud data
        self.clouds = None      # Cloudiness %

        # Rain & Snow / if available
        self.snow = None        # Snow volume for last 3 hours
        self.rain = None        # Rain volume for last 3 hours

        """

        UTC = SECONDS SINCE JAN 01 1970. (UTC)

        """
        # Time Data
        self.timezone = None    # Shift in seconds from UTC
        self.dt = None          # Time of data forecasted, Unix, UTC
        self.sunrise = None     # Sunrise time, Unix, UTC
        self.sunset = None      # Sunset time, Unix, UTC