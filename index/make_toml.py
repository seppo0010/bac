from lxml import etree
import os
import sys

import toml
from bs4 import BeautifulSoup

'''
[input]
base_directory = "federalist"
url_prefix = "https://www.gutenberg.org/files/1404/1404-h/1404-h.htm#link2H_4_"
files = [
    {path = "federalist-1.txt", url = "0001", title = "General Introduction"},
    {path = "federalist-2.txt", url = "0002", title = "Concerning Dangers from Foreign Force and Influence"},
    {path = "federalist-3.txt", url = "0003", title = "Concerning Dangers from Foreign Force and Influence 2"},
    {path = "federalist-4.txt", url = "0004", title = "Concerning Dangers from Foreign Force and Influence 3"},
]
'''
def main():
    d = sys.argv[1]
    base = {
        'input': {
            'base_directory': d,
            'html_selector': 'div#divImprimir',
            'files': [],
            'stemming': 'Spanish',
        }
    }
    for f in os.listdir(d):
        with open(os.path.join(d, f)) as fp:
            soup = BeautifulSoup(fp.read(), 'html.parser')
        dom = etree.HTML(str(soup))
        title = ''
        if dom is not None:
            titles = dom.xpath('//*[@id="ctl00_CPH1_UCVistaPreviaPliego_usrCabeceraPliego_lblNomPliego"]')
            if titles is not None and len(titles) > 0:
                title = titles[0].text
        base['input']['files'].append({
            'path': f,
            'title': title,
            'url': f.replace('_', '/'),
            'filetype': 'HTML',
        })
    print(toml.dumps(base))

if __name__ == '__main__':
    main()
