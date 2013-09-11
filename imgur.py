import requests
from random import randint
from bs4 import BeautifulSoup

def gen_url():
    """ Generate an imgur url using the randomly generated characters. """
    base = "http://www.imgur.com/r/funny"
    return base


def grab_image():
    """ Grab the image from imgur and write it to a file. """
    url = gen_url()
    req = requests.get(url)
    if req.status_code != 404:
        soup = BeautifulSoup(req.content)
        imgs = None
        for div in soup.find_all('div'):
            if 'class' in div.attrs:
                if div['class'] == ['post']:
                    imgs = div.find_all('img')
                    if randint(0, 1) == 1:
                        return imgs
        return imgs

