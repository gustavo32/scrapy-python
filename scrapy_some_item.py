# https://www.hardmob.com.br/forums/407-Promocoes?pp=30&sort=dateline&order=desc&daysprune=-1
import re
import requests
from win10toast import ToastNotifier
import time
import pickle
import os
import glob
from twilio.rest import Client


hardmob_filename = "https://www.hardmob.com.br/forums/407-Promocoes?pp=50&sort=dateline&order=desc&daysprune=-1"
pelando_filename = "https://www.pelando.com.br/recentes?page="
adrenaline_filename = "https://adrenaline.uol.com.br/forum/forums/for-sale.221/?order=post_date"

from_whatsapp_number = 'whatsapp:+14155238886'
to_whatsapp_number = 'whatsapp:+554396662771'

# Todo
# Create a filter
# Add More sites
# Identify some written errors


def hardmob_request(path):
    pattern = r"\<a class=\"title.*\".+\>.*\<"
    content = requests.get(path).text
    return re.findall(pattern, content)


def pelando_request(path):
    pattern = r"\<a\s*class=\"cept-tt thread-link.*\"\s*title=\".*\"\s*href=\".*\" data\-handler=\".*\" data\-track=.*\>\s.*?\<\/a"
    contents = []
    for i in range(1, 15):
        contents.append(requests.get(path+str(i)).text)
    content = " ".join(contents)

    return re.findall(pattern, content)


def adrenaline_request(path):
    pattern = r"\<a href=\"threads\/.*\"\s*title=\".*\"\s*class=\"PreviewTooltip\"\s*data-previewUrl=\"threads/.*\"\>.*\<"
    content = requests.get(path).text
    return re.findall(pattern, content)


def request_from_site(path, site):
    if site == "hardmob":
        matches = hardmob_request(path)
    elif site == "pelando":
        matches = pelando_request(path)
    elif site == "adrenaline":
        matches = adrenaline_request(path)

    only_titles = []
    for i in matches:
        item = re.search(r">\s*(.+)<", i).group(1)
        link = re.search(r"href=\"(.*?)\"", i).group(1)
        if site == "hardmob":
            link = "https://www.hardmob.com.br/"+link
        elif site == "adrenaline":
            link = "https://adrenaline.uol.com.br/forum/"+link

        title = item + "\n\t-> link: " + link + "\n"
        only_titles.append(title)

    return only_titles


def verify_already_exists(items, site):
    pkl_file = site+".pkl"
    if not os.path.isfile(pkl_file):
        with open(pkl_file, 'wb') as f:
            pickle.dump([], f)

    with open(pkl_file, 'rb') as f:
        items_pkl = pickle.load(f)
        if items_pkl is None:
            items_pkl = []

    return items_pkl


def create_or_adjust_pickle_file(items, site):
    items_pkl = verify_already_exists(items, site)
    toaster = ToastNotifier()
    pkl_file = site+".pkl"
    client = Client()
    for i in items:
        i = r""+i
        print(i)
        if i not in items_pkl:
            print(str(i))
            print(items_pkl)
            toaster.show_toast("Achei para você!", i)

            client.messages.create(body='Achei para você!\n'+i,
                                   from_=from_whatsapp_number,
                                   to=to_whatsapp_number)

            with open(pkl_file, "wb") as f:
                items_pkl.append(i)
                pickle.dump(items_pkl, f)

    for i in items_pkl:
        if i not in items:
            items_pkl.remove(i)
            with open(pkl_file, "wb") as f:
                pickle.dump(items_pkl, f)


def get_interested_item(path, name=r"[notebook]|[ideapad]|[macbook]", site="hardmob"):
    titles = request_from_site(path, site)

    interested_items = []
    for t in titles:
        match = re.search(name, t, flags=re.IGNORECASE)
        if match:
            interested_items.append(t)

    create_or_adjust_pickle_file(interested_items, site)


def open_pickle_and_write_txt():
    all_items = []
    pkl_files = glob.glob("*.pkl")
    for pkl_file in pkl_files:
        with open(pkl_file, 'rb') as f:
            items_pkl = pickle.load(f)
            for i in items_pkl:
                if i:
                    all_items.append(i)

    with open("../../../../Desktop/items_procurados.txt", "wb") as f:
        for item in all_items:
            f.write((item + "\n").encode())


while(True):
    get_interested_item(hardmob_filename,
                        name=r"notebook|ideapad|macbook", site="hardmob")
    get_interested_item(pelando_filename,
                        name=r"notebook|ideapad|macbook", site="pelando")
    get_interested_item(adrenaline_filename,
                        name=r"notebook|ideapad|macbook", site="adrenaline")

    open_pickle_and_write_txt()

    time.sleep(600)
