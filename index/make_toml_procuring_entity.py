from lxml import etree
import os
import sys

import toml
import pandas as pd

def main():
    d = sys.argv[1]
    csv_path = sys.argv[2]
    pe = sys.argv[3]
    base = {
        'input': {
            'base_directory': d,
            'html_selector': 'div#divImprimir',
            'files': [],
            'stemming': 'Spanish',
        }
    }

    df = pd.read_csv(csv_path)
    df = df[df['tender/procuringEntity/name'] == pe]
    for f in df['tender/documents/0/url'].to_dict().values():
        f = f.replace('/', '_')
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
