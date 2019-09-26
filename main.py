# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 11:44:59 2019

@author: borre001


"""

# TODO: include proxy in the download.
# TODO: in case multiple files include threaded downloads using several proxies

from requests import get
from requests import codes

BASE_URL = "http://www.omie.es/informes_mercado/"


def generate_url(market="diario", session="1", year="2019", month="09",
                 day="09"):
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
                   [market, session, year, month, day])):
        raise TypeError("Only strings are allowed")

    if market == "diario":
        market_code = "PBC_EV_H_1"
    elif market == "intradiario":
        market_code = "PIB_EV_H_1_" + session

    date = "_".join([day, month, year])
    url = BASE_URL + "AGNO_" + str(year) + "/MES_" + str(month) + \
        "/TXT/INT_" + market_code + "_" + date + "_" + date + ".txt"

    return url


def retrieve_single_file(url, save=False):
    """
    Retrieves only one file. No threading. Serves it as a pandas object
    or saves it as a csv.
    """
    file = get(url)

    if not file.status_code == codes.ok:
        raise "Failure in the connection"

    
