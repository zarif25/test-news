import requests
from bs4 import BeautifulSoup


class Story:

  def __init__(self, provider_name: str, lang: str = 'en'):
    self.title = self.get_title()
    self.summary = self.get_summary()
    self.lang = lang
    self.provider_name = provider_name

  def is_complete(self):
    return (self.title and self.summary)

  def get_title(self) -> str:
    """
    Returns:
        The title of the story
    """
    raise NotImplementedError

  def get_summary(self) -> str:
    """
    Returns:
        The summary of the story
    """
    raise NotImplementedError

  def __eq__(self, other):
    return self.title == other.title

  def __repr__(self):
    return f"<Story: {self.title}>"


class Provider:
  def __init__(self, url: str, story_class: Story, name: str):
    self.url = url
    self.name = name
    self.story_class = story_class

  def __repr__(self):
    return f"<Provider: {self.name}>"

  def get_story_soups(self) -> list[BeautifulSoup]:
    raise NotImplementedError

  def get_stories(self) -> list[Story]:
    """
    Returns:
        A list of latest stories
    """
    soups = self.get_story_soups()

    stories: list[Story] = []
    for soup in soups:
      story = self.story_class(soup, self.name)
      stories.append(story)
    return stories


class RssStory(Story):
  def __init__(self, soup, provider_name, lang='en'):
    self.__soup = soup
    super().__init__(provider_name, lang=lang)

  def get_title(self):
    try:
      return self.__soup.title.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)

  def get_summary(self):
    try:
      return self.__soup.description.text.strip()
    except AttributeError as e:
      print("ERROR IN STORY: ", e)


class RssProvider(Provider):
  def __init__(self, url, name) -> None:
    super().__init__(url, RssStory, name)

  def get_story_soups(self):
    soup = BeautifulSoup(requests.get(self.url).text, 'lxml')
    return soup.find_all('item')
