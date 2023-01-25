from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


if __name__=='__main__':
    uvicorn.run('main:app', reload=True)




def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# MENU
@app.post("/api/v1/menus", response_model=schemas.Menu, status_code=201)
def create_menu(menu: schemas.MenuCreate, db: Session = Depends(get_db)):
    db_menu = crud.get_menu(db=db)
    if db_menu:
        raise HTTPException(status_code=404, detail="menu already exists")
    else:
        return crud.create_menu(db=db, menu=menu)


@app.get("/api/v1/menus", response_model=list[schemas.Menu],status_code=200)
def read_menu(db: Session = Depends(get_db)):
    menu = crud.get_menu(db=db)
    return menu


@app.get("/api/v1/menus/{menu_id}", response_model=schemas.Menu, status_code=200)
def read_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_id(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return db_menu


@app.delete("/api/v1/menus/{menu_id}", status_code=200)
def delete_menu(menu_id: str, db: Session = Depends(get_db)):
    db_menu = crud.delete_menu(db=db, menu_id=menu_id)
    if db_menu is None:
        raise HTTPException(status_code=404, detail="menu not found")
    return {"status": True, "message": "The menu has been deleted"}


@app.patch("/api/v1/menus/{menu_id}", response_model=schemas.Menu,status_code=200)
def update_menu(menu_id: str, menu: schemas.MenuUpdate, db: Session = Depends(get_db)):
    db_menu = crud.get_menu_id(db=db, menu_id=menu_id)
    if db_menu:
        db_menu.title = menu.title
        db_menu.description = menu.description
        return crud.update_menu(db=db, menu_id=menu_id)
    else:
        raise HTTPException(status_code=404, detail="menu not found")


# SUBMENU

@app.post("/api/v1/menus/{menu_id}/submenus", response_model=schemas.SubMenu, status_code=201)
def create_submenu(menu_id: str, submenu: schemas.SubMenuCreate, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu(db=db)
    if db_submenu:
        raise HTTPException(status_code=404, detail="submenu already exists")
    else:
        return crud.create_submenu(db=db, submenu=submenu, menu_id=menu_id)


@app.get("/api/v1/menus/{menu_id}/submenus", response_model=list[schemas.SubMenu])
def read_submenu(db: Session = Depends(get_db)):
    submenu = crud.get_submenu(db=db)
    return submenu


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}", status_code=200, response_model=schemas.SubMenu)
def read_submenu(submenu_id: str, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_id(db=db, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return db_submenu


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}", response_model=schemas.SubMenu)
def update_submenu(submenu_id: str, submenu: schemas.SubMenuUpdate, db: Session = Depends(get_db)):
    db_submenu = crud.get_submenu_id(db=db, submenu_id=submenu_id)
    if db_submenu:
        db_submenu.title = submenu.title
        db_submenu.description = submenu.description
        return crud.update_submenu(db=db, submenu_id=submenu_id)
    else:
        raise HTTPException(status_code=404, detail="submenu not found")


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    db_submenu = crud.delete_submenu(db=db, menu_id=menu_id, submenu_id=submenu_id)
    if db_submenu is None:
        raise HTTPException(status_code=404, detail="submenu not found")
    return {"status": True, "message": "The submenu has been deleted"}


# DISH


@app.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=schemas.Dish, status_code=201)
def create_dish(menu_id: str, submenu_id: str, dish: schemas.DishCreate, db: Session = Depends(get_db)):
    db_dish = crud.get_dish_id(db=db, dish_id=dish.id)
    if db_dish:
        raise HTTPException(status_code=404, detail="dish already exists")
    else:
        return crud.create_dish(db=db, dish=dish, menu_id=menu_id, submenu_id=submenu_id)


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes", response_model=list[schemas.Dish])
def read_dish(db: Session = Depends(get_db)):
    dish = crud.get_dish(db=db)
    return dish


@app.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def read_dish(dish_id: str, db: Session = Depends(get_db)):
    db_dish = crud.get_dish_id(db=db, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return db_dish


@app.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}", response_model=schemas.Dish)
def update_dish(dish_id: str, dish: schemas.DishUpdate, db: Session = Depends(get_db)):
    db_dish = crud.get_dish_id(db=db, dish_id=dish_id)
    if db_dish:
        db_dish.title = dish.title
        db_dish.description = dish.description
        db_dish.price = dish.price
        return crud.update_dish(db=db, dish_id=dish_id)
    else:
        raise HTTPException(status_code=404, detail="dish not found")


@app.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish(menu_id: str, submenu_id: str, dish_id: str, db: Session = Depends(get_db)):
    db_dish = crud.delete_dish(db=db, menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if db_dish is None:
        raise HTTPException(status_code=404, detail="dish not found")
    return {"status": True, "message": "The dish has been deleted"}
