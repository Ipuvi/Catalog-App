import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

#Class to store user details...
class User(Base):
    """docstring for User"""
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        #Returns Object data in easily serializable form...
        return {
        'id' : self.id,
        'name' : self.name,
        'email' : self.email,
        'picture' : self.picture,
        }


#Class Categories...
class Category(Base):
    """docstring for Categories"""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        #Returns Object data in easily serialiazable form...
        return {
        'name' : self.name,
        'id' : self.id,
        'user_id' : self.user_id
        }


# Restaurant Class ( Category 1)..... 
class Restaurant(Base):
    __tablename__ = 'restaurant'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    category = relationship(Category)

    @property
    def serialize(self):
        #Returns Object data in easily serialiazable form...
        return {
        'name' : self.name,
        'id' : self.id,
        'user_id' : self.user_id,
        'category_id' : self.category_id
        }

# Further sub category for Restaurant class...
class MenuItem(Base):
    __tablename__ = 'menu_item'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant) 
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        #Returns Object data in easily serialiazable form...
        return {
        'name' : self.name,
        'description' : self.description,
        'id' : self.id,
        'price' : self.price,
        'course' : self.course,
        'user_id' : self.user_id,
        }
 
# Hotel Class ( Category 2 ).....
class Hotel(Base):
    __tablename__ = 'hotel'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    category = relationship(Category)

    @property
    def serialize(self):
        #Returns Object data in easily serialiazable form...
        return {
        'name' : self.name,
        'id' : self.id,
        'user_id' : self.user_id,
        'category_id' : self.category_id
        }

#Further sub category for Hotel Class...
class HotelDetails(Base):
    """docstring for HotelList"""
    __tablename__ = 'hoteldetails'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    price = Column(String(8))
    room_type = Column(String(250))
    hotel_id = Column(Integer, ForeignKey('hotel.id'))
    hotel = relationship(Hotel)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        #Returns Object data in easily serialiazable form...
        return {
        'name' : self.name,
        'description' : self.description,
        'id' : self.id,
        'price' : self.price,
        'room_type' : self.room_type,
        'hotel_id' : self.hotel_id,
        'user_id' : self.user_id
        }
 

#Destination Class ( Category 3 ).....
class Destination(Base):
    """docstring for Destinations"""
    __tablename__ = 'destination' 

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user =relationship(User)

    @property
    def serialize(self):
        #Return Object data in easily serialiazable form...
        return {
        'name' : self.name,
        'id' : self.id,
        'user_id' : self.user_id,
        'category_id' : self.category_id
        }
        

#Further sub category for School Class...
class DestinationDetails(Base):
    """docstring for SchoolDetails"""
    __tablename__ = 'destinationdetails'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    address = Column(String(250))
    destination_id = Column(Integer, ForeignKey('destination.id'))
    destination = relationship(Destination)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)
    
    @property
    def serialize(self):
        #Returns Object data in easily serialiazable form...
        return {
        'name' : self.name,
        'id' : self.id,
        'description' : self.description,
        'address' : self.address,
        'destination_id' : self.school_id,
        'user_id' : self.user_id
        }
    

engine = create_engine('sqlite:///Catalog.db')
Base.metadata.create_all(engine)