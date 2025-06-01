import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

class StockData:
    def __init__(self, file_path, output_path):
        self.stocks = pd.read_csv(file_path)
        self.symbols = self.stocks['Symbol']
        self.output_path = output_path
        self.end_date = datetime.today()
        self.start_date = datetime.today() - timedelta(days=1)
        self.two_days_backdata = datetime.today() - timedelta(days=2)

    def get_stock_data(self):
        tickers = [f"{symbol}.NS" for symbol in self.symbols]

        try:
            data = yf.download(tickers, start=self.two_days_backdata, end=self.end_date, progress=False)['Close']

            if data.empty:
                print("No data was returned for any of the tickers.")
                return

            stock_list = []
            for symbol in self.symbols:
                col_name = f"{symbol}.NS"
                if col_name in data.columns:
                    try:
                        close_price = data[col_name].iloc[-1]
                        previous_close = data[col_name].iloc[0]
                        percent_change = ((close_price - previous_close) / previous_close) * 100

                        if pd.notna(close_price) and pd.notna(previous_close):
                            stock_list.append({
                                'Symbol': symbol,
                                'Close Price': close_price,
                                'Previous Close': previous_close,
                                'percent_change': percent_change
                            })
                        else:
                            print(f"{symbol}: Incomplete data.")
                    except IndexError:
                        print(f"{symbol}: Not enough data points.")
                else:
                    print(f"{symbol}: No data available for the given date range.")

            if stock_list:
                df = pd.DataFrame(stock_list)
                df.to_csv(self.output_path, mode='a', index=False, header=not os.path.exists(self.output_path))
                print("Saved successfully")

        except Exception as e:
            print(f"Error fetching stock data: {e}")

    @staticmethod
    def new_func(end):
        return f"D:\\project1\\pycode\\stocks_list\\stock_list-{end}.csv"

if __name__ == '__main__':
    file_path = "D:\\project1\\pycode\\stocks_list\\nifty50.csv"
    end = datetime.today().strftime("%Y-%m-%d")
    output_path = StockData.new_func(end)
    s = StockData(file_path, output_path)
    s.get_stock_data()

