#  Copyright (c) Matthew Buglass
#  Author: Matthew Buglass
#  Maintainer: Matthew Buglass
#  Website: matthewbuglass.com
#  Date: 9/18/21, 11:09 AM
import json


class Card:
    def __init__(self, j:json):
        self.name = j["name"].replace(",", "")
        self.rarity = j["rarity"]
        self.id = j["id"]
        self.uri = j["scryfall_uri"]
        self.lang = j["lang"]
        self.super_type, self.type, self.sub_type = self.split_types(j["type_line"])
        self.foil = j["foil"]
        self.nonfoil = j["nonfoil"]
        self.set_name = j["set_name"]
        self.collector_number = j["collector_number"]
        self.artist = j["artist"].replace(",", "")

        try:
            self.illustration_id = j["illustration_id"]
        except KeyError:
            self.illustration_id = None

        self.booster = j["booster"]
        self.price_usd = j["prices"]["usd"]
        self.price_foil_usd = j["prices"]["usd_foil"]
        self.price_etched_usd = j["prices"]["usd_etched"]

    def get_csv_line(self) -> str:
        return "{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n".format(
            self.name, self.rarity, self.id, self.uri, self.lang, self.super_type, self.type,
            self.sub_type, self.foil, self.nonfoil, self.set_name, self.collector_number, self.artist,
            self.illustration_id, self.booster, self.price_usd, self.price_foil_usd, self.price_etched_usd)

    def get_csv_header(self) -> str:
        return "name, rarity, id, uri, lang, super_type, type, sub_type, foil, nonfoil, set_name, " \
               "collector_number, artist, illustration_id, booster, price_usd, price_foil_usd, " \
               "price_etched_usd\n"

    def print_string(self):
        print(self.get_csv_line())

    @staticmethod
    def split_types(type_line) -> (str, str, str):
        """
        Splits the creature type into super-type, type, and sub-type
        :param type_line: the line type of the creature
        :return: (str, str, str): (super-type, type, sub-type)
        """
        if ("//" in type_line):
            split_faces = type_line.split("//")
            backside = split_faces[1].strip()
            back_item = backside.split("—")[-1].strip()

            type_line = split_faces[0] + "// " + back_item

        split_hyphen = type_line.split("—")
        split_hyphen = [x.strip() for x in split_hyphen]

        if len(split_hyphen) == 1:
            return None, split_hyphen[0], None
        else:
            split_spaces = split_hyphen[0].split(" ")

            if len(split_spaces) == 1:
                return None, split_spaces[0], split_hyphen[1]
            else:
                return split_spaces[0], split_spaces[1], split_hyphen[1]

    # @classmethod
    # def from_json(cls, j):
    #     return Card(**json.loads(j))
