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
        'picture' : self.picture
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
class CategoryList(Base):
    __tablename__ = 'list'
   
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
class Items(Base):
    __tablename__ = 'items'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    list_id = Column(Integer, ForeignKey('list.id'))
    list = relationship(CategoryList)
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
        'user_id' : self.user_id
        }
 

engine = create_engine('sqlite:///Catalog.db')
Base.metadata.create_all(engine)