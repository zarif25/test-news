import requests
from bs4 import BeautifulSoup

from . import Provider, Story


class BnTribuneStory(Story):
  def __init__(self, soup, provider_name):
    self.name = soup.base_url
    self.__soup = soup
    self.__url = soup.base_url
    super().__init__(provider_name, lang='bn')

  def get_title(self):
    try:
      return self.__soup.h1.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)

  def get_summary(self):
    try:
      return self.__soup.article.p.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)


class BnTribune(Provider):
  def __init__(self) -> None:
    super().__init__(
        url='https://www.banglatribune.com/archive/',
        story_class=BnTribuneStory,
        name="বাংলা ট্রিবিউন"
    )

  def get_story_soups(self) -> Story:
    # get soup of main page
    soup = BeautifulSoup(requests.get(self.url).text,
                         'lxml').find(class_='summery_view')

    # get urls recent stories
    a_tags = soup.find_all('a')
    urls = ["https:"+a_tag['href']
            for a_tag in a_tags if 'link_overlay' in a_tag.attrs['class']][:10]

    soups = []
    for url in urls:
      soup = BeautifulSoup(requests.get(url).text, 'lxml')
      soup.base_url = url
      soups.append(soup)

    return soups
