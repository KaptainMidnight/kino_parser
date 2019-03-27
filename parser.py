from bs4 import BeautifulSoup as bs
import requests


class Parser:
    headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)"
    }

    def __init__(self):
        self.get_html()

    def get_html(self):
        url = "https://www.afisha.ru/chelyabinsk/schedule_cinema/"
        with requests.Session() as session:
            response = session.get(url, headers=self.headers)
        return response.text

    def parse_html(self, html):
        urls = []
        soup = bs(html, 'lxml')
        main_div = soup.find_all('div', {'class': 'cards-grid__item'})
        for i in main_div:
            try:
                name = i.find('h3', {'class': 'card__title'}).text
                rating = i.find('div', {'class': 'rating-static__item'}).text
                href = i.find('a', {'class': 'card__link'}).get('href')
                links = {
                    'href': f'https://www.afisha.ru{href}',
                    'name': name,
                    'rating': rating
                }
                urls.append(links)
            except:
                continue
        for j in urls:
            with requests.Session() as session:
                response = session.get(j['href'], headers=self.headers)
                if response.status_code == 200:
                    soup = bs(response.text, 'lxml')
                    print(soup.prettify())
                    div_schedule = soup.find_all('div', {'class': 'object__block-content'})
                    print(div_schedule)
                    for k in div_schedule:
                        cinema = k.find('a', {'class': 'unit__movie-name__link'}).text
                        print(cinema)
def main():
    bot = Parser()
    html = bot.get_html()
    result = bot.parse_html(html)
    return result


if __name__ == '__main__':
    print(main())
