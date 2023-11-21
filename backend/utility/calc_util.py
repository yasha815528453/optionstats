
class Calculator:

    def calc_abslow(self, volume, lowprice, marketprice):
        if volume > 1000:
            return lowprice
        else:
            middle = (lowprice + marketprice) / 2
            return middle + volume/1000 * (lowprice - middle)


    def calc_abshigh(self, volume, marketprice, highprice):
        if volume > 1000:
            return highprice
        else:
            middle = (highprice + marketprice) / 2
            return middle + volume/1000 * (middle - highprice)

    def calc_avg(self, avg_value, value):
        return ((29 * avg_value + value)/30)

    def calc_adjust_option(self, market_price, price_diff, delta, gamma, rho, interest):
        return market_price - (rho*interest) - (price_diff * delta) + (price_diff**2 * gamma)
