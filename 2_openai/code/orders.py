from pydantic import BaseModel

class Order(BaseModel):
    customer_id: str
    item: str
    total_price: float
    status: str


def group_orders_by_customer_id(orders: list[Order]) -> dict:
    """注文をcustomer_idでグループ化し、customer_idをキー、注文のリストを値とする辞書を返す。"""

    customer_ids = {order.customer_id for order in orders}
    grouped = dict.fromkeys(customer_ids, [])
    for order in orders:
        grouped[order.customer_id].append(order)
    return grouped