from autobahn import wamp
from autobahn.wamp import ApplicationError
from database import sessionLocal
from models import EmployeeData


class Register:
    def validate_name(self, name: str):
        return name.isalpha()

    def validate_number(self, phone: str):
        if len(str(phone)) != 11:
            return False
        return True

    @wamp.register('com.test.create', check_types=True)
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
            data = session.query(EmployeeData).filter_by(roll_id=roll_id).first()
            session.close()
        if data:
            result = {'status': 'success', 'data': {'name': data.name, 'phone': data.phone, 'major': data.major}}
        else:
            result = {'msg': f" There is no student with roll ID {roll_id} ."}
        return result
