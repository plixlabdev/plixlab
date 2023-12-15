from pybtex.database.input import bibtex
import os


def get_authors(authors):

     # Printing authors---------------------
     names = []
     for author in authors:
      if len(author.middle_names) > 0:
        middle= author.middle_names[0] + '. '
      else:  middle = ''
      name = author.first_names[0][0] + '. ' + middle +   author.last_names[0]
      names.append(name)

     if len(names) == 1:
      authors = names[0] + ', '
     elif len(names) > 1 :
      authors = names[0] + ' _et al_.'
     #--------------------------------------

     return authors

def render_software(bib_data):

     authors = get_authors(bib_data.persons['author'])
     year      = bib_data.fields['year']
     url       = bib_data.fields['url']
     text = authors + ' ' + '[' + url + '](' + url + '), ' + year 

     return text

def render_book(bib_data):

     authors = get_authors(bib_data.persons['author'])
     year      = bib_data.fields['year']
     url       = bib_data.fields['url']
     publisher       = bib_data.fields['publisher']
     text = authors + ' ' + '[' + publisher + '](' + url + '), ' + year 

     return text





def format(entry_key):


    #local
    if os.path.isfile('biblio.bib') :
       name = 'biblio.bib'
    else:   
       home_dir = os.path.expanduser("~")
       #User-wide
       if not os.path.isfile(home_dir + '/.plix/biblio.bib') :
           print('No biblio file found')
           quit()
       else:    
         name = home_dir + '/.plix/biblio.bib'

    bib_data = bibtex.Parser().parse_file(name).entries[entry_key]

    
    if bib_data.type == 'software':
        return render_software(bib_data)
    elif bib_data.type == 'book':
        return render_book(bib_data)

    else:
 
     authors = get_authors(bib_data.persons['author'])
     #Journal
     journal   = bib_data.fields['journal']
     year      = bib_data.fields['year']
     pages     = bib_data.fields['pages']
     volume    = bib_data.fields['volume']
     url       = bib_data.fields['url']
     text = authors + ' ' + '[' + journal + '](' + url + ') '  + volume + ', ' + pages + ' (' + year + ')'
    return text



