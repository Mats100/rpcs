from autobahn import wamp
from database import sessionLocal
from models import EmployeeData


class Register:

    @wamp.register('com.test.create', check_types=True)
    async def save_record(self, roll_id: int, name: str, phone: int, major: str):
        record = EmployeeData(roll_id=roll_id, name=name, phone=phone, major=major)
        with sessionLocal() as session:
            session.add(record)
            session.commit()
            session.close()
            result = {'status': 'success', 'data': {'roll_id': roll_id, 'name': name, 'phone': phone, 'major': major}}
            return result

    @wamp.register('com.test.get', check_types=True)
    async def get_data(self, roll_id: int):
        with sessionLocal() as session:
            data = session.query(EmployeeData).filter_by(roll_id=roll_id).first()
            session.close()
        if data:
            result = {'status': 'success', 'data': {'name': data.name, 'phone': data.phone, 'major': data.major}}
        else:
            result = {'msg': f" There is no student with roll ID {roll_id} ."}
        return result
