#  Copyright (c) Matthew Buglass
#  Author: Matthew Buglass
#  Maintainer: Matthew Buglass
#  Website: matthewbuglass.com
#  Date: 9/18/21, 10:07 AM
import json


class Card:
    def __init__(self, name, rarity, id, uri, lang, type_line, foil, nonfoil, set_name, collector_number, artist,
                 illustration_id, booster, prices):
        self.name = name
        self.rarity = rarity
        self.id = id
        self.uri = uri
        self.lang = lang
        self.type_line = type_line
        self.foil = foil
        self.nonfoil = nonfoil
        self.set_name = set_name
        self.collector_number = collector_number
        self.artist = artist
        self.illustration_id = illustration_id
        self.booster = booster
        self.price_usd = prices["usd"]
        self.price_foil_usd = prices["usd_foil"]
        self.price_etched_usd = prices["usd_etched"]

    def to_csv_line(self) -> str:
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(
            self.name, self.rarity, self.id, self.uri, self.lang, self.type_line, self.foil,
            self.nonfoil, self.set_name, self.collector_number, self.artist,
            self.illustration_id, self.booster, self.price_usd, self.price_foil_usd, self.price_etched_usd)

    def print_string(self):
        print(self.to_csv_line())

    @classmethod
    def from_json(cls, j):
        return Card(**json.loads(j))
