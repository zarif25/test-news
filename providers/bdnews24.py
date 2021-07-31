import requests
from bs4 import BeautifulSoup

from . import Provider, Story


class Bdnews24Story(Story):
  def __init__(self, soup, provider_name):
    self.__soup = soup
    super().__init__(provider_name)

  def get_title(self):
    try:
      return self.__soup.find(id='news-details-page').h1.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)

  def get_summary(self):
    try:
      return self.__soup.find(class_='article_lead_text').h5.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)


class Bdnews24(Provider):
  def __init__(self) -> None:
    super().__init__(
        url='http://bdnews24.com/',
        story_class=Bdnews24Story,
        name="bdnews24"
    )

  def get_story_soups(self):
    # get soup of main page
    soup = BeautifulSoup(requests.get(self.url).text, 'lxml')

    # get urls recent stories
    a_tags = soup.find(id='homepagetabs-tabs-2-2').find_all('a')
    urls = [a_tag['href'] for a_tag in a_tags]

    soups = []
    for url in urls:
      soup = BeautifulSoup(requests.get(url).text, 'lxml')
      soup.base_url = url
      soups.append(soup)

    return soups
