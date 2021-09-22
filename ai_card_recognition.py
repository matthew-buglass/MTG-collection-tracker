#  Copyright (c) Matthew Buglass
#  Author: Matthew Buglass
#  Maintainer: Matthew Buglass
#  Website: matthewbuglass.com
#  Date: 9/22/21, 10:19 AM

# BIG NOTE: The rule of not feeding your entire dataset is being broken here. This is because
# that rule exists for when you are training on a sample and extrapolating out into a population.
# For this dataset, this is not the case. Scryfall has almost the entirety of Magic's card
# history so we essentially have the population of cards.
#
# Additionally we are not trying to generalize predictions. Because each card entry is unique, from name, art,
# artist, release yer, edition number, etc. We want to be able to recognize and classify the exact card.
import time

import requests

import card
import main

import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


def download_small_images(card_list: list[card.Card]):
    """
    Downloads the small images from scryfall for training

    :param card_list: list of card objects
    """
    delay = 105    # ms delay between each call to avoid overloading the API

    for c in card_list[0:15]:
        image_uri = c.image_uris["small"]

        img_data = requests.get(image_uri).content
        with open("images/small/" + c.id + ".jpg", "wb") as img:
            img.write(img_data)
            img.close()

        time.sleep(delay/1000.0)


def prepare_data(card_list):
    """
    Prepares the data set given a list of card data

    :param card_list: list of card objects
    :return: A
    """