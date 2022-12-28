from API.AFTONBLADET.aftonbladet import Aftonbladet
from API.CRYPTO.coinmarketcap import CoinMarketCap
from API.HUE.hue import Hue
from API.SL_TRAFFIC.fooo_sl import SL
from API.TRAKT.trakt import Trakt
from API.WEATHER.weather import Weather

_aftonbladet = Aftonbladet()
_cmc = CoinMarketCap()
_hue = Hue()
_sl = SL()
_trakt = Trakt()
_weather = Weather()

if __name__ == '__main__':

    """ Aftonbladet testing"""
    #_aftonbladet.get_data_first_article()
    #_aftonbladet.FOO()
    #_aftonbladet.testing()

    """ Crypto testing"""
    """ Hue testing"""
    """ SL testing"""

    """ Trakt testing"""
    print(_trakt.get_movie("Batman"))

    """ Weather testing"""
    #fos = Weather()
    #fos.set_forecast()

    



