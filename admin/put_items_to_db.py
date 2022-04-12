from data.products import Products


def add_to_bd(title, price, type_item, image_path, db_session):
    products = Products(
        title=title,
        price=price,
        type=type_item,
        image_path=image_path
    )
    db_session.add(products)
    db_session.commit()


def main_add_to_bd(db_session):
    add_to_bd("LOOTUS / Косуха", 4000, "woman", "lootus.jpg", db_session)
    add_to_bd("SRSShop / Куртка", 7000, "woman", "srsshop.jpg", db_session)
    add_to_bd("Avrilla / Джинсы", 2500, "woman", "avrilla.jpg", db_session)
    add_to_bd("Avrilla / Джинсы", 2000, "woman", "avrilla2.jpg", db_session)
    add_to_bd("Corner_more / Юбка", 2400, "woman", "corner_more.jpg", db_session)
    add_to_bd("MARYMARY / Футболка", 2700, "woman", "marymary.jpg", db_session)
    add_to_bd("Serenada / Туника", 2600, "woman", "serenada.jpg", db_session)
    add_to_bd("ART FAMILY / Водолазка", 1200, "woman", "artfamily.jpg", db_session)
    add_to_bd("Nikolom / Пальто", 8000, "man", "nikolom.jpg", db_session)
    add_to_bd("VipDressCode / Пальто", 10000, "man", "VipDressCode.jpg", db_session)
    add_to_bd("BULANTI / Рубашка", 3000, "man", "BULANTI.jpg", db_session)
    add_to_bd("Wrangler / Рубашка", 4300, "man", "Wrangler.jpg", db_session)
    add_to_bd("TOM TAILOR / Джинсы", 5900, "man", "TOM TAILOR.jpg", db_session)
    add_to_bd("IMHO / Шорты", 1500, "man", "imho.jpg", db_session)
    add_to_bd("BASEWEAR / Костюм", 5700, "man", "basewear.jpg", db_session)
    add_to_bd("Бест Трикотаж / Брюки", 3300, "man", "best.jpg", db_session)
    add_to_bd("Sherysheff / Куртка", 4400, "kids", "sherysheff2.jpg", db_session)
    add_to_bd("LELUkids / Платье", 6900, "kids", "lelukids.jpg", db_session)
    add_to_bd("PlayToday / Джинсы", 2200, "kids", "playToday.jpg", db_session)
    add_to_bd("Hohloon / Куртка", 3000, "kids", "hohloon.jpg", db_session)
    add_to_bd("Orso Bianco / Жилетка", 2100, "kids", "orsobianco.jpg", db_session)
    add_to_bd("Sherysheff / Комбинезон", 5800, "kids", "sherysheff.jpg", db_session)
    add_to_bd("CAROC / Кроссовки", 3800, "kids", "caroc.jpg", db_session)
    add_to_bd("PlayToday / Футболка", 2000, "kids", "playtoday2.png", db_session)
