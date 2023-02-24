from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from os import environ
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.internet.defer import inlineCallbacks


Base = declarative_base()

class MyModel(Base):

    __tablename__ = 'data'

    roll_id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    major = Column(Integer)
class MyComponent(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        engine = create_engine('sqlite:///person.db')
        Base.metadata.create_all(engine)

        Session = sessionmaker(bind=engine)
        session = Session()
        print("Procedure registered")

        def save_record(roll_id, name, phone, major):
            record = MyModel(roll_id=roll_id, name=name, phone=phone, major=major)
            session.add(record)
            session.commit()
            result = {'status': 'success', 'data': {'roll_id': roll_id, 'name': name, 'phone': phone, 'major': major}}
            return (result)

        yield self.register(save_record, 'com.test.create')

        def get_data(roll_id):
            data = session.query(MyModel).filter_by(roll_id=roll_id).first()
            if data:
                result = {'status': 'success',
                         'data': {'name': data.name, 'phone': data.phone, 'major': data.major}}
            else:
                result = {'status': 'error', 'message': f"No student with roll ID {roll_id} found."}
            return (result)

        yield self.register(get_data, 'com.test.get')




if __name__ == '__main__':
    url = environ.get("wick", "ws://localhost:8080/ws")
    realm = "realm1"
    runner = ApplicationRunner(url, realm)
    runner.run(MyComponent)
