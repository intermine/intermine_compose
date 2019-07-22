from flask_login import LoginManager
from ..models.users import User
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.filter_by(id=user_id).first()
    return None
