#from pybtex.database.input import bibtex
import bibtexparser
def get_authors(authors_str):
    """
    Generate a string representation of authors from a BibTeX-style string.
    If there is only one author, returns "FirstInitial. MiddleInitial. LastName, ".
    If there are multiple authors, returns "FirstAuthor _et al_.".

    Parameters:
        authors_str (str): A string of authors in BibTeX format (e.g., "Last, First Middle and Last, First").

    Returns:
        str: Formatted author string.
    """
    # Split the authors string into individual authors
    author_list = [author.strip() for author in authors_str.split(" and ")]

    # List to hold formatted author names
    formatted_names = []

    for author in author_list:
        # Split into "Last, First Middle" or "First Middle Last" format
        if ", " in author:
            last_name, first_name_middle = author.split(", ", 1)
            name_parts = first_name_middle.split()
        else:
            name_parts = author.split()
            last_name = name_parts[-1]

        # Extract first and middle names
        first_name = name_parts[0]
        middle_name = name_parts[1] if len(name_parts) > 1 else ""

        # Construct the formatted name
        middle_initial = f"{middle_name[0]}." if middle_name else ""
        formatted_name = f"{first_name[0]}. {middle_initial}{last_name}".strip()
        formatted_names.append(formatted_name)

    # Generate the final author string based on the number of authors
    if len(formatted_names) == 1:
        authors_string = f"{formatted_names[0]}, "
    elif len(formatted_names) > 1:
        authors_string = f"{formatted_names[0]} _et al_."
    else:
        authors_string = "No authors available."

    return authors_string


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




def format(filename,entry_key):


    #bib_data = bibtex.Parser().parse_file(filename).entries[entry_key]


    library = bibtexparser.parse_file(filename)


    # Access a specific entry by key
    bib_data = next((entry for entry in library.entries if entry.key == entry_key), None)


    
    if bib_data.entry_type == 'software':
        return render_software(bib_data)
    elif bib_data.entry_type == 'book':
        return render_book(bib_data)

    else:
     
    
     
     authors = get_authors(bib_data.get('author').value)
 
     journal = bib_data.get("journal", "Unknown Journal").value
     year = bib_data.get("year", "Unknown Year").value
     pages = bib_data.get("pages", "Unknown Pages").value
     volume = bib_data.get("volume", "Unknown Volume").value
     url = bib_data.get("url", "#").value

     # Construct the formatted text
     text = (
        f"{authors} [{journal}]({url}) {volume}, {pages} ({year})"
     )

    return text



