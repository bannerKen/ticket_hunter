from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class ticket_hunter:
    def hi():
        return 'hi'
    
    def get_tickets(self, data):
        return data

def main():
    options = Options() 
    # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
    # options.add_argument(f'user-agent={user_agent}')
    options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver_path = '/Users/sehuang/Desktop/chromedriver_mac64/chromedriver'
    # driver = webdriver.Chrome()
    depa = "TPE"
    dest = "OKA"
    trip = "oneway"
    OUT_DATE = conver_date("2024-05-20")
    IN_DATE = conver_date("2024-05-30")
    url = f"https://flight.eztravel.com.tw/tickets-{trip}-{depa}-{dest}/?outbounddate={OUT_DATE}&inbounddate={IN_DATE}&dport=&aport=&adults=1&children=0&infants=0&direct=false&cabintype=&airline=&searchbox=s"
    print(f'url: {url}')
    driver.get(url)
    
    time.sleep(10)
    flight_list_container = driver.find_element(By.CLASS_NAME, "flight-list-contain")
    flight_list = flight_list_container.find_element(By.TAG_NAME, "ul")
    tickets = flight_list.find_elements(By.TAG_NAME, "li")
    for ticket in tickets:
        try:
            flight_single = ticket.find_element(By.CLASS_NAME, "flight-single")
            flight_info = flight_single.find_element(By.CLASS_NAME, "flight-info")
            company = flight_info.find_element(By.CLASS_NAME, 'el-popover__reference')
            depart = flight_info.find_element(By.CLASS_NAME, 'departure-sec').find_element(By.CLASS_NAME, 'time-detail')
            arriv = flight_info.find_element(By.CLASS_NAME, 'arrival-sec').find_element(By.CLASS_NAME, 'time-detail')
            print(f'name: {company.text} time: {depart.text}->{arriv.text}')
            find_price(flight_single)
        except:
            pass
    print(f'len: {len(tickets)}')
    # print(f'flight_list: {flight_list}')

    # driver.quit()

def conver_date(date):
    date = date.split("-")
    date.reverse()
    return "%2F".join(date)

def find_e(parent, by, value):
    return parent.find_element(by, value)

def find_price(flight_single):
    flight_seat_list = flight_single.find_element(By.CLASS_NAME, 'flight-seat-list')
    flight_seats = flight_seat_list.find_elements(By.CLASS_NAME, 'flight-seat')
    for seat in flight_seats:
        flight_seat_price = seat.find_element(By.CLASS_NAME, 'all-money')
        print(f'price: {flight_seat_price.text}')

request = [
    {
        "endDate": "2024-5-15",
        "startDate": "2024-5-1",
        'departure': 'TPE',
        'arrival': 'TYO',
        'adult': 1
    },
    {
        "endDate": "2024-5-22",
        "startDate": "2024-5-8",
        'departure': 'TPE',
        'arrival': 'TYO',
        'adult': 1
    },
    {
        "endDate": "2024-5-29",
        "startDate": "2024-5-15",
        'departure': 'TPE',
        'arrival': 'TYO',
        'adult': 1
    },
    {
        "endDate": "2024-6-5",
        "startDate": "2024-5-22",
        'departure': 'TPE',
        'arrival': 'TYO',
        'adult': 1
    },
    {
        "endDate": "2024-6-12",
        "startDate": "2024-5-29",
        'departure': 'TPE',
        'arrival': 'TYO',
        'adult': 1
    }
]


if __name__ == "__main__":
    main()
