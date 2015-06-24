#encoding=utf8
from mymusic.models import Song
from django.contrib.auth.models import User
from favourite.models import Favourite
import random

#返回歌曲的query_set
def get_random_song(n = 1):
    n = int(n)
#   return Song.objects.order_by('?')[:n]
    return [x.id for x in Song.objects.order_by('?')[:n]]

#返回歌曲的id的list
def get_similar_song(songid, n = 1):
    n = int(n)
    res = set()
    res = _get_similar_song(songid, 5, n, res)
    res = _get_similar_song(songid, 3, n, res)
    return random.sample(list(res), min(len(res), n))

#辅助函数
def _get_similar_song(songid, limit, n, res):
    if len(res) >= n:
        return res
    users = Favourite.objects.filter(song_id = songid, love__gte = limit)
    for u in users:
        res = res | set([s.song.id for s in Favourite.objects.filter(user_id = u.id, love__gte = limit).exclude(song_id = songid)])
        if len(res) >= n:
            break
    return res

#返回用户可能喜欢的歌曲的id
def get_similar_userlove(userid, n = 1):
    userlove = Favourite.objects.filter(user_id = userid).order_by('song_id')
    users = map(lambda x : similar_2user(userid, userlove, x), User.objects.all())
    users = [x[0] for x in sorted(users, key = lambda x : x[1])[:n]]
    res = list(get_users_love(users) - set([s.song.id for s in userlove]))
    return random.sample(res, min(n, len(res)))

def get_users_love(users):
    res = set()
    for u in users:
        res = res | set([s.song.id for s in Favourite.objects.filter(user_id = u.id, love__gte = 3)])
    return res;

#辅助函数，返回二者相似度
def similar_2user(usera, lovea, userb):
    loveb = list(Favourite.objects.filter(user_id = userb.id).order_by('song_id'))
    n = len(loveb)
    res = 0
    i = 0
    for song in lovea:
        while i < n and loveb[i].song.id < song.id:
            i += 1
        if i < n and loveb[i].song.id == song.id:
            res += (loveb[i].love - song.love) ** 2
        else:
            res += song.love ** 2
    return (userb, res)

#判断用户行为
def update_favourite(userid, songid, behave):
    try:
        val = Favourite.objects.get(user_id=userid, song_id=songid).love
    except Favourite.DoesNotExist:
        val = 0
    if behave == 'collected':
        val = 5
    if behave == 'shared':
        val = min(val, 4)
    if behave == 'full_listen':
        val = min(val + 1, 3)
    if behave == 'jump':
        val = max(val - 1, -3)
    if behave == 'blacklist':
        val = -5
    set_favourite(userid, songid, val)

#设置喜好程度（辅助函数）
def set_favourite(uid, sid, val):
    try:
        t = Favourite.objects.get(user_id=uid, song_id=sid)
        t.love = val
        t.save()
    except Favourite.DoesNotExist:
        t = Favourite(user_id = uid, song_id = sid, love = val)
        t.save()

#以下改动作者:dinosaur
#返回歌曲的object的list
def get_similar_song2(songid, n = 1):
    n = int(n)
    res = set()
    res = _get_similar_song2(songid, 5, n, res)
    res = _get_similar_song2(songid, 3, n, res)
    return random.sample(list(res), min(len(res), n))
    
#辅助函数
def _get_similar_song2(songid, limit, n, res):
    if len(res) >= n:
        return res
    users = Favourite.objects.filter(song_id = songid, love__gte = limit)
    for u in users:
        res = res | set([s.song for s in Favourite.objects.filter(user_id = u.id, love__gte = limit).exclude(song_id = songid)])
        if len(res) >= n:
            break
    return res
