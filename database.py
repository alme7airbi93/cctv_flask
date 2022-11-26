from tinydb import TinyDB, where, Query


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


class SETTINGS_DB:
    def __init__(self) -> None:
        self.settings_db = TinyDB('settings_db.json')

    def save_settings(self, settings):
        self.settings_db.insert(settings)

    def update_settings(self, settings: dict):
        self.settings_db.truncate()
        self.save_settings(settings)

    def get_settings_Dict(self):
        list = self.settings_db.all()
        settings = {}
        for item in list:
            for key, val in item.items():
                settings[key] = val
        return settings

    def delete_SETTINGS(self, id):
        try:
            self.settings_db.remove(doc_ids=[int(id)])
        except:
            return "Error deleting the camera"
