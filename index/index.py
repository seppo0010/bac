from lxml import etree
import os
import sys
import subprocess

import toml

def chunks(L, n): return [L[x: x+n] for x in range(0, len(L), n)]


BATCH_SIZE = 30000
def main():
    d = sys.argv[1]
    for i, ch in enumerate(chunks(os.listdir(d), BATCH_SIZE)):
        print(f'processing batch {i}')
        base = {
            'input': {
                'base_directory': d,
                'html_selector': 'div#divImprimir',
                'files': [],
                'stemming': 'Spanish',
            }
        }
        for f in ch:
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
        with open('index.toml', 'w') as fp:
            fp.write(toml.dumps(base))
        subprocess.check_call(['stork', 'build', '--input', 'config.toml', '--output', f'index{i}.st'])
        break

if __name__ == '__main__':
    main()
