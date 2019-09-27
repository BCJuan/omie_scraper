# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 11:44:59 2019

@author: borre001


"""

# TODO: include proxy in the download.
# TODO: in case multiple files include threaded downloads using several proxies

from requests import get
from requests import codes
from os import path
from os import mkdir
from shutil import rmtree
from argparse import ArgumentParser
from datetime import datetime

BASE_URL = "http://www.omie.es/informes_mercado/"


def parse():
    parser = ArgumentParser()
    parser.add_argument("-i", "--initial_date", dest="initial_date",
                        help="Initial date of period or single date",
                        type=str, default=None)
    parser.add_argument("-e", "--end_date", dest="end_date",
                        help="Final date of period",
                        type=str, default=None)
    parser.add_argument("-m", "--market", dest="market",
                        help="Type of market: diario, intradiario",
                        type=str, default="diario")
    parser.add_argument("-o", "--organize", dest="organize",
                        help="If you ahve downloaded the files you can\
                        organize them in a single file", default=False)
    return parser.parse_known_args()


class Retriever():

    def __init__(self, initial_date=None, end_date=None, market=None,
                 root="./data", diario='diario', intra='intradiario'):
        self.initial_date = initial_date
        self.end_date = end_date
        self.market = market
        self.path_root = root
        self.path_diario = path.join(self.path_root, diario)
        self.path_intradiario = path.join(self.path_root, intra)

        self.generate_tree_folder()

    def generate_url(self, session="1", year="2019",
                     month="09", day="09"):
        """
        Generates the url necessary to get the corresponding txt file in
        the omie page.

        Parameters
        ----------
        market : string
            which data, diario o intradiario
        session : string
            session in case is intradiario
        year : string
            year
        month : string
            if 1-9 needs to be in format "09"
        day : string
            same as month

        Returns
        -------
        url : string
            the url for the specified data

        """

        if not all(map(lambda x: isinstance(x, str),
                       [self.market, session, year, month, day])):
            raise TypeError("Only strings are allowed")

        if self.market == "diario":
            market_code = "PBC_EV_H_1"
        elif self.market == "intradiario":
            market_code = "PIB_EV_H_1_" + session

        date = "_".join([day, month, year])
        url = BASE_URL + "AGNO_" + year + "/MES_" + month + \
            "/TXT/INT_" + market_code + "_" + date + "_" + date + ".txt"

        return url

    def retrieve_data_single(self, url):
        """
        Retrieves only one file. No threading. Serves it as a pandas object
        or saves it as a csv.
        """
        file = get(url)

        if not file.status_code == codes.ok:
            raise "Failure in the connection"

        return file.text

    def generate_tree_folder(self, remove=False):
        if remove:
            rmtree(self.path_root)

        if not path.exists(self.path_root):
            mkdir(self.path_root)

        if not path.exists(self.path_diario):
            mkdir(self.path_diario)

        if not path.exists(self.path_intradiario):
            mkdir(self.path_intradiario)

        for i in range(1, 6):
            intra_specific = path.join(self.path_intradiario,
                                       "intra_" + str(i))

            if not path.exists(intra_specific):
                mkdir(intra_specific)

    def obtain_data(self):

        if self.end_date:
            # TODO: implement getting files per range
            pass
        else:
            self.save_single()

    def save_single(self):
        year, month, day = generate_date_data(self.initial_date)
        if self.market == "diario":
            url = self.generate_url(year=year, month=month, day=day)
            data = self.retrieve_data_single(url)
            name = path.join(self.path_diario,
                             year + "_" + month + "_" + day + ".txt")
            with open(name, "w") as file:
                file.write(data)

        elif self.market == "intradiario":
            for i in range(1, 6):
                url = self.generate_url(year=year, month=month, day=day,
                                        session=str(i))
                data = self.retrieve_data_single(url)
                name = path.join(self.path_intradiario, "intra_" + str(i),
                                 year + "_" + month + "_" + day + ".txt")
                with open(name, "w") as file:
                    file.write(data)


def convert_date(initial_date=None):
    return datetime.strptime(initial_date, "%Y-%m-%d")


def generate_date_data(dat=None):
    year = str(dat.year)
    month = str(dat.month)
    day = str(dat.day)

    month, day = ("0" + i for i in (month, day) if len(i) == 1)

    return year, month, day


def main():
    parsed = parse()[0]
    print(parsed)
    if parsed.organize:
        # TODO: implement function to organize all files in two files
        # diario and intradiario
        pass
    else:
        if parsed.end_date:
            end_date = convert_date(parsed.end_date)
        else:
            end_date = parsed.end_date
        initial_date = convert_date(parsed.initial_date)
        print(initial_date)
        retriever = Retriever(initial_date=initial_date,
                              end_date=end_date,
                              market=parsed.market)
        retriever.obtain_data()


if __name__ == "__main__":
    main()
