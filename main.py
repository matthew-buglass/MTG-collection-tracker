#  Copyright (c) Matthew Buglass
#  Author: Matthew Buglass
#  Maintainer: Matthew Buglass
#  Website: matthewbuglass.com
#  Date: 9/18/21, 9:50 AM
import json

import requests

def get_default_cards():
    """
    Queries scryfall API (https://scryfall.com/docs/api) for current lists of magic cards.

    :return: str
    """
    response = requests.get("https://api.scryfall.com/bulk-data/default_cards")

    if response.status_code == 200:
        print("successfully retrieved bulk data.")
        response_json = response.json()

        card_response = requests.get(response_json["download_uri"])

        if card_response.status_code == 200:
            print("successfully retrieved default cards.")
            card_json = card_response.json()
            print("{} cards found".format("{:,}".format(len(card_json))))
            print(json.dumps(card_json[0:3], indent=4))

            card_response.close()
        else:
            print("failed to retrieve default cards. Error code: " + str(card_response.status_code))

        response.close()
    else:
        print("failed to retrieve bulk data. Error code: " + str(response.status_code))

if __name__ == '__main__':
    get_default_cards()
