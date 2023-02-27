
from os import environ
from autobahn import wamp
from models import EmployeeData
from database import session
from autobahn.asyncio.wamp import ApplicationSession, ApplicationRunner



class MyComponent(ApplicationSession):


    async def onJoin(self, details):
        print("Procedure registered")

        @wamp.register('com.test.create',check_types=True)
        async def save_record(roll_id, name, phone, major):
            record = EmployeeData(roll_id=roll_id, name=name, phone=phone, major=major)
            session.add(record)
            session.commit()
            session.close()

            result = {'status': 'success', 'data': {'roll_id': roll_id, 'name': name, 'phone': phone, 'major': major}}
            return result


        @wamp.register('com.test.get', check_types=True)
        async def get_data(roll_id):
            data = session.query(EmployeeData).filter_by(roll_id=roll_id).first()
            session.close()
            if data:
                result = {'status': 'success', 'data': {'name': data.name, 'phone': data.phone, 'major': data.major}}
            else:
                result = {'msg': f" There is no student with roll ID {roll_id} ."}
            return result



if __name__ == '__main__':
    url = environ.get("wick", "ws://localhost:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(MyComponent)
