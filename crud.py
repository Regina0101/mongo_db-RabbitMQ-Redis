import json
from models import Author, Quote

def insert_data_author(authors_data):
    with open(authors_data, 'r') as file:
        data = json.load(file)

    authors = []
    for author_data in data:
        author = Author(
            fullname=author_data['fullname'],
            born_date=author_data['born_date'],
            born_location=author_data['born_location'],
            description=author_data['description']
        )
        author.save()
        print(f'Author "{author.fullname}" saved successfully')
        authors.append(author)

    return authors

def insert_data_quotes(quotes_data, authors):
    with open(quotes_data, 'r') as file:
        data = json.load(file)

    for quote_data in data:
        author_name = quote_data['author']
        author = next((author for author in authors if author.fullname == author_name), None)
        if author:
            quote = Quote(
                tags=quote_data['tags'],
                author=author,
                quote=quote_data['quote']
            )
            quote.save()
            print(f'Quote "{quote.quote}" saved successfully for author "{author.fullname}"')
        else:
            print(f'Author "{author_name}" not found for quote "{quote_data["quote"]}"')


authors = insert_data_author('authors.json')
insert_data_quotes('quotes.json', authors)
