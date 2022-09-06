from app import Category, Products, db

category = [
    Category(id="1", name="GTA V", image_path="static/imgs/gta_thumbnail.png", cat_name="gta"), 
    Category(id="2", name="DAYZ", image_path="static/imgs/gta_thumbnail.png", cat_name="dayz"),
    Category(id="3", name="ARMA 3", image_path="static/imgs/gta_thumbnail.png", cat_name="arma"),
    Category(id="4", name="TABG", image_path="static/imgs/gta_thumbnail.png", cat_name="tabg")
]

products = [
    Products(id="1", cat_name="gta", name="GTA V_1", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="2", cat_name="gta", name="GTA V_2", image_path="static/imgs/gta_thumbnail.png"), 
    Products(id="3", cat_name="gta", name="GTA V_3", image_path="static/imgs/gta_thumbnail.png"), 
    Products(id="4", cat_name="gta", name="GTA V_4", image_path="static/imgs/gta_thumbnail.png"), 
    Products(id="5", cat_name="dayz", name="DAYZ_1", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="6", cat_name="dayz", name="DAYZ_2", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="7", cat_name="dayz", name="DAYZ_3", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="8", cat_name="dayz", name="DAYZ_4", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="9", cat_name="arma", name="ARMA 3_1", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="10", cat_name="arma", name="ARMA 3_2", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="11", cat_name="arma", name="ARMA 3_3", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="12", cat_name="arma", name="ARMA 3_4", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="13", cat_name="tabg", name="TABG_1", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="14", cat_name="tabg", name="TABG_2", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="15", cat_name="tabg", name="TABG_3", image_path="static/imgs/gta_thumbnail.png"),
    Products(id="16", cat_name="tabg", name="TABG_4", image_path="static/imgs/gta_thumbnail.png")
]

for i in products:
    db.session.add(i)
    db.session.commit()

