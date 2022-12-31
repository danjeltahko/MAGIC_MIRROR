from API import Aftonbladet, CoinMarketCap, Hue, SL, Trakt, Weather

#_aftonbladet = Aftonbladet()
#_cmc = CoinMarketCap()
#_hue = Hue()
_sl = SL()
#_trakt = Trakt()
#_weather = Weather()

if __name__ == '__main__':

    """ Aftonbladet testing"""
    #_aftonbladet.get_data_first_article()
    #_aftonbladet.FOO()
    #_aftonbladet.testing()

    """ Crypto testing"""
    """ Hue testing"""

    """ SL testing"""        
    stations = _sl.get_stations("Vällingby")
    from_id = _sl.get_station_id(stations=stations, index=0)
    _sl.set_from_station(from_id)

    stations = _sl.get_stations("Karolinska institutet västra")
    #stations = _sl.get_stations("Odenplan")
    to_id = _sl.get_station_id(stations=stations, index=0)
    _sl.set_to_station(to_id)

    array = _sl.test_travel()
    _sl.print_trains(array)
    #print(sl.get_from_station())

    """ Trakt testing"""
    #print(_trakt.get_movie("Batman"))

    """ Weather testing"""
    #fos = Weather()
    #fos.set_forecast()

    



