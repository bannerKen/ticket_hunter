from fastapi import HTTPException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from ._schema import TicketHunterSchema, Direction

class BaseService():
    _response: dict | None = None

    def process(self) -> None:
        pass

    @property
    def response(self) -> dict:
        if self._response is None:
            raise HTTPException(
                status_code=500,
                detail="Unknown Internal server error.",
            )
        return self._response
    
class Crawler(BaseService):
    _result: dict | None

    def __init__(self, request_form: TicketHunterSchema.RequestForm) -> None:
        self.__set_options()
        self.__set_driver()
        self._request_form = request_form

    def __set_options(self) -> None:
        self.options = Options()
        self.options.add_argument('--headless')

    def __set_driver(self) -> None:
        self.driver = webdriver.Chrome(options=self.options)

    async def process(self) -> None:
        result = {
            Direction.GO: self.claw(Direction.GO),
            Direction.BACK: self.claw(Direction.BACK)
        }
        if result[Direction.GO] and result[Direction.BACK]:
            self._result = result
        

    def claw(self, direction: Direction) -> None:
        claw_result = {}
        if direction == Direction.GO:
            url = f"https://flight.eztravel.com.tw/tickets-oneway-{self._request_form.departure}-{self._request_form.arrival}/?outbounddate={self.conver_date(self._request_form.startDate)}&adults={self._request_form.adult}&direct=true&searchbox=s"
        elif direction == Direction.BACK:
            url = f"https://flight.eztravel.com.tw/tickets-oneway-{self._request_form.arrival}-{self._request_form.departure}/?outbounddate={self.conver_date(self._request_form.endDate)}&adults={self._request_form.adult}&direct=true&searchbox=s"
        
        self.driver.get(url)
        get_data = False
        iteration = 10
        for i in range(iteration):
            print(f'iteration: {i}')
            if not get_data:
                time.sleep(1)
                try:
                    flight_list_container = self.driver.find_element(By.CLASS_NAME, "flight-list-contain")
                    flight_list = flight_list_container.find_element(By.TAG_NAME, "ul")
                    tickets = flight_list.find_elements(By.TAG_NAME, "li")
                    if isinstance(tickets, list):
                        for ticket in tickets:
                            try:
                                flight_single = ticket.find_element(By.CLASS_NAME, "flight-single")
                                flight_info = flight_single.find_element(By.CLASS_NAME, "flight-info")
                                company = flight_info.find_element(By.CLASS_NAME, 'el-popover__reference').text
                                depart = flight_info.find_element(By.CLASS_NAME, 'departure-sec').find_element(By.CLASS_NAME, 'time-detail').text
                                arriv = flight_info.find_element(By.CLASS_NAME, 'arrival-sec').find_element(By.CLASS_NAME, 'time-detail').text
                                flight_seat_list = flight_single.find_element(By.CLASS_NAME, 'flight-seat-list')
                                flight_seats = flight_seat_list.find_elements(By.CLASS_NAME, 'flight-seat')
                                for seat in flight_seats:
                                    flight_seat_price = int(seat.find_element(By.CLASS_NAME, 'all-money').text.replace(',', ''))
                                    if 'price' in claw_result:
                                        if claw_result['price'] > flight_seat_price:
                                            claw_result['company'] = company
                                            claw_result['price'] = flight_seat_price
                                            claw_result['depart'] = depart
                                            claw_result['arriv'] = arriv
                                    else:
                                        claw_result = {
                                            'company': company,
                                            'price': flight_seat_price,
                                            'depart': depart,
                                            'arriv': arriv
                                        }
                            except:
                                pass
                        print(f'result: {claw_result}')
                        if 'price' in claw_result:
                            get_data = True
                            return claw_result
                except:
                    pass
            else:
                break

    def build_response(self) -> None:
        if self._result:
            try:
                self._response = {
                    "startDate": self._request_form.startDate.strftime('%Y/%m/%d'),
                    "endDate": self._request_form.endDate.strftime('%Y/%m/%d'),
                    "total": self._result[Direction.GO]['price']+self._result[Direction.BACK]['price'],
                    "go": self._result[Direction.GO],
                    "back": self._result[Direction.BACK]
                }
            except:
                pass
    
    def conver_date(self, date: str) -> str:
        date_list = date.split('-')[::-1]
        return '%2f'.join(date_list)