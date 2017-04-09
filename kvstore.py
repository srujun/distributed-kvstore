import asyncio
import logging

from ui import UI
from network import AsyncNetwork

class KVStore:
    def __init__(self, evloop, nodeslist):
        self.evloop = evloop

        self.ui = UI(self.evloop)
        self.network = AsyncNetwork(self.evloop, nodeslist)


    async def main(self):
        await self.network.create_server()

        try:
            while True:
                command = await self.ui.input()
                self.ui.output('Got: ' + command)

        except asyncio.CancelledError:
            self.network.close()
            self.ui.output('\nBYE!')


logging.basicConfig(filename='app.log', level=logging.DEBUG)

with open('nodeslist.txt', 'r') as f:
    nodes = [line.split() for line in f.readlines()]

evloop = asyncio.get_event_loop()
kvstore = KVStore(evloop, nodes)
main_task = evloop.create_task(kvstore.main())

try:
    evloop.run_forever()
except KeyboardInterrupt:
    main_task.cancel()
    evloop.run_until_complete(main_task)
finally:
    evloop.close()
