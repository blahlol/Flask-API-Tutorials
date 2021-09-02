from ma import ma
from models.item import ItemModel
from models.store import StoreModel

class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel
        load_only = ('store', ) # since both store and store_id will be same on dumping we remove store
        dump_only = ('id', )
        load_instance = True
        include_fk = True #during dump