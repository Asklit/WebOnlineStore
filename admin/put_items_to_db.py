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
    add_to_bd("Salendo / Куртка женская демисезонная", 4000, "woman", "salendo.png", db_session)
    add_to_bd("My WEAR / Куртка женская", 7000, "woman", "mywear.png", db_session)
    add_to_bd("Avrilla / Джинсы клеш", 2500, "woman", "avrilla.png", db_session)
    add_to_bd("Salendo / Куртка женская демисезонная", 4000, "woman", "salendo.png", db_session)
    add_to_bd("My WEAR / Куртка женская", 7000, "woman", "mywear.png", db_session)
    add_to_bd("Avrilla / Джинсы клеш", 2500, "woman", "avrilla.png", db_session)
    add_to_bd("Avrilla / Джинсы женские", 2000, "woman", "avrilla2.png", db_session)
    add_to_bd("corner_more / Юбка плиссированная", 2400, "woman", "corner_more.png", db_session)
    add_to_bd("corner_more / Чёрная мини юбка с разрезом", 2700, "woman", "corner_more2.png", db_session)
    add_to_bd("Nikolom / Пальто", 8000, "man", "nikolom.png", db_session)
    add_to_bd("VipDressCode / Пальто", 10000, "man", "VipDressCode.png", db_session)
    add_to_bd("BULANTI / Рубашка мужская в клетку", 3000, "man", "BULANTI.png", db_session)
    add_to_bd("Wrangler / Джинсы ARIZONA", 4300, "man", "Wrangle.png", db_session)
    add_to_bd("TOM TAILOR / Джинсы", 5900, "man", "TOM TAILOR.png", db_session)
