from tinydb import TinyDB

class CCTV_DB:
    def __init__(self) -> None:
        self.cctv_db = TinyDB('cctv_db.json')

    def save_CCTV(self, cctv):
        self.cctv_db.insert(cctv)

    def get_CCTV_List(self):
        return self.cctv_db.all()

    def delete_CCTV(self, id):
        try:
            self.cctv_db.remove(doc_ids=[int(id)])
        except:
            return "Error deleting the camera"

