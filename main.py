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


def get_chapter_summary(link: str, name: str) -> None:
    html_source = get_page_source(link)

    paragraphs = re.findall(r"<div class='summary-text readable highlightable-content non-paywall'>\n(.*)\n</div>\n",
                            html_source)

    with open('book_summary.html', 'a') as book_summary:
        book_summary.write(f"<center><b> {name} </center> </b>\n")
        for x in paragraphs:
            book_summary.write("<br>\n")
            book_summary.write(x + '\n')
            # print(x)
            book_summary.write("<br>\n")


def get_chapter_links(summary_link: str) -> list[str]:
    # midchild_links = [
    #     "https://www.litcharts.com/lit/midnight-s-children/book-1-the-perforated-sheet",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-1-mercurochrome",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-1-hit-the-spittoon",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-1-under-the-carpet",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-1-a-public-announcement",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-1-many-headed-monsters",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-1-methwold",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-1-tick-tock",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-the-fisherman-s-pointing-finger",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-snakes-and-ladders",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-accident-in-a-washing-chest",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-all-india-radio",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-love-in-bombay",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-my-tenth-birthday",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-at-the-pioneer-cafe",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-alpha-and-omega",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-the-kolynos-kid",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-commander-sabarmati-s-baton",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-revelations",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-movements-performed-by-pepperpots",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-drainage-and-the-desert",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-jamila-singer",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-2-how-saleem-achieved-purity",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-3-the-buddha",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-3-in-the-sundarbans",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-3-sam-and-the-tiger",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-3-the-shadow-of-the-mosque",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-3-a-wedding",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-3-midnight",
    #     "https://www.litcharts.com/lit/midnight-s-children/book-3-abracadabra",
    # ]

    page_source = get_page_source(summary_link)
    chapters_temp = re.findall(r"class=\"subcomponent tappable\" href=\"/lit/(.*)\">",
                               page_source)

    chapters = []
    for _ in chapters_temp:
        if "chapter" in _:
            chapters.append("https://www.litcharts.com/lit/" + _)

    return chapters


if __name__ == '__main__':
    summary_link = 'https://www.litcharts.com/lit/the-white-tiger/summary'
    chapter_links = get_chapter_links(summary_link)

    # add HTML,HEAD & BODY tag for initialization
    with open('book_summary.html', 'w+') as html_page:
        html_page.write("<!DOCTYPE html>\n<html>\n<body>\n")

    # write book summary first
    summary = get_book_summary(summary_link)
    with open('book_summary.html', 'a') as book_summary:
        book_summary.write(f"<center><b> Book Summary </center> </b>\n")
        book_summary.write("<br>\n")
        book_summary.write(summary + '\n')
        # print(summary)
        book_summary.write("<br>\n")

    # Fetch & Write the book chapter's summary in HTML format
    for link in chapter_links:
        chapter_name = link.split('/')[-1]
        print(f"fetching {chapter_name}")
        get_chapter_summary(link, chapter_name)

    # end the above HTML, HEAD, BODY tag.
    with open('book_summary.html', 'a') as html_page:
        html_page.write("</body>\n</html>")
