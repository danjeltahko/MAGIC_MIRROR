from API import Aftonbladet, CoinMarketCap, Hue, SL, Trakt, Weather, Fitbit, AlbumGenerator, Telegram

_aftonbladet = Aftonbladet()
_cmc = CoinMarketCap()
_hue = Hue()
_sl = SL()
_trakt = Trakt()
_weather = Weather() 
_fitbit = Fitbit()
_gen = AlbumGenerator()

if __name__ == '__main__':

    #_gen.randomGenerator()
    #_gen.getTodaysAlbum()
    #tg = Telegram()
    #tg.send_message("test ERROR")

    """ Aftonbladet testing"""
    #_aftonbladet.get_data_first_article()
    #_aftonbladet.FOO()
    #_aftonbladet.testing()

    """ Crypto testing"""
    """ Hue testing"""

    """ SL testing"""        

    # returns a dictionary list with all stations similar to search
    from_stations = _sl.get_every_station("Vällingby")
    to_stations = _sl.get_every_station("Sundbyberg")
    #print(to_stations)
    # sets travel station, index 0 will always be the search /most similar
    _sl.from_station = from_stations[0]
    _sl.to_station = to_stations[0]
    
    array = _sl.set_trip()
    for i in array:
        print(i)
        print("\n")
    


    """ Trakt testing"""
    #print(_trakt.get_movie("Batman"))

    """ Weather testing"""
    #fos = Weather()
    #fos.set_forecast()

    """ Fitbit """
    #_fitbit.run()

    



