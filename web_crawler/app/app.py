from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import uvicorn
from typing import Annotated, List
from ticket_hunter import TicketHunter, TicketHunterSchema 
import asyncio
import json

app = FastAPI()

@app.post(
    path='/tickets', 
    response_class=JSONResponse, 
    summary="拿到指定時間最便宜機票"
)
async def get_tickets(
    request_form: Annotated[
        List[TicketHunterSchema.RequestForm],
        Body(
            examples=[
                [
                    {
                        "startDate": "2024-9-1",
                        "endDate": "2024-9-15",
                        'departure': 'TPE',
                        'arrival': 'TYO',
                        'adult': 1
                    },
                    {
                        "startDate": "2024-9-8",
                        "endDate": "2024-9-22",
                        'departure': 'TPE',
                        'arrival': 'TYO',
                        'adult': 1
                    }
                ]
            ]
        )
    ],
) -> JSONResponse:
    thunt = TicketHunter()
    results = []
    for form in request_form:
        result = await thunt.get_tickets(form)
        results.append(result)
    return JSONResponse({'success': True, 'result': results})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
