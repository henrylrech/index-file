from classes.entries.order_entry import OrderEntry
from classes.entries.product_entry import ProductEntry
from utility import parse

class Jewelry:
    def __init__(self, date, order_id, product_id, quantity, category_id, 
                 jewellery_type, brand_id, price, user_id, gender, box_colour, metal, gem):
        self.date = parse.to_str(date)
        self.order_id = parse.to_int(order_id)
        self.product_id = parse.to_int(product_id)
        self.quantity = parse.to_int(quantity)
        self.category_id = parse.to_float(category_id)
        self.jewellery_type = parse.to_str(jewellery_type)
        self.brand_id = parse.to_int(brand_id)
        self.price = parse.to_float(price)
        self.user_id = parse.to_int(user_id)
        self.gender = parse.to_str(gender)
        self.box_colour = parse.to_str(box_colour)
        self.metal = parse.to_str(metal)
        self.gem = parse.to_str(gem)

    def as_product_entry(self):
        return ProductEntry(self.product_id, self.jewellery_type, self.metal, self.gem)
    
    def as_order_entry(self):
        return OrderEntry(self.order_id, self.product_id, self.quantity, self.price, self.user_id)

