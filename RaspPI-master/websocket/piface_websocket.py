import asyncio
import websockets
import json
import sqlite3  # Beispiel für eine Datenbankverbindung

async def get_data(websocket, path):
    while True:
        # Beispiel: Daten aus einer SQLite-Datenbank abrufen
        conn = sqlite3.connect("messungen.db")
        cursor = conn.cursor()
        cursor.execute("SELECT date, value FROM temp_aussen ORDER BY date DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            data = {"date": row[0], "value": row[1]}
            await websocket.send(json.dumps(data))
        
        await asyncio.sleep(1)  # Pause zwischen Updates

start_server = websockets.server(get_data, "0.0.0.0", 9000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()