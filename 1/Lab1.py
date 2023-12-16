import matplotlib
import matplotlib.pyplot as plt
import requests
import datetime
from matplotlib.dates import DateFormatter

def visualize_data(data_set: list[dict]) -> None:
    ax = plt.figure().add_subplot(projection='3d')
    ax.set_xlabel("Date")
    ax.set_ylabel("USD Exchange Rate")
    ax.set_zlabel("Change")

    ax.xaxis.set_major_locator(matplotlib.dates.AutoDateLocator())
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%Y-%m-%d"))

    x_values = []
    y_values = []
    z_values = []

    for entry in data_set:
        x_values.append(entry.get("date"))
        y_values.append(entry.get("usd"))
        z_values.append(entry.get("delta"))

    x_dates = matplotlib.dates.date2num(x_values)
    ax.plot(x_dates, y_values, z_values)
    plt.show()

def calculate_exchange_rate_changes(data_set: list[dict]) -> list[dict]:
    processed_data = []
    next_entry = None
    length = len(data_set)
    key = "usd"
    
    for index, current_entry in enumerate(data_set):
        if index < (length - 1):
            next_entry = data_set[index + 1]

        previous_usd = current_entry[key]
        current_usd = next_entry[key]
        processed_data.append({**current_entry, "delta": (previous_usd - current_usd) / current_usd * 100})

    return processed_data

def fetch_exchange_rate_data(prepared_dates: list) -> list[dict]:
    data_collection = []
    
    for current_date in prepared_dates:
        link_template = 'https://www.cbr-xml-daily.ru/archive/{}/{}/{}/daily_json.js'

        month = '0' + str(current_date.month) if current_date.month < 10 else current_date.month
        day = '0' + str(current_date.day) if current_date.day < 10 else current_date.day

        link = link_template.format(current_date.year, month, day)
        request = requests.get(link)
        parsed_request = request.json()
        usd_rate = parsed_request['Valute']['USD']['Value']

        data_collection.append({"date": current_date, "usd": usd_rate})

    return data_collection

def generate_dates() -> list[datetime]:
    date_count = 14
    selected_dates = []
    date_today = datetime.datetime.today()

    for i in range(date_count):
        previous_date = date_today - datetime.timedelta(days=1)
        date_today = previous_date

        if previous_date.weekday() == 0 or previous_date.weekday() == 6:
            continue

        selected_dates.append(previous_date.date())

    return selected_dates

if __name__ == '__main__':
    selected_dates = generate_dates()
    base_data = fetch_exchange_rate_data(selected_dates)
    processed_data = calculate_exchange_rate_changes(base_data)
    visualize_data(processed_data)