#! /usr/bin/env python3

import asyncio
import sqlite3
import json
import plotly.graph_objs as go
import plotly.io as pio
from datetime import datetime

from autobahn.asyncio.websocket import WebSocketServerProtocol, WebSocketServerFactory

# Connect to SQLite3 database
DB_FILENAME = 'messungen.db'
conn = sqlite3.connect(DB_FILENAME, check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
cursor = conn.cursor()

class MyServerProtocol(WebSocketServerProtocol):
    verbindungen = [] # weakref.WeakSet() aus import weakref
    
    def onConnect(self, request):
        print("Client verbunden: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket-Verbindung geöffnet.")
        self.verbindungen.append(self)

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            message = payload.decode('utf8')
            print("Text message received: {0}".format(message))
            if message == "get_plot":
                self.send_plot()

    def send_plot(self):
        # Query data from the database
        cursor.execute("SELECT date, value FROM temp_aussen")
        rows = cursor.fetchall()
        
        # Extract data for plotting
        dates = [row[0] for row in rows]
        values = [row[1] for row in rows]
        
        # Create a plot using Plotly
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=values, mode='lines+markers', name='Temperature'))
        fig.update_layout(title='Temperature Over Time', xaxis_title='Date', yaxis_title='Temperature (°C)')
        
        # Convert plot to HTML
        plot_html = pio.to_html(fig, full_html=False)
        
        # Send plot HTML via WebSocket
        self.sendMessage(plot_html.encode('utf8'), isBinary=False)

    def onClose(self, wasClean, code, reason):
        print("WebSocket-Verbindung geschlossen: {0}".format(reason))
        if self in self.verbindungen:
            self.verbindungen.remove(self)

def start_server():
    factory = WebSocketServerFactory("ws://192.168.24.100:9000")
    factory.protocol = MyServerProtocol

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '192.168.24.100', 9000)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == "__main__":
    start_server()