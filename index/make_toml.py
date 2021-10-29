from lxml import etree
import os
import sys

import toml

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
            dom = etree.HTML(str(fp.read()))
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
