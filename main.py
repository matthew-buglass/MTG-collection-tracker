#  Copyright (c) Matthew Buglass
#  Author: Matthew Buglass
#  Maintainer: Matthew Buglass
#  Website: matthewbuglass.com
#  Date: 9/18/21, 10:43 AM
import json

import requests

from card import Card


def get_default_cards():
    """
    Queries scryfall API (https://scryfall.com/docs/api) for current lists of magic cards.

    :return: str
    """
    response = requests.get("https://api.scryfall.com/bulk-data/default_cards")

    if response.status_code == 200:
        print("successfully retrieved bulk data.")
        response_json = response.json()
        date = response_json["updated_at"]

        card_response = requests.get(response_json["download_uri"])

        if card_response.status_code == 200:
            print("successfully retrieved default cards.")
            card_json = card_response.json()
            print("{} cards found".format("{:,}".format(len(card_json))))
            card_response.close()

            card_list = []

            for c in card_json:
                card_list.append(Card(c))

            return card_list, date
        else:
            print("failed to retrieve default cards. Error code: " + str(card_response.status_code))
            card_response.close()

        response.close()
    else:
        print("failed to retrieve bulk data. Error code: " + str(response.status_code))
        response.close()


if __name__ == '__main__':
    cards, date = get_default_cards()
    header = cards[0].get_csv_header()

    with open("mtg_card_data_"+date+".csv", "w+") as f:
        f.write(header + "\n")

        for c in cards:
            f.write(c.get_csv_line())

        f.close()

