# В данном кейсе для каждого следующего запроса нужно получить cmcontinue
# предыдущего запроса. По этой причине делать запросы можно только
# последовательно. Так как обработка результатов в данном примере почти не
# занимает времени, считаю рациональным применить синхронный подход (иначе
# можно конкурентно/параллельно выполнять обработку и запросы).

import csv
from typing import TypeAlias

import requests

API_URL = 'https://ru.wikipedia.org/w/api.php'
PARAMS = {
    'action': 'query',
    'format': 'json',
    'list': 'categorymembers',
    'cmprop': 'title',
    'cmtitle': 'Категория:Животные по алфавиту',
    'cmlimit': '500',
    'cmtype': 'page',
}
FILENAME = 'test/beasts.csv'

UrlParams: TypeAlias = dict[str, str]


def get_all_categorymembers(
    wiki_api: str, params: UrlParams
) -> list[str]:
    """
    Делает запрос к api сервису и возвращает список участников.

    Args:
        wiki_api (str): url адрес api сервиса.
        params (UrlParams): url параметры в виде словаря (dict[str, str]).

    Returns:
        list[str]: список title'ов, вычленных из ответа api сервиса.
    """
    members = []
    cmcontinue = None

    while True:
        if cmcontinue:  # id следующей страницы
            params['cmcontinue'] = cmcontinue

        response = requests.get(wiki_api, params=params)
        response.raise_for_status()
        response_json = response.json()

        for i in response_json['query']['categorymembers']:
            members.append(i['title'])
        cmcontinue = response_json.get('continue', {}).get('cmcontinue')

        if not cmcontinue:
            break

    return members


def count_prefix_matches(members: list[str]) -> dict[str, int]:
    """
    Подсчитывает, сколько раз слова начинаются на каждую букву.

    Args:
        members (list[str]): слова, учавствующие в подсчёте.

    Returns:
        dict[str, int]: результат в виде {letter:count}.
    """
    result = {}
    for title in members:
        first_letter = title[0].upper()
        result[first_letter] = result.get(first_letter, 0) + 1
    return result


def save_csv(data: dict[str, int], filename: str):
    """
    Сохраняет переданные данные в файл .csv

    Args:
        data (dict[str, int]): данные для сохранения
        filename (str): путь до файла
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for letter in sorted(data.keys()):
            writer.writerow([letter, data[letter]])


def main(api_url: str, url_params: UrlParams, save_to: str):
    members = get_all_categorymembers(
        wiki_api=api_url,
        params=url_params
    )
    save_csv(count_prefix_matches(members), filename=save_to)


if __name__ == '__main__':
    main(
        api_url=API_URL,
        url_params=PARAMS,
        save_to=FILENAME
    )
