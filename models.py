

from sqlalchemy import Boolean,Column, ForeignKey, Integer, String, select, func
from sqlalchemy.orm import relationship

from database import Base


class Menu(Base):
    __tablename__ = "menus"

    id = Column(String, primary_key=True,index=True)
    title = Column(String,index=True)
    description = Column(String,index=True)
    submenus_count = Column(Integer,index=True)
    dishes_count = Column(Integer,index=True)

    submenus = relationship("SubMenu",back_populates="menu", cascade="all")

class SubMenu(Base):
    __tablename__ = "submenus"

    id = Column(String, primary_key=True,index=True)
    title = Column(String,index=True)
    description = Column(String,index=True)
    menu_id = Column(String,ForeignKey("menus.id"))
    dishes_count = Column(Integer,index=True)

    menu = relationship("Menu",back_populates="submenus")
    dishes = relationship("Dish",back_populates="submenu",cascade="all")


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(String, index=True)
    submenu_id = Column(String, ForeignKey("submenus.id"))

    submenu = relationship("SubMenu", back_populates="dishes")

