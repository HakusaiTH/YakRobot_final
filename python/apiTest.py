from fastapi import FastAPI, HTTPException, Request  # Add 'Request' here

app = FastAPI()

@app.post("/receive-data")
async def receive_data(request: Request):
    try:
        data = await request.json()
        print("Received data:", data)
        return {"status": "success", "message": "Data received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
