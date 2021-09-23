#  Copyright (c) Matthew Buglass
#  Author: Matthew Buglass
#  Maintainer: Matthew Buglass
#  Website: matthewbuglass.com
#  Date: 9/23/21, 11:16 AM

# BIG NOTE: The rule of not feeding your entire dataset is being broken here. This is because
# that rule exists for when you are training on a sample and extrapolating out into a population.
# For this dataset, this is not the case. Scryfall has almost the entirety of Magic's card
# history so we essentially have the population of cards.
#
# Additionally we are not trying to generalize predictions. Because each card entry is unique, from name, art,
# artist, release yer, edition number, etc. We want to be able to recognize and classify the exact card.
import ssl
import sys
import time
from os import listdir

import requests
import urllib3.exceptions

import card
import main

import matplotlib.pyplot as plt
import numpy as np
import os
import PIL
# import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

class RollingQueue:
    def init(self):
        self.max_queue = 100
        self.queue = []

    def enqueue(self, value):
        if len(self.queue) == self.max_queue:
            self.queue = self.queue[1:]

        self.queue.append(value)

    def get_avg(self):
        return self.queue.sum() / len(self.queue)

def download_small_images(card_list: list[card.Card], all_new: bool):
    """
    Downloads the small images from scryfall for training

    :param card_list: list of card objects
    """
    delay = 105    # ms delay between each call to avoid overloading the API
    my_path = os.path.dirname(os.path.abspath("top_level_file.txt"))
    last_size = 0
    entries = len(card_list)
    count = 0
    msg = ""
    error_log = ["Error log:"]
    times = RollingQueue()

    print("\n\n ----------- Getting Card Images:  -----------")

    for c in card_list:
        t1 = time.time()
        filename = "images\\small\\" + c.id + ".jpg"

        ids_present = [f.rstrip(".jpg") for f in listdir(my_path + "\\images\\small\\")]

        if c.id not in ids_present or all_new:
            try:
                img_response = requests.get("https://c1.scryfall.com/file/scryfall-cards/small/front/{}/{}/{}.jpg".format(
                    c.id[0],
                    c.id[1],
                    c.id))

                if img_response.status_code == 429:
                    msg = "Too many requests. Sleeping for 2 seconds"
                    last_size = print_loading_progress(last_size, msg, count, entries)
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
                        msg = "Wrote {} small image to file".format(c.name)
                else:
                    msg = "Got code {} while getting image for {} - {}. Skipping".format(
                        img_response.status_code,
                        c.name,
                        c.id)

                    error_log.append(msg)

                # time.sleep(delay/1000)
            except ssl.SSLEOFError:
                msg = "Got SSL EOF error while getting image for {} - {}. Skipping".format(
                    c.name,
                    c.id)
                error_log.append(msg)


            except urllib3.exceptions.MaxRetryError:
                msg = "Got Max Retry Error while getting image for {} - {}. Skipping".format(
                    c.name,
                    c.id)
                error_log.append(msg)
            except requests.exceptions.SSLError:
                msg = "Got an SSL Error from requests while getting image for {} - {}. Skipping".format(
                    c.name,
                    c.id)
                error_log.append(msg)
        else:
            msg = "Image for {} already on disk".format(c.id)

        count += 1
        # last_size = print_loading_progress(last_size, msg, count, entries)

        # estimating the time left
        t2 = time.time()
        times.enqueue(t2-t1)
        avg_time = times.get_avg()
        remaining_cards = entries - count
        seconds_remaining = avg_time * remaining_cards
        hrs = seconds_remaining // 3600
        mins = (seconds_remaining % 3600) // 60
        secs = (seconds_remaining % 3600) % 60

        printProgressBar(count, entries, "Progress: {:,} of {:,}".format(count, entries),
                         suffix="Estimated Time Remaining: {:03}:{:02}:{:02} - ID: {}".format(int(hrs), int(mins), int(secs), c.id),
                         length=50)

        # time.sleep(delay/1000.0)
    print("\n\n ----------- Error Log -----------\n{}".format("\n".join(error_log)))


def print_loading_progress(last_len, msg, complete, total):
    loading_bar_len = 50
    progress = float(complete) / float(total)
    complete_bars = int(loading_bar_len * progress)
    incomplete_dashes = loading_bar_len - complete_bars - 1

    # printing new things to the console after clearing it
    progress_str = "Progress: {:,} out of {:,} ".format(complete, total)
    loading_bar = "[{}{}{}] {:.2f}% - ".format("=" * complete_bars, ">", "-" * incomplete_dashes, 100*progress)
    final_string = progress_str + loading_bar + msg

    print(" " * last_len + "\r" + final_string, end="\r")

    # returning the final length of the recent print
    return len(final_string)

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 2, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

    sys.stdout.flush()


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
