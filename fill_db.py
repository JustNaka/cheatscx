from app import Category, Products, Users, db

category = [
    Category(id="1", name="GTA V", image_path="static/imgs/gta.png", cat_name="gta", starting_price="10", type="cat"), 
    Category(id="2", name="APEX", image_path="static/imgs/apex.png", cat_name="apex", starting_price="10", type="cat"),
    Category(id="3", name="TARKOV", image_path="static/imgs/tarkov.png", cat_name="tarkov", starting_price="10", type="cat"),
    Category(id="4", name="DAYZ", image_path="static/imgs/dayz.png", cat_name="dayz", starting_price="10", type="cat"),
    Category(id="5", name="DEAD BY DAYLIGHT", image_path="static/imgs/dead.png", cat_name="dead", starting_price="10", type="cat"),
    Category(id="6", name="VALORANT", image_path="static/imgs/valorant.png", cat_name="valorant", starting_price="10", type="cat"),
    Category(id="7", name="FIVEM", image_path="static/imgs/fivem.png", cat_name="fivem", starting_price="10", type="cat"),
    Category(id="8", name="CYCLE", image_path="static/imgs/cycle.png", cat_name="cycle", starting_price="10", type="cat"),
]

products = [
    Products(id="1", cat_name="gta", name="GTA V_1", image_path="/static/imgs/gta.png", type="product", description="Grazie a questo cheat potrai cheatare nel tuo gioco preferito!", status="Undetected", screens={"1": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg", "2": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg"}, requirements={"1": ["CPU:", "Intel only!"], "2": ["OS:", "Windows 10&11"], "3": ["Supported Anti-Cheat(s):", "BattlEye Anti-Cheat"]}, features={"AIM ASSIST": ["banane", "pesce"],"MISC": ["noci", "mandorle"]}),
    Products(id="2", cat_name="gta", name="GTA V_2", image_path="/static/imgs/gta.png", type="product", description="Grazie a questo cheat potrai cheatare nel tuo gioco preferito!", status="Undetected", screens={"1": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg", "2": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg"}, requirements={"1": ["CPU:", "Intel only!"], "2": ["OS:", "Windows 10&11"], "3": ["Supported Anti-Cheat(s):", "BattlEye Anti-Cheat"]}, features={"AIM ASSIST": ["banane", "pesce"],"MISC": ["noci", "mandorle"]}), 
    Products(id="3", cat_name="gta", name="GTA V_3", image_path="/static/imgs/gta.png", type="product", description="Grazie a questo cheat potrai cheatare nel tuo gioco preferito!", status="Undetected", screens={"1": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg", "2": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg"}, requirements={"1": ["CPU:", "Intel only!"], "2": ["OS:", "Windows 10&11"], "3": ["Supported Anti-Cheat(s):", "BattlEye Anti-Cheat"]}, features={"AIM ASSIST": ["banane", "pesce"],"MISC": ["noci", "mandorle"]}), 
    Products(id="4", cat_name="gta", name="GTA V_4", image_path="/static/imgs/gta.png", type="product", description="Grazie a questo cheat potrai cheatare nel tuo gioco preferito!", status="Undetected", screens={"1": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg", "2": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg"}, requirements={"1": ["CPU:", "Intel only!"], "2": ["OS:", "Windows 10&11"], "3": ["Supported Anti-Cheat(s):", "BattlEye Anti-Cheat"]}, features={"AIM ASSIST": ["banane", "pesce"],"MISC": ["noci", "mandorle"]}), 
    Products(id="5", cat_name="apex", name="DAYZ_1", image_path="/static/imgs/apex.png", type="product", description="Grazie a questo cheat potrai cheatare nel tuo gioco preferito!", status="Undetected", screens={"1": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg", "2": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg"}, requirements={"1": ["CPU:", "Intel only!"], "2": ["OS:", "Windows 10&11"], "3": ["Supported Anti-Cheat(s):", "BattlEye Anti-Cheat"]}, features={"AIM ASSIST": ["banane", "pesce"],"MISC": ["noci", "mandorle"]}),
    Products(id="6", cat_name="apex", name="DAYZ_2", image_path="/static/imgs/apex.png", type="product", description="Grazie a questo cheat potrai cheatare nel tuo gioco preferito!", status="Undetected", screens={"1": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg", "2": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg"}, requirements={"1": ["CPU:", "Intel only!"], "2": ["OS:", "Windows 10&11"], "3": ["Supported Anti-Cheat(s):", "BattlEye Anti-Cheat"]}, features={"AIM ASSIST": ["banane", "pesce"],"MISC": ["noci", "mandorle"]}),
    Products(id="7", cat_name="apex", name="DAYZ_3", image_path="/static/imgs/apex.png", type="product", description="Grazie a questo cheat potrai cheatare nel tuo gioco preferito!", status="Undetected", screens={"1": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg", "2": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg"}, requirements={"1": ["CPU:", "Intel only!"], "2": ["OS:", "Windows 10&11"], "3": ["Supported Anti-Cheat(s):", "BattlEye Anti-Cheat"]}, features={"AIM ASSIST": ["banane", "pesce"],"MISC": ["noci", "mandorle"]}),
    Products(id="8", cat_name="apex", name="DAYZ_4", image_path="/static/imgs/apex.png", type="product", description="Grazie a questo cheat potrai cheatare nel tuo gioco preferito!", status="Undetected", screens={"1": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg", "2": "https://ring-1.io/uploads/apex-1-62d9fa4e0fcd2025956931.jpg"}, requirements={"1": ["CPU:", "Intel only!"], "2": ["OS:", "Windows 10&11"], "3": ["Supported Anti-Cheat(s):", "BattlEye Anti-Cheat"]}, features={"AIM ASSIST": ["banane", "pesce"],"MISC": ["noci", "mandorle"]})
]


users = [
    Users(id="1", username="test", password="suca", is_auth=False)
]

for i in products:
    db.session.add(i)
    db.session.commit()

