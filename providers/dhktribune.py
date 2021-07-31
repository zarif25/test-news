import requests
from bs4 import BeautifulSoup


from . import Provider, Story


class DHKTribuneStory(Story):
  def __init__(self, soup, provider_name):
    self.name = soup.base_url
    self.__soup = soup
    self.__url = soup.base_url
    super().__init__(provider_name)

  def get_title(self):
    try:
      return self.__soup.h1.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)

  def get_summary(self):
    try:
      return self.__soup.find(class_="highlighted-content").p.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)


class DHKTribune(Provider):
  def __init__(self) -> None:
    super().__init__(
        url='https://www.dhakatribune.com/',
        story_class=DHKTribuneStory,
        name="Dhaka Tribune"
    )

  def get_story_soups(self) -> Story:
    # get soup of main page
    soup = BeautifulSoup(requests.get(self.url).text, 'lxml')

    # get urls recent stories
    h2_tags = soup.find(class_='just_in_news').find_all("h2")
    urls = ["https://www.dhakatribune.com"+h2_tag.a['href']
            for h2_tag in h2_tags]

    soups = []
    for url in urls:
      soup = BeautifulSoup(requests.get(url).text, 'lxml').find(
          class_="report-mainhead")
      soup.base_url = url
      soups.append(soup)
    return soups
