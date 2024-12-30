# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 30, 2024 14:49:30
# Database: sqlite:////tmp/tmp.QIuWIZzlRo-01JGC0MJG3NWFM24QA0NZ93RMD/Dog_Walker_System/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *

Base = SAFRSBaseX



class Owner(Base):  # type: ignore
    """
    description: This table represents dog owners who use the dog walking services.
    """
    __tablename__ = 'owner'
    _s_collection_name = 'Owner'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_number = Column(String)
    email = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    DogList : Mapped[List["Dog"]] = relationship(back_populates="owner")
    InvoiceList : Mapped[List["Invoice"]] = relationship(back_populates="owner")
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="owner")
    ClientFeedbackList : Mapped[List["ClientFeedback"]] = relationship(back_populates="owner")



class Service(Base):  # type: ignore
    """
    description: This table defines the types of services offered by the dog walking business.
    """
    __tablename__ = 'service'
    _s_collection_name = 'Service'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    base_rate = Column(Numeric(10, 2), nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    DogServiceAssociationList : Mapped[List["DogServiceAssociation"]] = relationship(back_populates="service")
    InvoiceItemList : Mapped[List["InvoiceItem"]] = relationship(back_populates="service")



class Walker(Base):  # type: ignore
    """
    description: This table represents the employees who walk the dogs.
    """
    __tablename__ = 'walker'
    _s_collection_name = 'Walker'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    contact_number = Column(String)
    email = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    ScheduleList : Mapped[List["Schedule"]] = relationship(back_populates="walker")
    WalkerEvaluationList : Mapped[List["WalkerEvaluation"]] = relationship(back_populates="walker")
    WalkList : Mapped[List["Walk"]] = relationship(back_populates="walker")



class Dog(Base):  # type: ignore
    """
    description: This table represents the dogs being walked by the business.
    """
    __tablename__ = 'dog'
    _s_collection_name = 'Dog'  # type: ignore

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    breed = Column(String)
    owner_id = Column(ForeignKey('owner.id'), nullable=False)

    # parent relationships (access parent)
    owner : Mapped["Owner"] = relationship(back_populates=("DogList"))

    # child relationships (access children)
    DogServiceAssociationList : Mapped[List["DogServiceAssociation"]] = relationship(back_populates="dog")
    WalkList : Mapped[List["Walk"]] = relationship(back_populates="dog")



class Invoice(Base):  # type: ignore
    """
    description: This table generates invoices for owners based on services and payments.
    """
    __tablename__ = 'invoice'
    _s_collection_name = 'Invoice'  # type: ignore

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('owner.id'), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    date_issued = Column(Date, nullable=False)

    # parent relationships (access parent)
    owner : Mapped["Owner"] = relationship(back_populates=("InvoiceList"))

    # child relationships (access children)
    InvoiceItemList : Mapped[List["InvoiceItem"]] = relationship(back_populates="invoice")



class Payment(Base):  # type: ignore
    """
    description: This table records payment information from owners for the dog walking services.
    """
    __tablename__ = 'payment'
    _s_collection_name = 'Payment'  # type: ignore

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('owner.id'), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    payment_date = Column(Date, nullable=False)

    # parent relationships (access parent)
    owner : Mapped["Owner"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)



class Schedule(Base):  # type: ignore
    """
    description: This table schedules the availability of walkers for dog walking.
    """
    __tablename__ = 'schedule'
    _s_collection_name = 'Schedule'  # type: ignore

    id = Column(Integer, primary_key=True)
    walker_id = Column(ForeignKey('walker.id'), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    # parent relationships (access parent)
    walker : Mapped["Walker"] = relationship(back_populates=("ScheduleList"))

    # child relationships (access children)



class WalkerEvaluation(Base):  # type: ignore
    """
    description: This table records evaluations of walkers based on their performance.
    """
    __tablename__ = 'walker_evaluation'
    _s_collection_name = 'WalkerEvaluation'  # type: ignore

    id = Column(Integer, primary_key=True)
    walker_id = Column(ForeignKey('walker.id'), nullable=False)
    evaluation_date = Column(Date, nullable=False)
    performance_score = Column(Integer, nullable=False)
    comments = Column(String)

    # parent relationships (access parent)
    walker : Mapped["Walker"] = relationship(back_populates=("WalkerEvaluationList"))

    # child relationships (access children)



class DogServiceAssociation(Base):  # type: ignore
    """
    description: This table is a junction table associating each dog with its services.
    """
    __tablename__ = 'dog_service_association'
    _s_collection_name = 'DogServiceAssociation'  # type: ignore

    id = Column(Integer, primary_key=True)
    dog_id = Column(ForeignKey('dog.id'), nullable=False)
    service_id = Column(ForeignKey('service.id'), nullable=False)

    # parent relationships (access parent)
    dog : Mapped["Dog"] = relationship(back_populates=("DogServiceAssociationList"))
    service : Mapped["Service"] = relationship(back_populates=("DogServiceAssociationList"))

    # child relationships (access children)



class InvoiceItem(Base):  # type: ignore
    """
    description: This table contains each item on an invoice, specifying services and charges.
    """
    __tablename__ = 'invoice_item'
    _s_collection_name = 'InvoiceItem'  # type: ignore

    id = Column(Integer, primary_key=True)
    invoice_id = Column(ForeignKey('invoice.id'), nullable=False)
    service_id = Column(ForeignKey('service.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    # parent relationships (access parent)
    invoice : Mapped["Invoice"] = relationship(back_populates=("InvoiceItemList"))
    service : Mapped["Service"] = relationship(back_populates=("InvoiceItemList"))

    # child relationships (access children)



class Walk(Base):  # type: ignore
    """
    description: This table logs each walk taken with details about which dog, which walker, and when.
    """
    __tablename__ = 'walk'
    _s_collection_name = 'Walk'  # type: ignore

    id = Column(Integer, primary_key=True)
    dog_id = Column(ForeignKey('dog.id'), nullable=False)
    walker_id = Column(ForeignKey('walker.id'), nullable=False)
    date_time = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)

    # parent relationships (access parent)
    dog : Mapped["Dog"] = relationship(back_populates=("WalkList"))
    walker : Mapped["Walker"] = relationship(back_populates=("WalkList"))

    # child relationships (access children)
    ClientFeedbackList : Mapped[List["ClientFeedback"]] = relationship(back_populates="walk")



class ClientFeedback(Base):  # type: ignore
    """
    description: This table captures feedback from clients regarding the service provided.
    """
    __tablename__ = 'client_feedback'
    _s_collection_name = 'ClientFeedback'  # type: ignore

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('owner.id'), nullable=False)
    walk_id = Column(ForeignKey('walk.id'), nullable=False)
    feedback_date = Column(Date, nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(String)

    # parent relationships (access parent)
    owner : Mapped["Owner"] = relationship(back_populates=("ClientFeedbackList"))
    walk : Mapped["Walk"] = relationship(back_populates=("ClientFeedbackList"))

    # child relationships (access children)
