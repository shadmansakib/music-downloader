import re
import os
from requests import Session

from file import create_dir, write_binary_file
from soup import Soup
from utils import decode_url, remove_whitespace, encode_to_url
from music_album_urls import ALBUM_URLS

USER_AGENT = "Mozilla/5.0 (Android 7.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"

MUSIC_TITLE_REGEX = r'([\d\w\s\.-]* - [a-zA-Z0-9\s\(\)]+) [0-9\.]+ MB'

scrape_config = {
    'content_selector': 'a.list-group-item',
    'content_data': [
        {
            'name': 'music_title',
            'selector': '*',  # * = content_selector
            'get_as': 'text',  # get the text of 'a.list-group-item' tag
        },
        {
            'name': 'music_url',
            'selector': '*',  # * = content_selector
            'get_attr': 'href',  # get the href attribute from 'a.list-group-item' tag
        },
    ],
}


def main():
    session = Session()
    session.headers.update({'User-Agent': USER_AGENT})

    for url in ALBUM_URLS:
        try:
            album_name = decode_url(url.split('/')[-2])
        except Exception:
            album_name = None

        print("Downloading music from album '{}'\n".format(album_name))
        resp = session.get(url, timeout=30)
        if not resp.ok:
            print('Response code: {}'.format(resp.status_code))
            return
        html = resp.text

        soup = Soup(html)
        try:
            music_list = soup.scrape(scrape_config)
        except Exception:
            print("Can't download music from album {}. check URL and content selector.\n".format(album_name))
            continue

        for song in music_list:
            music_title = remove_whitespace(song.get('music_title', None)) \
                .replace(" (music.com.bd).mp3", "") \
                .replace("{} - ".format(decode_url(url.split('/')[-3])), "")

            music_url = 'https:{}'.format(encode_to_url(song.get('music_url'))).replace(".html", "")

            if not music_url.endswith('.mp3'):
                print("Skipping '{}' : not a music file".format(music_title))
                continue

            music_title = '{}.mp3'.format(re.search(MUSIC_TITLE_REGEX, music_title).group(1))

            create_dir(os.path.join('Downloads', album_name))

            print('>>> Downloading {}'.format(music_title))
            resp_music = session.get(music_url)
            if not resp_music.ok:
                print('    >>> Download failed : {}'.format(resp_music.status_code))
                continue

            music_path = os.path.join(album_name, music_title)
            write_binary_file(music_path, resp_music)
            print('    >>> {} downloaded'.format(music_title))
        # end loop: music_list
        print("\n>>> Album '{}' downloaded".format(album_name))
        print('----------------------------\n\n')
    # end loop : urls
    print('- Done -')


if __name__ == '__main__':
    main()
