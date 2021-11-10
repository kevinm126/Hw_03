# Hw_03
## Ebay scraper description
My ebay-dl.py file allows me to input certain parameters, such as a search term and a number of pages creates a .json file containing a list of dictionaries. each dictionary in the list pertains to an item up for sale on ebay. my ebay-dl.py file gives the *name, price, shipping price, status, amount of items sold, and whether or not shipping is free of an item*. The program does this for every item on as many pages as ebay allows or as many as you specify and the program covers all the items on the given page.
<br>
  
## using the ebay-dl.py file

to use the ebay-dl.py file you have to specify the required paremeters, preceded by `python3 ebay-dl.py`. In the case that you happen to use a search term with more than one word in it, you must use qoutes around the serach term. Additionally the program gives the option of specifying the number of pages by adding `--num_pages=x` , where x is the number of pages you wish to run the program on for the given search term. below i will show how i used this file to create my 3 json files

### To create the books.json file

in the terminal write

```python
python3 ebay-dl.py 'books'

```

### To create the movies.json file

in the terminal write

```python
python3 ebay-dl.py 'movies'

```


### To create the green apple.json file

in the terminal type

```python
python3 ebay-dl.py 'green apple'

```
**it is important for this last file or any file using a search term that is more than one word long, YOU MUST USE QOUTES AROUND YOUR SEARCH TERM. Otherwise the file will take it as two different parameters.**
