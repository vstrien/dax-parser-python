import requests, json, html, re
from bs4 import BeautifulSoup

def get_navigation_tree(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    categories = soup.body.div.header.nav("ul")
    navtreedict = {}

    # Split into different types of language elements
    print("Found {} categories".format(len(categories)))
    for c in categories:
        if "data-type" in c.attrs:
            categorytype = c["data-type"][:-1]
        else:
            categorytype = "Function"
        navtreedict[categorytype] = []
        print("Found {} {}s".format(len(c("li")), categorytype))
        for li in c("li"):
            navtreedict[categorytype].append(li.a["href"])

    return navtreedict

def get_syntax_definitions(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    
    # Get the title
    title = soup.select("div.left-container")[0].header.h1.a.text    
    # Get the syntax definition
    syntax = soup.select("div.notation")[0].text
    # Regex to remove whitespace and newline characters
    syntax = re.sub(r"\s+", " ", syntax)

    # Get the return type
    return_type = None
    return_section = soup.select("section#returns")
    if len(return_section) > 0 and len(return_section[0]("div")) > 0:
        return_type = return_section[0].div.span.text

    return {title: {"syntax": syntax, "return_type": return_type}}



def main():
    base_url = "Any favorite DAX reference site"
    nav = get_navigation_tree(base_url)
    syntax_definitions = {}
    for categorytype in nav:
        syntax_definitions[categorytype] = {}
        if categorytype == "Function":
            for url in nav[categorytype]:
                try:
                    # Maybe not the fastest way. But at least it's clear what happens
                    syntax_definitions[categorytype].update(get_syntax_definitions(url))
                except (AttributeError, IndexError) as e:
                    print("Error on {}".format(url))
                    continue

    json.dump(syntax_definitions, open("syntax_definitions.json", "w"))
              
if __name__ == "__main__":
    main()
