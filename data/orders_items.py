import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class OrdersItems(SqlAlchemyBase):
    __tablename__ = 'orders_items'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_product = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"), nullable=False)
    id_order = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("orders.id"), nullable=False)