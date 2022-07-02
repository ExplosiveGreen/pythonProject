from services.animeList import anime_list
from services.crack_password import main
from services.graphics_cards_avalibility import main
from services.income_tax_calculator_us import main
def animeList():
    return anime_list()


def crack_password(username):
    return main(username)


def graphics_cards_availability():
    return main()


def income_tax_calculator_us(income):
    return main(income)


def job_salary():
    return "job_salary"


def neat_flappy_bird_training():
    return "neat_flappy_bird_training"


def predict_classification():
    return "predict_classification"


def SVM():
    return "SVM"


def tensorflow_image_recognition():
    return "tensorflow_image_recognition"


def tensorflow_prediction_model_training():
    return "tensorflow_prediction_model_training"


def tensorflow_recognition_training():
    return "tensorflow_recognition_training"


def tensorflow_text_classification():
    return "tensorflow_text_classification"


def years_to_retirement():
    return "years_to_retirement"

# pseudocode
# import sys
# from flask import render_template, redirect, url_for, request, abort
# from models.User import User
# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy()
# def index():
#     ...
# def store():
#     ...
# def show(userId):
#     ...
# def update(userId):
#     ...
# def delete(userId):
#     ...
