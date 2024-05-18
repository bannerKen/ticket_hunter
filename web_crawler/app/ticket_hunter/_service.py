from ._schema import TicketHunterSchema
from ._model import Crawler

class TicketHunter:
    async def get_tickets(self, request_form: TicketHunterSchema.RequestForm) -> dict:
        self._crawler = Crawler(request_form)
        await self._crawler.process()
        self._crawler.build_response()
        return self._crawler.response
