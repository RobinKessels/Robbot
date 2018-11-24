import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import *

class Robbot(sc2.BotAI):
    async def on_step(self, iteration):
        # This will be executed every step
        await self.distribute_workers()
        await self.build_workers()
        await self.build_pylons()
        await self.expand()
        await self.build_assimilator()
        await self.build_stalker_tech()
        await self.build_stalkers()

    async def build_workers(self):
        for nexus in self.units(NEXUS).ready.noqueue:
            if self.can_afford(PROBE):
                await self.do(nexus.train(PROBE))

    async def build_pylons(self):
        if self.supply_left < 5:
            nexuses = self.units(NEXUS).ready
            if nexuses.exists:
                if self.can_afford(PYLON) and not self.already_pending(PYLON):
                    await self.build(PYLON, nexuses.first)

    async def expand(self):
        if self.units(NEXUS).amount < 2 and self.can_afford(NEXUS):
            await self.expand_now()

    async def build_assimilator(self):
        for nexus in self.units(NEXUS).ready:
            vespenes = self.state.vespene_geyser.closer_than(10.0, nexus)
            for vespene in vespenes:
                if not self.units(ASSIMILATOR).closer_than(1.0, vespene).exists:
                    if self.can_afford(ASSIMILATOR):
                        worker = self.select_build_worker(vespene.position)
                        if worker is not None:
                            await self.do(worker.build(ASSIMILATOR, vespene))

    async def build_stalker_tech(self):
        if self.units(PYLON).ready.exists:
            pylon = self.units(PYLON).ready.random
            if self.units(GATEWAY).exists and not self.units(CYBERNETICSCORE).exists:
                if self.can_afford(CYBERNETICSCORE) and not self.already_pending(CYBERNETICSCORE):
                    await self.build(CYBERNETICSCORE, near=pylon)
            else:
                if self.can_afford(GATEWAY) and not self.already_pending(GATEWAY):
                    await self.build(GATEWAY, near=pylon)

    async def build_stalkers(self):
        for gateways in self.units(GATEWAY).ready.noqueue:
            if self.can_afford(STALKER) and self.supply_left > 0:
                await self.do(gateways.train(STALKER))

run_game(maps.get("(2)16-BitLE"), [
    Bot(Race.Protoss, Robbot()),
    Computer(Race.Terran, Difficulty.Easy)
], realtime=False)