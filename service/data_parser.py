import asyncio

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker

from service.adding_tasks import initial_data_collection


headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Mobile Safari/537.36'
}


async def pulling_data_for_each_page(session_maker: sessionmaker) -> None:
    while True:
        url: str = "https://codeforces.com/problemset?order=BY_SOLVED_DESC"
        with requests.Session() as session:
            response = session.get(url=url, headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')
        pagination_count = int(soup.find_all('span', class_='page-index')[-1].text)

        with requests.Session() as session:
            for page in range(1, pagination_count + 1):
                response = session.get(
                    url=f'https://codeforces.com/problemset/page/{page}?order=BY_SOLVED_DESC&locale=ru',
                    headers=headers)
                soup = BeautifulSoup(response.text, 'lxml')

                articles_urls = soup.find_all('tr')[1:-2]  # Все строчки таблицы
                all_topics = set()

                for au in articles_urls:
                    number = au.find('a').text.strip()
                    name = au.find("div").text.strip()

                    complexity = au.find("span", class_="ProblemRating")
                    if complexity:
                        complexity = complexity.text.strip()
                    else:
                        complexity = "-1"

                    number_of_decisions = au.find('a',
                                                  title="Количество решивших задачу")
                    if number_of_decisions:
                        number_of_decisions = number_of_decisions.text.strip()
                    else:
                        number_of_decisions = "00"

                    topics = [i.text for i in au.find_all("a", class_="notice")]

                    for topic in topics:
                        all_topics.add(topic)

                    await initial_data_collection(number,
                                                  name,
                                                  int(complexity),
                                                  int(number_of_decisions[1:]),
                                                  topics,
                                                  session_maker=session_maker)
        await asyncio.sleep(3600)
