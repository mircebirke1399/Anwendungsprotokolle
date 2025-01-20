import asyncio
from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory
import json
import sqlite3

class MyServerProtocol(WebSocketServerProtocol):
    async def onConnect(self, request):
        print(f"Neue Verbindung: {request.peer}")

    async def onOpen(self):
        print("Verbindung geöffnet")
        await self.send_data()

    async def onMessage(self, payload, isBinary):
        # Diese Methode wird aufgerufen, wenn eine Nachricht empfangen wird
        print(f"Nachricht erhalten: {payload.decode('utf8')}")
    
    async def onClose(self, wasClean, code, reason):
        print(f"Verbindung geschlossen: {reason}")

    async def send_data(self):
        while True:
            # Datenbankabfrage
            conn = sqlite3.connect("messungen.db")
            cursor = conn.cursor()
            cursor.execute("SELECT date, value FROM temp_aussen ORDER BY date DESC LIMIT 1")
            row = cursor.fetchone()
            conn.close()

            if row:
                data = {"date": row[0], "value": row[1]}
                print(f"Sende Daten: {data}")
                self.sendMessage(json.dumps(data).encode('utf8'))  # Sende die Daten als JSON
            else:
                print("Keine Daten in der Tabelle gefunden.")

            await asyncio.sleep(1)  # Warte 1 Sekunde bevor die nächsten Daten gesendet werden

# Server starten
async def main():
    factory = WebSocketServerFactory("ws://0.0.0.0:9000")
    factory.protocol = MyServerProtocol  # Definiere das Verhalten für die Verbindungen
    loop = asyncio.get_event_loop()
    server = loop.create_server(factory, '0.0.0.0', 9000)
    print("WebSocket-Server läuft auf Port 9000...")
    server = await loop.create_server(factory, '0.0.0.0', 9000)
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
