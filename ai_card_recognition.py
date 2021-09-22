#  Copyright (c) Matthew Buglass
#  Author: Matthew Buglass
#  Maintainer: Matthew Buglass
#  Website: matthewbuglass.com
#  Date: 9/22/21, 12:52 PM

# BIG NOTE: The rule of not feeding your entire dataset is being broken here. This is because
# that rule exists for when you are training on a sample and extrapolating out into a population.
# For this dataset, this is not the case. Scryfall has almost the entirety of Magic's card
# history so we essentially have the population of cards.
#
# Additionally we are not trying to generalize predictions. Because each card entry is unique, from name, art,
# artist, release yer, edition number, etc. We want to be able to recognize and classify the exact card.
import ssl
import time
from os import listdir

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


def download_small_images(card_list: list[card.Card], all_new: bool):
    """
    Downloads the small images from scryfall for training

    :param card_list: list of card objects
    """
    delay = 105    # ms delay between each call to avoid overloading the API
    my_path = os.path.dirname(os.path.abspath("top_level_file.txt"))

    for c in card_list:
        filename = "images\\small\\" + c.id + ".jpg"

        ids_present = [f.rstrip(".jpg") for f in listdir(my_path + "\\images\\small\\")]

        if c.id not in ids_present or all_new:
            try:
                img_response = requests.get("https://c1.scryfall.com/file/scryfall-cards/small/front/{}/{}/{}.jpg".format(
                    c.id[0],
                    c.id[1],
                    c.id))

                if img_response.status_code == 429:
                    print("Too many requests. Sleeping for 2 seconds")
                    time.sleep(2)
                    img_response = requests.get("https://c1.scryfall.com/file/scryfall-cards/small/front/{}/{}/{}.jpg".format(
                        c.id[0],
                        c.id[1],
                        c.id))

                if img_response.status_code == 200:
                    img_data = img_response.content
                    with open(filename, "wb") as img:
                        img.write(img_data)
                        img.close()
                        print("Wrote {} small image to file".format(c.name))
                else:
                    print("\n---------------  Got code {} while getting image for {}. Skipping ---------------\n".format(
                        img_response.status_code,
                        c.name))
                
                time.sleep(delay/1000)
            except ssl.SSLEOFError:
                print("\n---------------  Got SSL EOF error while getting image for {}. Skipping ---------------\n".format(
                    c.name))

        # time.sleep(delay/1000.0)


def prepare_data(card_list):
    """
    Prepares the data set given a list of card data

    :param card_list: list of card objects
    :return: A
    """
    print("preparing data")
    
if __name__ == '__main__':
    cards = main.get_default_cards()
    download_small_images(cards[0], False)
