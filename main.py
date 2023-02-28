from os import environ
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner
from api import Register


class MyComponent(ApplicationSession):

    async def onJoin(self, details):
        print("Procedure registered")
        registry = Register()
        regs = await self.register(registry)
        for reg in regs:
            print("registered", reg.procedure)
        print('Registered methods; ready for frontend.')


if __name__ == '__main__':
    url = environ.get("wick", "ws://localhost:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(MyComponent)
