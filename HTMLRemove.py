from HTMLParser import HTMLParser
import re

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def stripCode(html):
    #print re.findall('<pre><code>.*?</code></pre>|<code>.*?</code>', html)
    html = re.sub('<code>.*?</code>', '', html, flags=re.DOTALL)
    return html

def stripLinks(string):
    return re.sub(r'^https?:\/\/.*[\r\n]*', '', string, flags=re.MULTILINE)