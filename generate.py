
import datetime
import yaml
from jinja2 import Template
from yaml import Loader

class Paper:

  def __init__(self, data):
    self.title = data['title']
    self.authors = self.format(data['authors'])
    self.venue = data['venue']
    self.url = data['url']
    self.code = data.get('code', None)
    self.year = data['year']
    self.comment = data.get('comment', None)

  def format(self, authors):
    if len(authors) == 1:
      return '<u>A. Araujo</u>' 
    for i in range(len(authors)):
      if 'A. Araujo' in authors[i]:
        authors[i] = f'<u>{authors[i]}</u>'
    sep = [', '] * (len(authors)-2)
    sep += [' and ']
    authors_str = ''
    for author, sep in zip(authors, sep):
      authors_str += author
      authors_str += sep
    authors_str += authors[-1]
    return authors_str


def generate_bibtex():
  with open('bibtex.bib', 'r') as f:
    bibtex = f.read()
  kwords = []
  title_map = {}
  bibtex_lines = bibtex.split('\n')
  bibtex_cite = bibtex.split('\n\n')
  for line in bibtex_lines:
    if len(line) > 0 and '@' in line[0]:
      keyword = line.split('{')[-1].replace(',', '')
      kwords.append(keyword)
    if 'title' in line:
      title = line.split('{')[-1].replace('},', '')
      title_map[title] = keyword
  for keyword, cite in zip(kwords, bibtex_cite):
    filename = './static/bibtex/{}.txt'.format(keyword)
    with open(filename, 'w') as f:
      f.write(cite)

  # for k,v in title_map.items():
  #   print(k, v)

  return title_map

def generate_website(title_map):

  with open('description.txt') as f:
    description = f.read()

  papers = []
  with open('data.yaml') as f:
    for doc in yaml.load_all(f, Loader=Loader):
      papers.append(Paper(doc))
  papers = papers[::-1]

  for paper in papers:
    paper.bibtex = title_map[paper.title]

  date = datetime.datetime.now()
  with open('template.temp') as f:
    template = Template(f.read())
  html = template.render(
    description=description, papers=papers, date=date.strftime("%B %Y"))

  with open('index.html', 'w') as f:
    f.write(html)



if __name__ == '__main__':
  title_map = generate_bibtex()
  generate_website(title_map)

