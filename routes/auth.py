from flask import Blueprint
from controllers.auth import login

auth = Blueprint('auth', __name__)

auth.route('/login', methods=['POST'])(login)
#auth.route('/create', methods=['POST'])(store)
#auth.route('/<int:user_id>', methods=['GET'])(show)
#auth.route('/<int:user_id>/edit', methods=['POST'])(update)
#auth.route('/<int:user_id>', methods=['DELETE'])(destroy)