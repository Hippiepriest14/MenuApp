from sqlalchemy.orm import Session
import models
import schemas
import uuid

# MENU


def get_menu(db: Session):
    return db.query(models.Menu).all()


def create_menu(db: Session, menu: schemas.MenuCreate):
    db_menu = models.Menu(**menu.dict())
    db_menu.id = str(0)
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


def update_menu(db: Session, menu_id: str):
    db.commit()
    return get_menu_id(db=db, menu_id=menu_id)


def delete_menu(db: Session, menu_id: str):
    db_menu = get_menu_id(db, menu_id)
    if db_menu is None:
        return None
    else:
        db.delete(db_menu)
        db.commit()
        return True


def get_menu_id(db: Session, menu_id: str):
    return db.query(models.Menu).filter(models.Menu.id == menu_id).first()


# SUBMENU


def get_submenu(db: Session):
    return db.query(models.SubMenu).all()


def create_submenu(db: Session, submenu: schemas.SubMenuCreate, menu_id: str):
    db_submenu = models.SubMenu(**submenu.dict())
    db_submenu.menu_id = menu_id
    db_submenu.id = str(0)
    get_menu_id(db=db, menu_id=menu_id).submenus_count += 1
    db.add(db_submenu)
    db.commit()
    db.refresh(db_submenu)
    return db_submenu


def update_submenu(db: Session, submenu_id: str):
    db.commit()
    return get_submenu_id(db=db, submenu_id=submenu_id)


def delete_submenu(db: Session, menu_id: str, submenu_id: str):
    db_submenu = get_submenu_id(db, submenu_id)
    if db_submenu is None:
        return None
    else:
        db_menu = get_menu_id(db=db, menu_id=menu_id)
        db_menu.submenus_count -= 1
        db_menu.dishes_count -= db_submenu.dishes_count
        db.delete(db_submenu)
        db.commit()
        return True


def get_submenu_id(db: Session, submenu_id: str):
    return db.query(models.SubMenu).filter(models.SubMenu.id == submenu_id).first()

# DISH


def get_dish(db: Session):
    return db.query(models.Dish).all()


def create_dish(db: Session, dish: schemas.DishCreate, menu_id: str, submenu_id: str):
    db_dish = models.Dish(**dish.dict())
    db_dish.id = str(uuid.uuid1())
    db_dish.submenu_id = submenu_id
    get_menu_id(db=db, menu_id=menu_id).dishes_count += 1
    get_submenu_id(db=db, submenu_id=submenu_id).dishes_count += 1
    db.add(db_dish)
    db.commit()
    db.refresh(db_dish)
    return db_dish


def update_dish(db: Session, dish_id: str):
    db.commit()
    return get_dish_id(db=db, dish_id=dish_id)


def delete_dish(db: Session, menu_id: str, submenu_id: str, dish_id: str):
    db_dish = get_dish_id(db, dish_id)
    if db_dish is None:
        return None
    else:
        get_menu_id(db=db, menu_id=menu_id).dishes_count -= 1
        get_submenu_id(db=db, submenu_id=submenu_id).dishes_count -= 1
        db.delete(db_dish)
        db.commit()
        return True


def get_dish_id(db: Session, dish_id: str):
    return db.query(models.Dish).filter(models.Dish.id == dish_id).first()
