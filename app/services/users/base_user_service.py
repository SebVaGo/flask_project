from app.models.client_tipe_model import ClientTypeModel
from app.models.password_model import PasswordModel
from app.models.user_model import UserModel


class BaseUserService:
    
    def __init__(self):
        self.user_model = UserModel
        self.password_model = PasswordModel
        self.client_type_model = ClientTypeModel
