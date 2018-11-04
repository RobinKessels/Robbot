import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer

class Robbot(sc2.BotAI):
    async def on_step(self, iteration):
        # This will be executed every step
        await self.distribute_workers()

run_game(maps.get("(2)16-BitLE"), [
    Bot(Race.Protoss, Robbot()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=True)