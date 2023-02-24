import uuid

from autobahn import wamp
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

class Components(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("Session Attached")

    @wamp.register('com.test.create')
    def my_function(*args, **kwargs):
        if len(args) > 4:
            raise ValueError("Too many arguments - expected 4 or less.")
        if len(kwargs) > 1:
            raise ValueError("Too many keyword arguments. The expected value is 1.")






