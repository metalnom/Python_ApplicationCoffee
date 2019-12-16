from dao.product_dao import ProductDao
from dao.sale_dao import SaleDao


if __name__ == "__main__":
    Sdao = SaleDao()
    Sdao.select_item()
    # Sdao.insert_item('A003', 4000, 200, 13)
    # Sdao.delete_item(6)
    # Sdao.update_item(code='A002', price=3800, saleCnt=150, marginRate=15, no=5)
    # Sdao.select_item(5)

    Pdao = ProductDao()
    Pdao.select_item()
    # Pdao.insert_item('A005', '마키아또')
    # Pdao.delete_item('A005')
    # Pdao.update_item('A002', '카푸치노2')
    # Pdao.select_item('A002')