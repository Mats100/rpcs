from autobahn import wamp
from autobahn.wamp import ApplicationError
from database import sessionLocal
from models import EmployeeData
from schema import Schema
from sqlalchemy import update
from sqlalchemy.future import select


class Register:
    def validate_name(self, name: str):
        return name.isalpha()

    def validate_number(self, phone: str):
        if len(str(phone)) != 11:
            return False
        return True

    @wamp.register('com.test.create', check_types=False)
    async def save_record(self, roll_id: int, name: str, phone: str | int, major: str):
        if not self.validate_name(name):
            raise ApplicationError("validation error", f"name '{name}' is in invalid format")
        if not self.validate_number(phone):
            raise ApplicationError("validation error", f"phone '{phone}' is in invalid format")
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
            query = select(EmployeeData).where(EmployeeData.roll_id == roll_id)
            data = session.execute(query)
            result = data.scalars().first()
        if result is None:
            result = {'msg': f" There is no student with roll ID {roll_id} ."}
        else:
            result = {'status': 'success', 'data': {'name': result.name, 'phone': result.phone, 'major': result.major}}
        return result

    @wamp.register('com.test.update', check_types=True)
    async def update_user(self, roll_id: int, data: dict = None):
        tests = Schema(data)
        user = tests.dict()
        with sessionLocal() as session:
            this_data = session.query(EmployeeData).filter_by(roll_id=roll_id).first()
            update(EmployeeData).values(**user).where(EmployeeData.roll_id == roll_id)
        if this_data:
            result = {'status': 'success',
                      'data': {'name': this_data.name, 'phone': this_data.phone, 'major': this_data.major}}
        else:
            result = {'msg': f" There is no student with roll ID {roll_id} ."}
        return result
