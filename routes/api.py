from flask import Blueprint

from controllers.api import \
    animeList,\
    crack_password,\
    graphics_cards_availability,\
    income_tax_calculator_us,\
    job_salary,\
    neat_flappy_bird_training,\
    predict_classification,\
    SVM,\
    tensorflow_image_recognition,\
    tensorflow_prediction_model_training,\
    tensorflow_recognition_training,\
    tensorflow_text_classification,\
    years_to_retirement


api = Blueprint('api', __name__)


api.route('/animeList', methods=['GET'])(animeList)
api.route('/crack_password/<username>', methods=['GET'])(crack_password)
api.route('/graphics_cards_availability', methods=['GET'])(graphics_cards_availability)
api.route('/income_tax_calculator_us/<income>', methods=['GET'])(income_tax_calculator_us)
api.route('/job_salary', methods=['GET'])(job_salary)
api.route('/neat_flappy_bird_training', methods=['GET'])(neat_flappy_bird_training)
api.route('/predict_classification', methods=['GET'])(predict_classification)
api.route('/SVM', methods=['GET'])(SVM)
api.route('/tensorflow_image_recognition', methods=['GET'])(tensorflow_image_recognition)
api.route('/tensorflow_prediction_model_training', methods=['GET'])(tensorflow_prediction_model_training)
api.route('/tensorflow_recognition_training', methods=['GET'])(tensorflow_recognition_training)
api.route('/tensorflow_text_classification', methods=['GET'])(tensorflow_text_classification)
api.route('/years_to_retirement', methods=['GET'])(years_to_retirement)
# api.route('/', methods=['GET'])(index)
# api.route('/create', methods=['POST'])(store)
# api.route('/<int:user_id>', methods=['GET'])(show)
# api.route('/<int:user_id>/edit', methods=['POST'])(update)
# api.route('/<int:user_id>', methods=['DELETE'])(destroy)
