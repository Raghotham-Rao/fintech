from nsepython import equity_history


class DataLoader:
    req_columns = ['CH_TIMESTAMP', 'CH_SYMBOL', 'CH_TRADE_HIGH_PRICE', 'CH_TRADE_LOW_PRICE', 'CH_OPENING_PRICE', 'CH_CLOSING_PRICE', 'CH_LAST_TRADED_PRICE', 'CH_PREVIOUS_CLS_PRICE', 'CH_TOT_TRADED_QTY', 'CH_52WEEK_HIGH_PRICE', 'CH_52WEEK_LOW_PRICE']
    new_column_names = ['date', 'symbol', 'high', 'low', 'open', 'close', 'ltp', 'prev_close', 'volume', 'high_52w', 'low_52w']

    @staticmethod
    def load_data(script_name, start_date, end_date, series="EQ"):
        df = equity_history(script_name, series, start_date, end_date)
        df = df[DataLoader.req_columns]
        df.columns = DataLoader.new_column_names
        return df