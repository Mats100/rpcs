from autobahn import wamp
from autobahn.wamp import ApplicationError
from database import sessionLocal
from models import EmployeeData
from schema import Schema
from sqlalchemy import update
from sqlalchemy.future import select
from pydantic import ValidationError


class Register:
    def validate_name(self, name: str):
        return name.isalpha()

    def validate_number(self, phone: str):
        if len(str(phone)) != 11:
            return False
        return True

    def query(self, roll_id: int, session):
        query = select(EmployeeData).where(EmployeeData.roll_id == roll_id)
        data = session.execute(query)
        return data.scalar()

    @wamp.register('com.test.create', check_types=False)
    async def save_record(self, roll_id: int, name: str, phone: str, major: str):
        if not self.validate_name(name):
            raise ApplicationError("validation error", f"Name '{name}' is in invalid format")
        if not self.validate_number(phone):
            raise ApplicationError("validation error", f"Phone '{phone}' is in invalid format")
        with sessionLocal() as session:
            result = self.query(roll_id, session)
            if result is not None:
                raise ApplicationError("validation error", f" Student with this Id {roll_id} already exists.")

            record = EmployeeData(roll_id=roll_id, name=name, phone=phone, major=major)
            session.add(record)
            session.commit()
            session.close()
            result = {'roll_id': roll_id, 'name': name, 'phone': phone, 'major': major}
            return result

    @wamp.register('com.test.get', check_types=True)
    async def get_data(self, roll_id: int):
        with sessionLocal() as session:
            result = self.query(roll_id, session)
            if result is None:
                result = {'msg': f" There is no student with roll ID {roll_id} ."}
            else:
                result = {'name': result.name, 'phone': result.phone, 'major': result.major}
            return result

    @wamp.register('com.test.update', check_types=True)
    async def update_user(self, roll_id: int, data: dict = None):

        try:
            tests = Schema(**data, roll_id=roll_id)
        except ValidationError as ex:
            raise ApplicationError("validation error", f"{ex.json()}")
        user = tests.dict(exclude_none=True)
        name = user.get("name")
        phone = user.get("phone")
        major = user.get("major")
        if name is not None and not self.validate_name(name):
            raise ApplicationError("validation error", f"Name '{user.get('name')}' is in invalid format")
        if phone is not None and not self.validate_number(phone):
            raise ApplicationError("validation error", f"Phone '{user.get('phone')}' is in invalid format")
        with sessionLocal() as session:
            result = self.query(roll_id, session)
        if result is None:
            raise ApplicationError("validation error", f" Student with this roll ID {roll_id} does not exists.")
        update_query = update(EmployeeData).values(**user).where(EmployeeData.roll_id == roll_id)
        session.execute(update_query)
        session.commit()
        return Schema.from_orm(result).dict()

    @wamp.register('com.test.delete', check_types=True)
    async def delete_user(self, roll_id: int):
        delete_query = select(EmployeeData).where(EmployeeData.roll_id == roll_id)
        with sessionLocal() as session:
            result = session.execute(delete_query)
            user = result.scalar()
            if user is None:
                raise ApplicationError("validation error", f'Student with this roll ID {roll_id} does not exists.')
            session.delete(user)
            session.commit()
