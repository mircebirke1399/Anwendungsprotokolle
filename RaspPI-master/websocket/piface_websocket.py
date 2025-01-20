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

async def main():
    # WebSocket-Server starten
    async with websockets.serve(get_data, "0.0.0.0", 9000):
        print("WebSocket-Server läuft auf Port 9000...")
        await asyncio.Future()  # Blockiert, damit der Server weiterläuft

if __name__ == "__main__":
    asyncio.run(main())