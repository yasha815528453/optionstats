from .date_util import DateHlper


class StringHelper:

    def optionkey_breakdown(self, key):
        underscore_index = key.index("_") + 1
        CP_index = key.index("C", underscore_index) if "C" in key[underscore_index:] else key.index("P", underscore_index)
        dat = key[underscore_index:CP_index]
        dat = dat[0:2]+'-'+dat[2:4]+'-'+"20"+dat[4:6]
        strike = key[CP_index + 1:]
        return (dat, strike)

    def initial_api_option_response_break(self, optionsdata):
        optionmaps = ['putExpDateMap', 'callExpDateMap']
        date_today = DateHlper.get_todays_string()

        #To fill API NaN or -999 values with previous values...
        previous_volatility = 30
        previous_put_delta = -0.03
        previous_call_delta = 0.97
        previous_gamma = 0.005
        previous_rho = 0.0

        for optionmap in optionmaps:
            for expDate, dateContent in optionsdata[optionmap]:
                for strikeprice, data in dateContent.items():
                    data = data[0]
                    strike = float(strikeprice)

                    if data['volatility'] == -999 or data['volatility'] == 'NaN':
                        data['volatility'] = previous_volatility
                        data['gamma'] = previous_gamma
                        data['rho'] = previous_rho
                        if optionmap == 'putExpDateMap':
                            data['delta'] = previous_put_delta
                        else:
                            data['delta'] = previous_call_delta

    def distribute_sql_build(self, perf_metric, perf_date, key, table_name):
        return f"""
            INSERT INTO {table_name} (SYMBOLS, {perf_metric}, {perf_date}, volatility, volume, oi,
            description, category, pricechange, percentchange, closingprice, strikedate, strikeprice)
            SELECT
            perf.SYMBOLS,
            perf.{perf_metric},
            perf.{perf_date},
            option.volatility,
            option.volume,
            option.openinterest AS oi,
            COALESCE(s.description, s.description) AS description,
            COALESCE(s.INDUSTRY, e.CATEGORY) AS category,
            COALESCE(s.pricechange, e.pricechange) AS pricechange,
            COALESCE(s.percentchange, e.percentchange) AS percentchange,
            COALESCE(s.closingprice, e.closingprice) AS closingprice,
            option.strikedate,
            option.strikeprice,
        FROM
            perfaggre perf
        JOIN
            options option ON perf.{key} = option.optionkey
        LEFT JOIN
            tickersS s ON perf.SYMBOLS = s.SYMBOLS
        LEFT JOIN
            tickersE e ON perf.SYMBOLS = e.SYMBOLS
        ORDER BY
            perf.{perf_metric} DESC
        LIMIT 100;
        """
