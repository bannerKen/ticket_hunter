from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn

from ticket_hunter import ticket_hunter 

app = FastAPI()

@app.get(
    path='/tickets', 
    response_class=JSONResponse, 
    summary="拿到指定時間最便宜機票"
)
def get_tickets(request: Request) -> JSONResponse:
    thunt = ticket_hunter()
    req = [
        {
            "endDate": "2024-5-15",
            "startDate": "2024-5-1",
            'departure': 'TPE',
            'arrival': 'TYO',
            'adult': 1
        },
    ]
    tickets = thunt.get_tickets(req)
    return JSONResponse({'success': True, 'result': tickets})

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
