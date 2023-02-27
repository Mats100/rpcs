from os import environ
from models import MyModel
from database import session
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks


class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print("Procedure registered")

        def save_record(roll_id, name, phone, major):
            record = MyModel(roll_id=roll_id, name=name, phone=phone, major=major)
            session.add(record)
            session.commit()
            session.close()

            result = {'status': 'success', 'data': {'roll_id': roll_id, 'name': name, 'phone': phone, 'major': major}}
            return result

        yield self.register(save_record, 'com.test.create')

        def get_data(roll_id):
            data = session.query(MyModel).filter_by(roll_id=roll_id).first()
            session.close()
            if data:
                result = {'status': 'success', 'data': {'name': data.name, 'phone': data.phone, 'major': data.major}}
            else:
                result = {'msg': f" There is no student with roll ID {roll_id} ."}
            return result

        yield self.register(get_data, 'com.test.get')


if __name__ == '__main__':
    url = environ.get("wick", "ws://localhost:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(MyComponent)
