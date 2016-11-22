from autobahn.asyncio.wamp import ApplicationRunner
import os

from . import ExampleGame

runner = ApplicationRunner(
    os.environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
    u'orthogonalspace',
    extra={},
)

runner.run(ExampleGame)
