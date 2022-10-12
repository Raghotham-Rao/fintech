from utils.load_data import DataLoader
from datetime import datetime, timedelta

script_name = 'INFY'
series = 'EQ'
end_date = datetime.now().date()
start_date = end_date - timedelta(days = 365)

df = DataLoader.load_data(
    script_name, 
    start_date.strftime("%d-%m-%Y"), 
    end_date.strftime("%d-%m-%Y"), 
    series).sort_values('date').drop_duplicates()

print(df.count())