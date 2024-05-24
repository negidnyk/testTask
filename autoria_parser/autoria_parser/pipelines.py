from .spiders.models import CarItem
from .spiders.database import session_factory


class AutoriaParserPipeline:

    async def process_item(self, item, spider):

        with session_factory() as session:
            print("Data to be store, URL", item['url'])
            car_item = CarItem(url=item['url'],
                               title=item['title'],
                               price=item['price'],
                               brand=item['brand'],
                               model=item['model'],
                               year=item['year'],
                               region=item['region'],
                               mileage=item['mileage'],
                               color=item['color'],
                               cabin_color=item['cabin_color'],
                               cabin_material=item['cabin_material'],
                               ad_creation_date=item['ad_creation_date'],
                               seller_contacts=item['seller_contacts'],
                               )
            session.add_all([car_item])
            # flush отправляет запрос в базу данных
            # После flush каждый из item получает первичный ключ id, который отдала БД
            session.flush()
            session.commit()
