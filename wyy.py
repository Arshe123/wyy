import datetime
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# 获取数据
def Get_Data(url, rank_name):
    headers = {
        'Referer': 'https://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
    }
    response = requests.get(url, headers=headers)

    # 假设response.text是网页的HTML内容
    soup = BeautifulSoup(response.text, 'lxml')

    # 找到包含歌曲列表的div标签
    song_list_div = soup.find('ul', class_='f-hide')

    # 在这个div中找到所有的li标签，每个li标签代表一首歌曲
    songs_li= song_list_div.find_all('li')

    # 初始化一个空列表来存储歌曲信息
    songs = []

    # 获取歌手名称及排名变化
    singers_name, sings_rank_change = Get_Other_Data(soup)

    # 记录排名
    rank = 1
    # 遍历每个li标签，提取歌曲信息
    for song_li in songs_li:
        # 解析歌曲名字
        song_name = song_li.find('a').text.strip()

        # 解析歌曲链接
        song_url = song_li.find('a')['href']

        # 将歌曲信息添加到列表中
        songs.append({'歌曲排名': rank, '排名变化': sings_rank_change[rank - 1], '歌曲名称': song_name, '歌曲作者': singers_name[rank - 1], '歌曲链接': song_url})
        rank = rank + 1

    # 保存到csv文件
    # 获取当前日期
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # 格式化日期为YYYY-MM-DD
    path = '爬取数据/' + rank_name + '/' + current_date + rank_name + 'Top' + str(rank - 1) + '首歌曲.csv'
    # 将数组转换为DataFrame
    df_data = pd.DataFrame(songs, columns=['歌曲排名', '排名变化', '歌曲名称', '歌曲作者', '歌曲链接'])

    df_data.to_csv(path, encoding='utf-8', index=False)

    return songs

# 获取数据

# 获取歌手名称及排名变化
def Get_Other_Data(soup):
    # 解析数据
    sings_data_str = str(soup.find_all('textarea', id='song-list-pre-data'))

    # 使用切片去除开头和结尾的 <textarea> 和 </textarea>
    start_index = sings_data_str.find('>') + 1  # 找到第一个 '>'，并向后移动一个字符
    end_index = sings_data_str.rfind('</textarea>')  # 找到最后一个 '</textarea>' 的索引

    cleaned_data = sings_data_str[start_index:end_index]

    # 使用 json.loads() 将 JSON 字符串转换为 Python 对象
    sings_data = json.loads(cleaned_data)

    # 提取特定数据
    artists_data = []
    sings_rank_change = []
    for sing_data in sings_data:
        if 'artists' in sing_data:
            artists_data.extend(sing_data['artists'])
        try:
            sings_rank_change.append(str(int(sing_data['lastRank']) - int(sing_data['no']) + 1))
        except KeyError:
            sings_rank_change.append('new')

    # 存储歌手名字
    singers_name = []
    for artist_data in artists_data:
        singers_name.append(artist_data['name'])

    return singers_name, sings_rank_change


# 获取歌手名称及排名变化

if __name__ == '__main__':
    urls = [
        {
            'title': '飙升榜',
            'url': 'https://music.163.com/discover/toplist'
        },
        {
            'title': '新歌榜',
            'url': 'https://music.163.com/discover/toplist?id=3779629'
        },
        {
            'title': '原创榜',
            'url': 'https://music.163.com/discover/toplist?id=2884035'
        },
        {
            'title': '热歌榜',
            'url': 'https://music.163.com/discover/toplist?id=3778678'
        }
    ]

    # 获取数据
    data1 = Get_Data(urls[0]['url'], urls[0]['title'])
    data2 = Get_Data(urls[1]['url'], urls[1]['title'])
    data3 = Get_Data(urls[2]['url'], urls[2]['title'])
    data4 = Get_Data(urls[3]['url'], urls[3]['title'])
    # 获取数据
