from urllib import request
from urllib.parse import unquote
from bs4 import BeautifulSoup

import requests
import ssl
import os


def main():
    ssl._create_default_https_context = ssl._create_stdlib_context
    #find_roms_by_html_page()
    find_roms_by_link_page()


def find_roms_by_html_page():
    host = "https://r-roms.github.io/megathread/retro/"

    page = get_page(host)
    console_tables = page.find_all("table")

    for console_table in console_tables:
        console_bodies = console_table.find_all("tbody")
        for console_body in console_bodies:
            console_rows = console_body.find_all("tr")
            for console_row in console_rows:
                console_columns = console_row.find_all("td")
                folder = console_columns[0].get_text()
                href = console_columns[1].find("a")["href"]
                if href.startswith("https://myrient.erista.me/files/No-Intro/"):
                    rom_page = get_page(href)
                    table = rom_page.find("table", {"id": "list"})
                    if table is not None:
                        tbody = table.find("tbody")
                        if tbody is not None:
                            trs = tbody.find_all("tr")
                            for tr in trs:
                                rom_link = tr.find("a").attrs["href"]
                                if rom_link is None or rom_link == '../':
                                    continue
                                path = href + rom_link

                                download_file(path, folder)


def find_roms_by_link_page():
    links = [
        # "https://myrient.erista.me/files/No-Intro/Atari%20-%202600/",
        # "https://myrient.erista.me/files/No-Intro/Atari%20-%205200/",
        # "https://myrient.erista.me/files/No-Intro/Atari%20-%207800/",
        # "https://myrient.erista.me/files/No-Intro/NEC%20-%20PC%20Engine%20-%20TurboGrafx-16/",
        # "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/",
        # "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Color/",
        # "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy/",
        # "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(BigEndian)/",
        # "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/",
        # "https://myrient.erista.me/files/No-Intro/Sega%20-%2032X/",
        # "https://myrient.erista.me/files/No-Intro/Sega%20-%20Master%20System%20-%20Mark%20III/",
        # "https://myrient.erista.me/files/No-Intro/Sega%20-%20Mega%20Drive%20-%20Genesis/",
        # "https://archive.org/download/mame-sl/mame-sl/",
        # "https://archive.org/download/MAME_0.225_CHDs_merged/",
        # "https://archive.org/download/mame-merged/mame-merged/",
        # "https://archive.org/download/hbmame_0244_roms/",
        # "https://archive.org/download/mame-chds-roms-extras-complete/",
        # "https://archive.org/download/mame-support/Support/",
        "https://archive.org/download/fbnarcade-fullnonmerged/arcade/"
    ]

    for link in links:
        page = get_page(link)
        rom_links = page.find_all("a")
        for rom_link in rom_links:
            try:
                rom_link = rom_link.attrs["href"]
                if rom_link.endswith(".zip"):
                    path = link + rom_link
                    folder = link.replace("https://myrient.erista.me/files/No-Intro/", "").replace("https://archive.org/download/", "").split('/')[0]
                    download_file(path, unquote(folder))
            except Exception as e:
                continue
    print("Done.")


def get_page(url):
    page = requests.get(url)
    page_html = BeautifulSoup(page.content, 'html.parser')
    return page_html


def get_links_from_css(html, css_selector):
    links = html.select(css_selector)
    return links


def get_all_links(html):
    links = html.find_all('a')
    return links


def download_file(url, folder):
    full_path = './roms/' + folder

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    full_path_filename = full_path + '/' + unquote(url.split('/')[-1])
    if os.path.isfile(full_path_filename):
        print('File ' + full_path_filename + ' exists.')
        return

    try:
        print('Downloading link ' + unquote(url))
        file = request.urlopen(url)
        with open(full_path_filename, 'wb') as f:
            f.write(file.read())
    except:
        print('Erro ao baixar a url ' + unquote(url))


if __name__ == "__main__":
    main()
