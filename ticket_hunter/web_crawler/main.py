from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def main():
    options = Options() 
    # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
    # options.add_argument(f'user-agent={user_agent}')
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    depa = "TPE"
    dest = "OKA"
    trip = "oneway"
    OUT_DATE = conver_date("2024-05-01")
    IN_DATE = conver_date("2024-05-30")
    url = f"https://flight.eztravel.com.tw/tickets-{trip}-{depa}-{dest}/?outbounddate={OUT_DATE}&inbounddate={IN_DATE}&dport=&aport=&adults=1&children=0&infants=0&direct=false&cabintype=&airline=&searchbox=s"
    driver.get(url)
    
    time.sleep(10)
    flight_list_container = driver.find_element(By.CLASS_NAME, "flight-list-contain")
    flight_list = flight_list_container.find_element(By.TAG_NAME, "ul")
    tickets = flight_list.find_elements(By.TAG_NAME, "li")
    for ticket in tickets:
        print(f'ticket: {ticket}')
        try:
            flight_single = ticket.find_element(By.CLASS_NAME, "flight-single")

            flight_info = flight_single.find_element(By.CLASS_NAME, "flight-info")
            flight_info_item = flight_info.find_element(By.CLASS_NAME, "flight-list-item")
            flight_list_name = flight_info_item.find_element(By.CLASS_NAME, "flight-list-name")
            flight_list_name_div = flight_list_name.find_element(By.CLASS_NAME, "list-name")
            flight_list_name_span = flight_list_name_div.find_element(By.TAG_NAME, "span")
            flight_list_name_span_span = flight_list_name_span.find_element(By.TAG_NAME, "span")
            flight_list_name_span_span_span = flight_list_name_span_span.find_element(By.TAG_NAME, "span")
            print(f'flight_list_name_span_span_span: {flight_list_name_span_span_span.text}')

            # flight_seat_list = flight_single.find_element(By.CLASS_NAME, "flight-seat-list")

        except:
            print("No flight-single")
    print(f'len: {len(tickets)}')
    # print(f'flight_list: {flight_list}')

    # driver.quit()

def conver_date(date):
    date = date.split("-")
    date.reverse()
    return "%2F".join(date)

def find_e(parent, by, value):
    return parent.find_element(by, value)

if __name__ == "__main__":
    main()
