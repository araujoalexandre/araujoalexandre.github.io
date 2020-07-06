
import datetime
import yaml
from jinja2 import Template
from yaml import Loader

class Paper:

  def __init__(self, data):
    self.name = data['name']
    self.authors = self.format(data['authors'])
    self.venue = data['venue']
    self.url = data['url']
    self.code = data['code']
    self.year = data['year']
    self.bibtex = data['bibtex']

  def format(self, authors):
    for i in range(len(authors)):
      if authors[i] == 'Alexandre Araujo':
        authors[i] = '<u>Alexandre Araujo</u>'
    sep = [', '] * (len(authors)-2)
    sep += [' and ']
    authors_str = ''
    for author, sep in zip(authors, sep):
      authors_str += author
      authors_str += sep
    authors_str += authors[-1]
    return authors_str
        

def main():

  papers = []
  with open('data.yaml') as f:
    for doc in yaml.load_all(f, Loader=Loader):
      papers.append(Paper(doc))
  papers = papers[::-1]

  date = datetime.datetime.now()
  with open('template.temp') as f:
    template = Template(f.read())
  html = template.render(papers=papers, date=date.strftime("%B %Y"))

  with open('index.html', 'w') as f:
    f.write(html)



if __name__ == '__main__':
  main()
