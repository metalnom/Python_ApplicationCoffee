from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao


if __name__ == "__main__":

    Pdao = ProductDao()
    Pdao.select_item()

    Sdao = SaleDao()
    Sdao.select_item()