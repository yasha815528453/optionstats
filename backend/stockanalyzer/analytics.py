from enum import Enum
from utility import date_util
from utility import calc_util
import pandas as pd

class OptionsAnalyzer:

    def __init__(self, write_db_manager=None, read_db_manager=None):
        self.write_db_manager = write_db_manager
        self.read_db_manager = read_db_manager

    def initial_api_options_break(self, optionsdata):
        optionmaps = ['putExpDateMap', 'callExpDateMap']
        date_today = date_util.DateHlper.get_todays_string()
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

                    if data['totalVolume'] == 0:
                        data['lowPrice'] = data['last']
                        data['highPrice'] = data['last']


                    if data['volatility'] == -999 or data['volatility'] == 'NaN':
                        data['volatility'] = previous_volatility
                        data['gamma'] = previous_gamma
                        data['rho'] = previous_rho
                        if optionmap == 'putExpDateMap':
                            data['delta'] = previous_put_delta
                        else:
                            data['delta'] = previous_call_delta
                    else:
                        previous_volatility = data['volatility']
                        previous_gamma = data['gamma']
                        previous_rho = data['rho']
                        if optionmap == 'putExpDateMap':
                            previous_put_delta = data['delta']
                        else:
                            previous_call_delta = data['delta']

                    ITM = "Y" if data['inTheMoney'] == True else 'N'

                    compiled_data = (data['symbol'], optionmap[0], optionsdata['symbol'], strike, data['mark'], data['bid'],
                                     data['ask'], data['daysToExpiration'], data['lowPrice'], data['highPrice'], data['lowPrice'], data['highPrice'],
                                     date_today, date_today, data['volatility'], data['totalVolume'], data['openInterest'],
                                     data['delta'], data['gamma'], date_today, data['markPercentChange'], -data['markPercentChange'], data['rho'], ITM
                                     )
                    self.write_db_manager.insert_options(compiled_data)


    def daily_api_options_breakdown(self, optionsdata):
        calculator = calc_util.Calculator()

        optionmaps = ['putExpDateMap', 'callExpDateMap']
        date_today = date_util.DateHlper.get_todays_string()

        previous_volatility = 30
        previous_put_delta = -0.03
        previous_call_delta = 0.97
        previous_gamma = 0.005
        previous_rho = 0.0

        for optionmap in optionmaps:
            for expDate, dateContent in optionsdata[optionmap]:
                expDate = expDate[0:10]
                for strikeprice, data in dateContent.items():
                    data = data[0]
                    strike = float(strikeprice)


                    #### fixing bad values from api
                    if data['totalVolume'] == 0:
                        data['lowPrice'] = data['last'] if data['last'] < data['mark'] else data['mark']
                        data['highPrice'] = data['last'] if data['last'] > data['mark'] else data['mark']

                    if data['volatility'] == -999 or data['volatility'] == 'NaN':
                        data['volatility'] = previous_volatility
                        data['gamma'] = previous_gamma
                        data['rho'] = previous_rho
                        if optionmap == 'putExpDateMap':
                            data['delta'] = previous_put_delta
                        else:
                            data['delta'] = previous_call_delta
                    else:
                        previous_volatility = data['volatility']
                        previous_gamma = data['gamma']
                        previous_rho = data['rho']
                        if optionmap == 'putExpDateMap':
                            previous_put_delta = data['delta']
                        else:
                            previous_call_delta = data['delta']

                    ## calculate lowest and highest
                    data['lowPrice'] = calculator.calc_abslow(data['totalVolume'], data['lowPrice']), data['ask']
                    data['highPrice'] = calculator.calc_abshigh(data['totalVolume'], data['bid'], data['highPrice'])
                    ITM = "Y" if data['inTheMoney'] == True else 'N'
                    ## updating record or inserting
                    option_record = self.read_db_manager.check_option_exist(data['symbol'])
                    if option_record: # option exists in db
                        if option_record[0]['absLow'] > data['lowPrice']:
                            abs_low_date = date_today
                        else:
                            data['lowPrice'] = option_record[0]['absLow']

                        if option_record[0]['absHigh'] < data['highPrice']:
                            abs_high_date = date_today
                        else:
                            data['highPrice'] = option_record[0]['absHigh']

                        up_perf = round((data['highPrice']/option_record[0]['absLow']) * 100, 1)
                        down_perf = round(((data['lowPrice'] - option_record[0]['absHigh'])/option_record[0]['absHigh'])* 100, 1)

                        if option_record[0]['absLow'] == 0 or option_record[0]['absHigh'] == 0:
                            up_perf = 1
                            down_perf = -1

                        updateData = (data['daysToExpiration'], data['mark'], data['bid'], data['ask'], data['lowPrice'],
                                    data['highPrice'], data['lowPrice'], data['highPrice'], abs_low_date, abs_high_date,
                                    data['volatility'], data['totalVolume'], data['openInterest'], data['delta'], data['gamma'],
                                    date_today, up_perf, down_perf, data['rho'], ITM, data['symbol'])

                        self.write_db_manager.update_options(updateData)




                    else:   # does not exist, insert new
                        insert_data = (data['symbol'], optionmap[0], optionsdata['symbol'], strike, expDate, data['mark'], data['bid'],
                                        data['ask'], data['daysToExpiration'], data['lowPrice'], data['highPrice'], data['lowPrice'], data['highPrice'],
                                        date_today, date_today, data['volatility'], data['totalVolume'], data['openInterest'],
                                        data['delta'], data['gamma'], date_today, data['markPercentChange'], -data['markPercentChange'], data['rho'], ITM
                                        )
                        self.write_db_manager.insert_options(insert_data)



    def option_perf_aggregate(self, symbol, option_records):

        df_options = pd.DataFrame(option_records)

        calls = df_options[df_options['type'] == 'C']
        puts = df_options[df_options['type'] == 'P']

        todays_best_call = calls.loc[calls['upperformance'].idxmax()]
        todays_worst_call = calls.loc[calls['downperformance'].idxmin()]
        todays_best_put = puts.loc[puts['upperformance'].idxmax()]
        todays_worst_put = puts.loc[puts['downperformance'].idxmin()]

        update_data = (todays_best_call['optionkey'], todays_best_call['upperformance'], todays_best_call['absLDate'],
                       todays_worst_call['downperformance'], todays_worst_call['absHDate'], todays_worst_call['optionkey'],
                       todays_best_put['optionkey'], todays_best_put['upperformance'], todays_best_put['absLDate'],
                       todays_worst_put['downperformance'], todays_worst_put['absHDate'], todays_worst_put['optionkey'],
                       symbol)

        self.write_db_manager.update_option_perf(update_data)



    def option_stats_aggregate(self, option_records, symbol, totalotmcall=None, totalotmput=None, totalotmcoi = None,
                         totalotmputoi = None):
        calculator = calc_util.Calculator()
        aggre_info = self._initialize_option_aggre_context()
        previous_record = self.read_db_manager.get_stats_aggre(symbol)
        df_options = pd.DataFrame(option_records)

        calls = df_options[df_options['type'] == 'C']
        itm_calls = calls[calls['ITM'] == 'Y']
        otm_calls = calls[calls['ITM'] == 'N']
        puts = df_options[df_options['type'] == 'P']
        itm_puts = puts[puts['ITM'] == 'Y']
        otm_puts = puts[puts['ITM'] == 'N']

        aggre_info['callvolume'] = calls['volume'].sum()
        aggre_info['putvolume'] = puts['volume'].sum()
        aggre_info['calloi'] = calls['openinterest'].sum()
        aggre_info['putoi'] = puts['openinterest'].sum()
        aggre_info['OTM_calls'] = otm_calls['volume'].sum()
        aggre_info['ITM_calls'] = itm_calls['volume'].sum()
        aggre_info['OTM_puts'] = otm_puts['volume'].sum()
        aggre_info['ITM_puts'] = itm_puts['volume'].sum()
        aggre_info['OTM_calloi'] = otm_calls['openinterest'].sum()
        aggre_info['ITM_calloi'] = itm_calls['openinterest'].sum()
        aggre_info['OTM_putoi'] = otm_puts['openinterest'].sum()
        aggre_info['ITM_putoi'] = itm_puts['openinterest'].sum()
        aggre_info['volatility'] = self._30day_volatility(df_options)
        aggre_info['avgvola'] = calculator.calc_avg(previous_record['avgvola'], aggre_info['volatility'])
        aggre_info['oi'] = aggre_info['putoi'] + aggre_info['caloi']
        aggre_info['avgoi'] = calculator.calc_avg(previous_record['avgoi'], aggre_info['oi'])
        aggre_info['volume'] = aggre_info['callvolume'] + aggre_info['putvolume']
        aggre_info['avgvolume'] = calculator.calc_avg(previous_record['avgvolume'], aggre_info['volume'])
        aggre_info['SYMBOLS'] = symbol
        update_data = tuple(aggre_info.values())
        self.write_db_manager.update_option_stats(update_data)

        #for etfs
        if totalotmcall == None:
            return None
        else:
            return (totalotmcall + aggre_info['OTM_calls'], totalotmput + aggre_info['OTM_puts'],
                    totalotmcoi + aggre_info['OTM_calloi'], totalotmputoi + aggre_info['OTM_putoi'])

    def speculative_ratio(self, symbol):
        previous_record = self.read_db_manager.get_stats_aggre(symbol)

        cratio = 1 if previous_record['callvolume'] < 300 else previous_record['OTM_calls'] / previous_record['ITM_calls']
        pratio = 1 if previous_record['putvolume'] < 300 else previous_record['OTM_puts'] / previous_record['ITM_puts']
        coiratio = 1 if previous_record['calloi'] < 500 else previous_record['OTM_calloi'] / previous_record['ITM_calloi']
        poiratio = 1 if previous_record['putoi'] < 500 else previous_record['OTM_putoi'] / previous_record['ITM_putoi']
        voloi = previous_record['volume'] / previous_record['oi']
        cpratio = previous_record['callvolume'] / previous_record['putvolume']

        insert_data = (cratio, pratio, coiratio, poiratio, voloi, cpratio, symbol)
        self.write_db_manager.update_specu_ratio(insert_data)

    def price_skews_bydate(self, symbol, interest_rate, closingprice):
        calculator = calc_util.Calculator()
        datehelper = date_util.DateHlper()
        date_today = datehelper.get_todays_string()
        exp_date = datehelper.get_datetime_delta(15)
        self.write_db_manager.delete_old_records("dstock", exp_date)
        options_sorted = self.read_db_manager.get_options_sorted(symbol)
        options_by_exp = {}
        for option in options_sorted:
            expiry = option['daysToExpiration']
            if expiry not in options_by_exp:
                options_by_exp[expiry] = {'calls': [], 'puts': []}

            if option['type'] == 'C' and option['ITM'] == 'N':
                options_by_exp[expiry]['calls'].append(option)
            elif option['type'] == 'P' and option['ITM'] == 'N':
                options_by_exp[expiry]['puts'].append(option)

        for expiry, option_data in options_by_exp.items():
            price_skew, callvol, putvol = 0, 0, 0
            call_options = option_data['calls']
            put_options = option_data['puts']
            price_diff = self._diff_from_equil(call_options, put_options, closingprice)
            compiledate = option_data[0]['strikedate']
            for i in range(len(call_options)):
                calls_adjusted = calculator.calc_adjust_option(call_options[i]['mark'], price_diff, call_options[i]['delta'],
                                                                call_options[i]['gamma'], call_options[i]['rho'], interest_rate)
                puts_adjusted = calculator.calc_adjust_option(put_options[i]['mark'], price_diff, put_options[i]['delta'],
                                                                put_options[i]['gamma'], put_options[i]['rho'], interest_rate)
                price_skew += calls_adjusted - puts_adjusted
                callvol += call_options[i]['volume']
                putvol += put_options[i]['volume']

            data = (date_today, symbol, compiledate, price_skew, callvol, putvol)
            self.write_db_manager.insert_date_aggre(data)

    def _diff_from_equil(calls, puts, closingprice):
        call_mid = calls[0]['mark']
        put_mid = puts[-1]['mark']

        equil_price = (call_mid + put_mid) / 2
        return equil_price - closingprice


    def _30day_volatility(self, df):
        df['diff_30'] = (df['daysToExpiration'] - 30).abs()
        mindiff = df['diff_30'].min()
        closest_rows = df[df['diff_30'] == mindiff]

        median_option = closest_rows['strikeprice'].median()
        closest_rows['diff_30'] = (closest_rows['strikeprice'] - median_option).abs()
        mindiff = closest_rows['diff_30'].min()
        final = closest_rows[closest_rows['diff_30'] == mindiff]
        if len(final) == 1:
            return final['volatility'].iloc[0]
        else:
            return final['volatility'].mean()

    def _initialize_option_aggre_context(self):
        return {
            'callvolume': 0,
            'putvolume': 0,
            'calloi' : 0,
            'putoi' : 0,
            'OTM_calls': 0,
            'ITM_calls' : 0,
            "OTM_puts" : 0,
            'ITM_puts' : 0,
            'OTM_calloi': 0,
            'ITM_calloi' : 0,
            'OTM_putoi' : 0,
            'ITM_putoi' : 0,
            'volatility' : 0,
            'avgvola' : 0,
            'oi' : 0,
            'avgoi' : 0,
            "volume" : 0,
            "avgvolume" : 0,
            "SYMBOLS" : "",
        }
