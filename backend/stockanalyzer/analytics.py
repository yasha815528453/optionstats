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
        dateHelper = date_util.DateHelper()
        date_today = dateHelper.get_todays_string()
        #To fill API NaN or -999 values with previous values...
        previous_volatility = 30
        previous_put_delta = -0.03
        previous_call_delta = 0.97
        previous_gamma = 0.005
        previous_rho = 0.0

        for optionmap in optionmaps:
            for expDate, dateContent in optionsdata[optionmap].items():
                expDate = expDate[0:10]
                for strikeprice, data in dateContent.items():
                    data = data[0]
                    strike = float(strikeprice)

                    if data['totalVolume'] == 0:
                        data['lowPrice'] = data['last']
                        data['highPrice'] = data['last']


                    if data['volatility'] == -999 or data['volatility'] == 'NaN' or data['delta'] == 'NaN':
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
                    type = optionmap[0]
                    compiled_data = (data['symbol'], type, optionsdata['symbol'], strike, expDate,data['mark'], data['bid'],
                                     data['ask'], data['daysToExpiration'], data['lowPrice'], data['highPrice'], data['lowPrice'], data['highPrice'],
                                     date_today, date_today, data['volatility'], data['totalVolume'], data['openInterest'],
                                     data['delta'], data['gamma'], date_today, data['markPercentChange'], -data['markPercentChange'], data['rho'], ITM
                                     )
                    self.write_db_manager.insert_options(compiled_data)


    def daily_api_options_breakdown(self, optionsdata):
        calculator = calc_util.Calculator()

        optionmaps = ['putExpDateMap', 'callExpDateMap']
        Datehelper = date_util.DateHelper()
        date_today = Datehelper.get_todays_string()

        previous_volatility = 30
        previous_put_delta = -0.03
        previous_call_delta = 0.97
        previous_gamma = 0.005
        previous_rho = 0.0

        for optionmap in optionmaps:
            for expDate, dateContent in optionsdata[optionmap].items():
                expDate = expDate[0:10]
                for strikeprice, data in dateContent.items():
                    data = data[0]

                    strike = float(strikeprice)


                    #### fixing bad values from api


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

                    if data['totalVolume'] == 0:
                        data['lowPrice'] = data['last'] if data['last'] < data['mark'] else data['mark']
                        data['highPrice'] = data['last'] if data['last'] > data['mark'] else data['mark']
                    ## calculate lowest and highest
                    else:
                        data['lowPrice'] = calculator.calc_abslow(data['totalVolume'], data['lowPrice'], data['ask'])
                        data['highPrice'] = calculator.calc_abshigh(data['totalVolume'], data['bid'], data['highPrice'])
                    ITM = "Y" if data['inTheMoney'] == True else 'N'
                    ## updating record or inserting
                    option_record = self.read_db_manager.check_option_exist(data['symbol'])

                    if option_record: # option exists in db
                        option_record = option_record[0]
                        if option_record['absLow'] == 0 and data['last'] != 0:
                            option_record['absLow'] = data['last']
                            option_record['absHigh'] = data['last']
                        elif option_record['absLow'] == 0 and data['mark'] != 0:
                            option_record['absLow'] = data['mark']
                            option_record['absHigh'] = data['mark']
                        elif option_record['absLow'] == 0:
                            option_record['absLow'] = 1
                            option_record['absHigh'] = 0.01

                        up_perf = round((data['highPrice']/option_record['absLow']) * 100, 1)
                        down_perf = round(((data['lowPrice'] - option_record['absHigh'])/option_record['absHigh'])* 100, 1)

                        if option_record['absLow'] > data['lowPrice']:
                            abs_low_date = date_today
                        else:
                            data['lowPrice'] = option_record['absLow']
                            abs_low_date = option_record['absLDate']
                        if option_record['absHigh'] < data['highPrice']:
                            abs_high_date = date_today
                        else:
                            data['highPrice'] = option_record['absHigh']
                            abs_high_date = option_record['absHDate']

                        if option_record['absLow'] == 0 or option_record['absHigh'] == 0:
                            up_perf = 1
                            down_perf = -1
                        updateData = (data['daysToExpiration'], data['mark'], data['bid'], data['ask'], data['lowPrice'],
                                    data['highPrice'], option_record['absLow'], option_record['absHigh'], abs_low_date, abs_high_date,
                                    data['volatility'], data['totalVolume'], data['openInterest'], data['delta'], data['gamma'],
                                    date_today, up_perf, down_perf, data['rho'], ITM, data['symbol'])

                        self.write_db_manager.update_options(updateData)



                    else:   # does not exist, insert new

                        if data['highPrice'] == 0 and data['last'] != 0:
                            data['highPrice'] = data['last']
                            data['lowPrice'] = data['last']
                        elif data['highPrice'] == 0:
                            data['highPrice'] = data['mark']
                            data['lowPrice'] = data['mark']
                        type = optionmap[0]
                        insert_data = (data['symbol'], type, optionsdata['symbol'], strike, expDate, data['mark'], data['bid'],
                                        data['ask'], data['daysToExpiration'], data['lowPrice'], data['highPrice'], data['lowPrice'], data['highPrice'],
                                        date_today, date_today, data['volatility'], data['totalVolume'], data['openInterest'],
                                        data['delta'], data['gamma'], date_today, 1, 1, data['rho'], ITM
                                        )
                        self.write_db_manager.insert_options(insert_data)



    def option_perf_aggregate(self, symbol, option_records):

        calls = option_records[option_records['type'] == 'c']
        puts = option_records[option_records['type'] == 'p']
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

        previous_record = previous_record[0]


        calls = option_records[option_records['type'] == 'c']
        itm_calls = calls[calls['ITM'] == 'Y']
        otm_calls = calls[calls['ITM'] == 'N']
        puts = option_records[option_records['type'] == 'p']
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
        aggre_info['volatility'] = self._30day_volatility(option_records)

        aggre_info['avgvola'] = calculator.calc_avg(previous_record['avgvola'], aggre_info['volatility'])

        aggre_info['oi'] = aggre_info['putoi'] + aggre_info['calloi']

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
        previous_record = previous_record[0]
        cratio = 1 if previous_record['callvolume'] < 300 else (previous_record['otmcallvolume'] / (1 if previous_record['itmcallvolume'] == 0 else previous_record['itmcallvolume']))
        pratio = 1 if previous_record['putvolume'] < 300 else (previous_record['otmputvolume'] / (1 if previous_record['itmputvolume'] == 0 else previous_record['itmputvolume']))
        coiratio = 1 if previous_record['calloi'] < 500 else (previous_record['otmcalloi'] / (1 if previous_record['itmcalloi'] == 0 else previous_record['itmcalloi']))
        poiratio = 1 if previous_record['putoi'] < 500 else (previous_record['otmputoi'] / (1 if previous_record['itmputoi'] == 0 else previous_record['itmputoi']))
        voloi = 1 if previous_record['volume'] < 200 else (previous_record['volume'] / (1 if previous_record['oi'] == 0 else previous_record['oi']))
        cpratio = 1 if previous_record['volume'] < 200 else (previous_record['callvolume'] / (1 if previous_record['putvolume'] == 0 else previous_record['putvolume']))
        insert_data = (cratio, pratio, coiratio, poiratio, voloi, cpratio, symbol)
        self.write_db_manager.update_specu_ratio(insert_data)

    def price_skews_bydate(self, symbol, interest_rate, closingprice, expiration_map, options_sorted):
        calculator = calc_util.Calculator()
        datehelper = date_util.DateHelper()
        date_today = datehelper.get_todays_string()
        exp_date = datehelper.get_datetime_delta(15)
        self.write_db_manager.delete_old_records("dstock", exp_date)

        options_by_exp = {}
        options_sorted = options_sorted.to_dict('records')


        for option in options_sorted:

            expiry = option['strikedate']

            if option['strikedate'] not in expiration_map or expiration_map[expiry] != option['daysToExpiration']:
                continue

            if expiry not in options_by_exp:
                options_by_exp[expiry] = {'calls': [], 'puts': []}

            if option['type'] == 'c' and option['ITM'] == 'N':
                options_by_exp[expiry]['calls'].append(option)

            elif option['type'] == 'p' and option['ITM'] == 'N':
                options_by_exp[expiry]['puts'].append(option)


        for expiry, option_data in options_by_exp.items():
            try:
                price_skew, callvol, putvol, count = 0, 0, 0, 0

                call_options = option_data['calls']

                put_options = option_data['puts']
                price_diff = self._diff_from_equil(call_options, put_options, closingprice)

                compiledate = expiry

                for i in range(min(len(call_options), len(put_options))):
                    count += 1
                    calls_adjusted = calculator.calc_adjust_option(call_options[i]['marketprice'], price_diff, call_options[i]['delta'],
                                                                    call_options[i]['gamma'], call_options[i]['rho'], interest_rate)
                    puts_adjusted = calculator.calc_adjust_option(put_options[-i]['marketprice'], price_diff, put_options[-i]['delta'],
                                                                    put_options[-i]['gamma'], put_options[-i]['rho'], interest_rate)
                    price_skew += calls_adjusted - puts_adjusted
                    callvol += call_options[i]['volume']
                    putvol += put_options[i]['volume']
                if count == 0:
                    count = 1
                data = (date_today, symbol, compiledate, price_skew/count, callvol, putvol)
                self.write_db_manager.insert_date_aggre(data)
            except Exception as e:
                print(e)

    def _diff_from_equil(self, calls, puts, closingprice):

        call_mid = calls[0]['strikeprice']
        put_mid = puts[-1]['strikeprice']

        equil_price = (call_mid + put_mid) / 2
        return equil_price - closingprice


    def _30day_volatility(self, df):
        df['diff_30'] = (df['daysToExpiration'] - 30).abs()
        mindiff = df['diff_30'].min()
        closest_rows = df[df['diff_30'] == mindiff].copy()

        median_option = closest_rows['strikeprice'].median()

        closest_rows['diff_30']= (closest_rows['strikeprice'] - median_option).abs()

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
