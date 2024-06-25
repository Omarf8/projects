import re
import requests
from bs4 import BeautifulSoup

def wiki():
    page_name = input("Enter the Wikipedia page name: ")
    page_name = page_name.replace(" ", "_")

    baseurl = "https://en.wikipedia.org/wiki/"
    page_url = baseurl + page_name


    wikipedia = requests.get(page_url)
    content = wikipedia.text
    soup = BeautifulSoup(content, 'lxml')

    ''' Make a function to check the link for a tag 'no article text' and if it finds it
    check the website using different capitilization for a good website
    '''

    noArticle = soup.find("div", class_="no-article-text-sister-projects")
    if noArticle != None:
        return print("Try to submit the Wikipedia Page with different capitalization")


    referenceBox = soup.find_all("div", class_="reflist")

    ''' Finds the amount of REFERENCES
    in a Wikipedia Page '''
    if len(referenceBox) == 0:
        print("No References")
    elif len(referenceBox) > 1:
        # Creates a pattern to find a specific piece of text in the format found within compile()
        pattern = re.compile("id=\"cite_note([\S]+)>", re.IGNORECASE)
        # Creates a list with the amount of times it found the pattern inside the HTML text
        result = pattern.findall(str(referenceBox[len(referenceBox) - 1]))

        print(f"Amount of References: {len(result)}")
    else:
        pattern = re.compile("id=\"cite_note([\S]+)>", re.IGNORECASE)
        result = pattern.findall(str(referenceBox[0]))

        print(f"Amount of References: {len(result)}")


    ''' Finds the link needed to
    scrape the info page
    '''

    # Takes the URL for the page that has all the info about the Wikipedia Page
    info_box = soup.find("li", id="t-info")

    findInfoLink = re.compile("href=\"([\S]+)\"", re.IGNORECASE)
    infoResult = findInfoLink.search(str(info_box))

    # Removes the "amp" in the string causing the page to redirect to the wrong page
    infoResult = infoResult.group(1).replace("&amp;", "&")

    info_page = "https://en.wikipedia.org" + infoResult

    # Process to have access to all the HTML on the info page
    infoWikipedia = requests.get(info_page)
    infoContent = infoWikipedia.text
    infoSoup = BeautifulSoup(infoContent, "lxml")

    ''' Finds the Creation Date of the
    Wikipedia Page
    '''

    # # Finds an HTML tag with the tag as "tr" and a class starting with "mw-pageinfo-firsttime"
    creationTag = infoSoup.find("tr", id="mw-pageinfo-firsttime")

    # # Finds the Birth Date Pattern in the format "TIME, DAY MONTH YEAR"
    datePattern = re.compile(">([\d:]+),\s([\d]+)\s([\w]+)\s([\d]+)<", re.IGNORECASE)
    dateResult = datePattern.search(str(creationTag))

    # Prints the date that the Wikipedia Page was created 
    print(f"Date Creation: {dateResult.group(3)} {dateResult.group(2)}, {dateResult.group(4)} at {dateResult.group(1)}")

    ''' Finds the number of edits done
    on a Wikipedia Page
    '''

    editTag = infoSoup.find("tr", id="mw-pageinfo-edits")

    # Finds the # of edits in the format '</td><td>NUMBER'
    editPattern = re.compile("</td><td>([\d,]+)", re.IGNORECASE)
    editResult = editPattern.search(str(editTag))

    print(f"Number of Edits: {editResult.group(1)}")

wiki()
