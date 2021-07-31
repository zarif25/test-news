import requests
from bs4 import BeautifulSoup

from . import Provider, Story


class IttefaqStory(Story):
  def __init__(self, soup, provider_name):
    self.name = soup.base_url
    self.__soup = soup
    super().__init__(provider_name, lang='bn')

  def get_title(self):
    try:
      return self.__soup.find(id='dtl_hl_block').h1.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)

  def get_summary(self):
    try:
      return self.__soup.find(id='dtl_content_block').strong.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)


class Ittefaq(Provider):
  def __init__(self) -> None:
    super().__init__(
        url='https://www.ittefaq.com.bd/',
        story_class=IttefaqStory,
        name="ইত্তেফাক"
    )

  def get_story_soups(self) -> Story:
    # get soup of main page
    soup = BeautifulSoup(requests.get(self.url).text,
                         'lxml').find(class_='latest-news')

    # get urls recent stories
    a_tags = soup.find_all('a')
    urls = [a_tag['href'] for a_tag in a_tags]

    soups = []
    for url in urls:
      soup = BeautifulSoup(requests.get(url).text,
                           'lxml').find(class_='body-content')
      soup.base_url = url
      soups.append(soup)

    return soups
