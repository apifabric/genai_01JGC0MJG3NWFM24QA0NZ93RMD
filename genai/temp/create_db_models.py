# using resolved_model self.resolved_model FIXME
# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from datetime import date   
from datetime import datetime
from typing import List


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py


from sqlalchemy.dialects.sqlite import *

class Owner(Base):
    """description: This table represents dog owners who use the dog walking services."""
    __tablename__ = 'owner'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_number = Column(String, nullable=True)
    email = Column(String, nullable=True)

class Dog(Base):
    """description: This table represents the dogs being walked by the business."""
    __tablename__ = 'dog'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    breed = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)

class Walker(Base):
    """description: This table represents the employees who walk the dogs."""
    __tablename__ = 'walker'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_number = Column(String, nullable=True)
    email = Column(String, nullable=True)

class Walk(Base):
    """description: This table logs each walk taken with details about which dog, which walker, and when."""
    __tablename__ = 'walk'
    id = Column(Integer, primary_key=True)
    dog_id = Column(Integer, ForeignKey('dog.id'), nullable=False)
    walker_id = Column(Integer, ForeignKey('walker.id'), nullable=False)
    date_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)

class Payment(Base):
    """description: This table records payment information from owners for the dog walking services."""
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)

class Service(Base):
    """description: This table defines the types of services offered by the dog walking business."""
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    base_rate = Column(Numeric(10, 2), nullable=False)

class DogServiceAssociation(Base):
    """description: This table is a junction table associating each dog with its services."""
    __tablename__ = 'dog_service_association'
    id = Column(Integer, primary_key=True)
    dog_id = Column(Integer, ForeignKey('dog.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)

class Invoice(Base):
    """description: This table generates invoices for owners based on services and payments."""
    __tablename__ = 'invoice'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    date_issued = Column(Date, nullable=False)

class InvoiceItem(Base):
    """description: This table contains each item on an invoice, specifying services and charges."""
    __tablename__ = 'invoice_item'
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoice.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

class Schedule(Base):
    """description: This table schedules the availability of walkers for dog walking."""
    __tablename__ = 'schedule'
    id = Column(Integer, primary_key=True)
    walker_id = Column(Integer, ForeignKey('walker.id'), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

class WalkerEvaluation(Base):
    """description: This table records evaluations of walkers based on their performance."""
    __tablename__ = 'walker_evaluation'
    id = Column(Integer, primary_key=True)
    walker_id = Column(Integer, ForeignKey('walker.id'), nullable=False)
    evaluation_date = Column(Date, nullable=False)
    performance_score = Column(Integer, nullable=False)
    comments = Column(String, nullable=True)

class ClientFeedback(Base):
    """description: This table captures feedback from clients regarding the service provided."""
    __tablename__ = 'client_feedback'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owner.id'), nullable=False)
    walk_id = Column(Integer, ForeignKey('walk.id'), nullable=False)
    feedback_date = Column(Date, nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(String, nullable=True)


# end of model classes


try:
    
    
    # ALS/GenAI: Create an SQLite database
    import os
    mgr_db_loc = True
    if mgr_db_loc:
        print(f'creating in manager: sqlite:///system/genai/temp/create_db_models.sqlite')
        engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    else:
        current_file_path = os.path.dirname(__file__)
        print(f'creating at current_file_path: {current_file_path}')
        engine = create_engine(f'sqlite:///{current_file_path}/create_db_models.sqlite')
    Base.metadata.create_all(engine)
    
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # ALS/GenAI: Prepare for sample data
    
    
    session.commit()
    walker_1 = Walker(name="John Doe", contact_number="1234567890", email="johndoe@example.com")
    walker_2 = Walker(name="Jane Smith", contact_number="0987654321", email="janesmith@example.com")
    walker_3 = Walker(name="Jake Fox", contact_number="1928374650", email="jakefox@example.com")
    walker_4 = Walker(name="Lara Croft", contact_number="5647382910", email="laracroft@example.com")
    owner_1 = Owner(name="Alice Johnson", contact_number="1122334455", email="alice@example.com")
    owner_2 = Owner(name="Bob Brown", contact_number="2233445566", email="bob@example.com")
    owner_3 = Owner(name="Charlie Davis", contact_number="3344556677", email="charlie@example.com")
    owner_4 = Owner(name="Diana Prince", contact_number="4455667788", email="diana@example.com")
    dog_1 = Dog(name="Rex", breed="Labrador", owner_id=1)
    dog_2 = Dog(name="Bella", breed="Beagle", owner_id=2)
    dog_3 = Dog(name="Max", breed="German Shepherd", owner_id=3)
    dog_4 = Dog(name="Luna", breed="Golden Retriever", owner_id=4)
    service_1 = Service(name="Regular Walk", description="30-minute walk", base_rate=10.00)
    service_2 = Service(name="Extended Walk", description="60-minute walk", base_rate=18.00)
    service_3 = Service(name="Training Session", description="30-minute training", base_rate=15.00)
    service_4 = Service(name="Overnight Stay", description="24-hour stay", base_rate=50.00)
    payment_1 = Payment(owner_id=1, amount=100.00, payment_date=date(2023, 10, 1))
    payment_2 = Payment(owner_id=2, amount=75.00, payment_date=date(2023, 10, 2))
    payment_3 = Payment(owner_id=3, amount=150.00, payment_date=date(2023, 10, 3))
    payment_4 = Payment(owner_id=4, amount=200.00, payment_date=date(2023, 10, 4))
    walk_1 = Walk(dog_id=1, walker_id=1, date_time=datetime(2023, 10, 5, 9, 30), duration=30)
    walk_2 = Walk(dog_id=2, walker_id=2, date_time=datetime(2023, 10, 5, 10, 30), duration=60)
    walk_3 = Walk(dog_id=3, walker_id=3, date_time=datetime(2023, 10, 5, 11, 30), duration=30)
    walk_4 = Walk(dog_id=4, walker_id=4, date_time=datetime(2023, 10, 5, 12, 30), duration=60)
    invoice_1 = Invoice(owner_id=1, total_amount=100.00, date_issued=date(2023, 10, 1))
    invoice_2 = Invoice(owner_id=2, total_amount=50.00, date_issued=date(2023, 10, 2))
    invoice_3 = Invoice(owner_id=3, total_amount=150.00, date_issued=date(2023, 10, 3))
    invoice_4 = Invoice(owner_id=4, total_amount=200.00, date_issued=date(2023, 10, 4))
    
    
    
    session.add_all([walker_1, walker_2, walker_3, walker_4, owner_1, owner_2, owner_3, owner_4, dog_1, dog_2, dog_3, dog_4, service_1, service_2, service_3, service_4, payment_1, payment_2, payment_3, payment_4, walk_1, walk_2, walk_3, walk_4, invoice_1, invoice_2, invoice_3, invoice_4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')
