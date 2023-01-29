from pydantic import BaseModel

# MENU


class MenuBase(BaseModel):
    id: str | None = None
    title: str
    description: str


class MenuCreate(MenuBase):
    submenus_count: int = 0
    dishes_count: int = 0


class MenuUpdate(MenuBase):
    pass


class Menu(MenuBase):
    submenus_count: int
    dishes_count: int

    class Config:
        orm_mode = True

# SUBMENU


class SubMenuBase(BaseModel):
    id: str | None = None
    title: str
    description: str | None = None


class SubMenuCreate(SubMenuBase):
    dishes_count: int = 0


class SubMenuUpdate(SubMenuBase):
    pass


class SubMenu(SubMenuBase):
    dishes_count: int

    class Config:
        orm_mode = True


# DISH
class DishBase(BaseModel):
    id: str | None = None
    title: str
    description: str | None = None
    price: str | None = None


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class Dish(DishBase):

    class Config:
        orm_mode = True
