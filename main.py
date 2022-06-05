#!/usr/bin/env python3

import re
import requests


def get_page_source(link: str) -> str:
    source = requests.get(link.strip())
    return source.text


def get_book_summary(summary_link: str) -> str:
    paragraphs = re.findall(r"""<div class='readable highlightable-content'> <p class="plot-text">(.*)</div>\n""",
                            get_page_source(summary_link))
    summary = paragraphs[0]
    return summary


def get_chapter_summary(link: str, name: str, book_file_name: str) -> None:
    html_source = get_page_source(link)

    paragraphs = re.findall(r"<div class='summary-text readable highlightable-content non-paywall'>\n(.*)\n</div>\n",
                            html_source)

    with open(book_file_name, 'a') as book_summary:
        book_summary.write(f"<center><b> {name} </center> </b>\n")
        for x in paragraphs:
            book_summary.write("<br>\n")
            book_summary.write(x + '\n')
            # print(x)
            book_summary.write("<br>\n")


def get_chapter_links(summary_link: str) -> list[str]:
    page_source = get_page_source(summary_link)
    chapters_temp = re.findall(r"class=\"subcomponent tappable\" href=\"/lit/(.*)\">",
                               page_source)

    chapters = []
    for _ in chapters_temp:
        if "chapter" in _:
            chapters.append("https://www.litcharts.com/lit/" + _)

    return chapters


def get_summary_link():
    link = input("Enter book Page link on litcharts\n"
                 "it should be something like 'https://www.litcharts.com/lit/the-white-tiger/'\n\n")

    if link.endswith('/'):
        return link.strip() + "summary"
    else:
        return link.strip() + "/summary"
    
    
if __name__ == '__main__':
    # summary_link = 'https://www.litcharts.com/lit/the-white-tiger/summary'
    summary_link = get_summary_link()

    chapter_links = get_chapter_links(summary_link)
    book_title: str = re.findall(r"<title>(.*) Plot Summary \| LitCharts</title>", get_page_source(summary_link))[0]
    book_title = book_title.replace(" ", "_")
    book_file_name = book_title + ".html"

    print(f"Saving '{book_title}' to '{book_file_name}'\n")
    # add HTML,HEAD & BODY tag for initialization
    with open(book_file_name, 'w+') as html_page:
        html_page.write("<!DOCTYPE html>\n<html>\n<body>\n")

    # write book summary first
    summary = get_book_summary(summary_link)
    with open(book_file_name, 'a') as book_summary:
        book_summary.write(f"<center><b> Book Summary </center> </b>\n")
        book_summary.write("<br>\n")
        book_summary.write(summary + '\n')
        # print(summary)
        book_summary.write("<br>\n")

    # Fetch & Write the book chapter's summary in HTML format
    for link in chapter_links:
        chapter_name = link.split('/')[-1]
        print(f"fetching {chapter_name}")
        get_chapter_summary(link, chapter_name, book_file_name)

    # end the above HTML, HEAD, BODY tag.
    with open(book_file_name, 'a') as html_page:
        html_page.write("</body>\n</html>")

    print(f"Summary saved in '{book_file_name}' in project dir. ")
