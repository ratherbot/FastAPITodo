from fastapi import WebSocket, Depends, WebSocketDisconnect
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.crud import get_currencies


active_connections = []


async def send_to_all_clients(message: str):
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except Exception as e:
            print(f"Error sending message: {e}")


async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    active_connections.append(websocket)

    try:
        while True:
            message = await websocket.receive_text()

            if message == "get_data":
                data = get_currencies(db)
                await websocket.send_json(data)

                message = "Currency data updated"
                await send_to_all_clients(message)

    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Client disconnected")