import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class OrdersItems(SqlAlchemyBase):
    __tablename__ = 'orders_items'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_product = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"), nullable=False)
    id_client = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=False)