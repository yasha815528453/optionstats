from .date_util import DateHelper


class StringHelper:

    def optionkey_breakdown(self, key):
        underscore_index = key.index("_") + 1
        CP_index = key.index("C", underscore_index) if "C" in key[underscore_index:] else key.index("P", underscore_index)
        dat = key[underscore_index:CP_index]
        dat = dat[0:2]+'-'+dat[2:4]+'-'+"20"+dat[4:6]
        strike = key[CP_index + 1:]
        return (dat, strike)

    def create_key_expiration(self, optionsdata):
        optionmaps = ['putExpDateMap', 'callExpDateMap']

        expiration_map = {}

        for optionmap in optionmaps:
            for expDate, dateContent in optionsdata[optionmap].items():
                expDate = expDate[0:10]
                for strikeprice, data in dateContent.items():
                    data = data[0]
                    if expDate not in expiration_map:
                        expiration_map[expDate] = data['daysToExpiration']
                        break
        return expiration_map

    def distribute_sql_build(self, table_name, perf_metric, perf_date, key):
        return f"""
            INSERT INTO {table_name} (SYMBOLS, {perf_metric}, {perf_date}, volatility, volume, oi,
            description, category, pricechange, percentchange, closingprice, strikedate, strikeprice)
            SELECT
            perf.SYMBOLS,
            perf.{perf_metric},
            perf.{perf_date},
            opt.volatility,
            opt.volume,
            opt.openinterest AS oi,
            COALESCE(s.description, e.description) AS description,
            COALESCE(s.INDUSTRY, e.CATEGORY) AS category,
            COALESCE(s.pricechange, e.pricechange) AS pricechange,
            COALESCE(s.percentchange, e.percentchange) AS percentchange,
            COALESCE(s.closingprice, e.closingprice) AS closingprice,
            opt.strikedate,
            opt.strikeprice
        FROM
            perfaggre perf
        JOIN
            options opt ON perf.{key} = opt.optionkey
        LEFT JOIN
            tickersS s ON perf.SYMBOLS = s.SYMBOLS
        LEFT JOIN
            tickersE e ON perf.SYMBOLS = e.SYMBOLS
        ORDER BY
            perf.{perf_metric} DESC
        LIMIT 100;
        """
