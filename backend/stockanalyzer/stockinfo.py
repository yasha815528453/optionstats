
class StockHelper:

    def useful_options_size(self, tda_data):
        strike_size = 0
        shortest_date, longest_date = 1000, 0
        for expDate, expDatedict in tda_data['callExpDateMap'].items():
            for strikeprice, info in expDatedict.items():
                volume = info[0]['totalVolume']
                oi = info[0]['openInterest']
                if volume >= 5 or oi >= 5:
                    strike_size += 1
            if strike_size < shortest_date:
                shortest_date = strike_size
            if strike_size > longest_date:
                longest_date = strike_size
            strike_size = 0

        strike_size = (shortest_date + longest_date) // 2
        if strike_size < 10:
            return 10
        elif strike_size >= 60:
            return 60
        return strike_size
