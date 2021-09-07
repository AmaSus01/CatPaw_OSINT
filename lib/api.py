import random
from .local import *
from .location import get_geolocation
import requests

cookie = {"sessionid": 'write here your session id from instagram account'}
resp_js = None
is_private = False
total_uploads = 12
location_list = []


def get_page(username):
    global resp_js
    session = requests.session()
    session.headers = {'User-Agent': random.choice(useragent)}
    resp_js = session.get(f'https://www.instagram.com/{username}/?__a=1', cookies=cookie).json()
    return resp_js


banner_i()


def user_info(username):
    global total_uploads, is_private
    js = get_page(username)
    try:
        js = js['graphql']['user']
    except KeyError:
        print('No such account exists ')
        exit(1)
    if js['is_private'] != False:
        is_private = True

    if js['edge_owner_to_timeline_media']['count'] > 12:
        pass
    else:
        total_uploads = js['edge_owner_to_timeline_media']['count']

    userinfo = {
        'username': js['username'],
        'user id': js['id'],
        'name': js['full_name'],
        'followers': js['edge_followed_by']['count'],
        'following': js['edge_follow']['count'],
        'posts img': js['edge_owner_to_timeline_media']['count'],
        'posts vid': js['edge_felix_video_timeline']['count'],
        'reels': js['highlight_reel_count'],
        'bio': js['biography'].replace('\n', ', '),
        'external url': js['external_url'],
        'profile img': urlshortner(js['profile_pic_url_hd']),
    }

    print(f"{su}{ye} user info")
    for key, val in userinfo.items():
        if val == None or val == False:
            pass
        else:
            print(f"  {gr}%s : {wh}%s" % (key, val))
    print("")
    return username


def highlight_post_info(all_data, photo_number):
    postinfo = {}
    user = all_data['graphql']['user']
    node = user['edge_owner_to_timeline_media']['edges'][photo_number]['node']
    if node['location'] == None:
        pass
    else:
        info = {
            'location': node['location']['name'],
        }
        location_list.append(info['location'])
        postinfo['info'] = info
    return postinfo


def range_ob(data):  # Common json data and range control init
    user = data['graphql']['user']
    range_control = user['edge_owner_to_timeline_media']['count']
    return range_control


def location_info(username):  # get location info
    if is_private != False:
        print(f"{fa}{gr} cannot use -l for private accounts !\n")
        sys.exit(1)
    posts = []
    data = get_page(username)
    for x in range(total_uploads):
        if x == range_ob(data) + 1:
            return
        else:
            posts.append(highlight_post_info(data, x))
    get_location_info(location_list)


def get_location_info(local_list):  # condition of location work
    if len(local_list) <= 3:
        print('Not enough information to get life location of this person')
    else:
        location_dict = {i:local_list.count(i) for i in local_list}
        keywithmaxval(location_dict)
    return

def keywithmaxval(location_dict):  # return the key with the max value
    value = list(location_dict.values())
    key = list(location_dict.keys())
    place = (key[value.index(max(value))])
    get_geolocation(place)
    return


