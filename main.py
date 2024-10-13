import requests
import os
from difflib import get_close_matches
from concurrent.futures import ThreadPoolExecutor

from pydub import AudioSegment
from pydub.utils import which

# 设置 ffmpeg 和 ffprobe 的路径
AudioSegment.converter = which("ffmpeg")  # 确保 pydub 使用系统中的 ffmpeg
AudioSegment.ffprobe = which("ffprobe")   # 确保 pydub 使用系统中的 ffprobe

# 请求的 URL
url = 'http://www.6002255.com/'

# 请求头信息
headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'zh-CN,zh;q=0.9',
    'connection': 'keep-alive',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'UM_distinctid=19283a25275a7d-0b815f031e5a1b-26001051-384000-19283a252762e05; CNZZDATA1279348389=615993390-1728785306-https%253A%252F%252Fwww.baidu.com%252F%7C1728785321',
    'origin': 'http://www.6002255.com',
    'referer': 'http://www.6002255.com/?name=%E8%A7%81%E4%B8%80%E9%9D%A2%E5%B0%91%E4%B8%80%E9%9D%A2&type=netease',
    'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'x-requested-with': 'XMLHttpRequest'
}

# 设置下载路径，确保music文件夹存在
music_folder = 'music'
if not os.path.exists(music_folder):
    os.makedirs(music_folder)  # 如果文件夹不存在，则创建它

# 文件来存储没有找到的歌曲名称
not_found_file = 'not_found_songs.txt'
unplayable_file = 'unplayable_songs.txt'  # 新增用于记录无法播放的歌曲

# 初始化一个锁，确保多线程时文件写操作安全
from threading import Lock
file_lock = Lock()

# 检查歌曲是否可以播放
def is_song_playable(file_path):
    try:
        # 尝试加载音频文件
        song = AudioSegment.from_file(file_path, format="mp3")
        return True  # 如果成功加载，文件可以播放
    except CouldntDecodeError:
        return False  # 无法加载文件，文件可能已损坏

# 下载并检查 MP3 文件
def download_and_check_song(song_name, song_url, file_path):
    # 下载歌曲文件
    download_response = requests.get(song_url)

    # 检查下载请求是否成功
    if download_response.status_code == 200:
        # 将内容写入文件
        with open(file_path, 'wb') as f:
            f.write(download_response.content)
        print(f"歌曲 '{song_name}' 已成功下载到 {file_path}")

        # 检查歌曲是否可播放
        if is_song_playable(file_path):
            return True
        else:
            print(f"歌曲 '{song_name}' 无法播放。")
            return False
    else:
        print(f"歌曲 '{song_name}' 下载失败，状态码: {download_response.status_code}")
        return False

# 下载函数
def download_song(song_name):
    # 请求的数据，更新歌曲名称
    data = {
        'input': song_name,
        'filter': 'name',
        'type': 'netease',
        'page': '1'
    }

    # 发起 POST 请求
    response = requests.post(url, headers=headers, data=data)

    # 检查响应状态码
    if response.status_code == 200:
        response_data = response.json()

        if response_data['code'] == 200 and response_data['data']:
            # 获取返回的歌曲列表中的名称
            song_titles = [song['title'] for song in response_data['data']]
            
            # 进行近似匹配
            matched_titles = get_close_matches(song_name, song_titles, n=len(song_titles), cutoff=0.6)  # 近似匹配
            
            for matched_title in matched_titles:
                # 找到匹配的歌曲
                for song in response_data['data']:
                    if song['title'] == matched_title:
                        first_song_url = song['url']
                        first_song_name = song['title']

                        # 定义文件保存的路径
                        file_name = f"{first_song_name}.mp3"  # 用歌曲名作为文件名
                        file_path = os.path.join(music_folder, file_name)

                        # 下载并检查 MP3 文件
                        if download_and_check_song(first_song_name, first_song_url, file_path):
                            return  # 如果找到可播放的歌曲，结束函数
                        else:
                            print(f"尝试下载其他匹配项...")

            # 如果所有匹配项都无法播放，将其记录到 unplayable_songs.txt
            with file_lock:
                with open(unplayable_file, 'a', encoding='utf-8') as uf:
                    uf.write(f"{song_name}\n")
            print(f"所有匹配项都无法播放，已记录 '{song_name}' 到 {unplayable_file}")

        else:
            print(f"没有找到歌曲 '{song_name}' 的相关信息。")
            # 将没有找到的歌曲写入 not_found_songs.txt
            with file_lock:
                with open(not_found_file, 'a', encoding='utf-8') as nf:
                    nf.write(f"{song_name}\n")
    else:
        print(f"请求歌曲 '{song_name}' 信息失败，状态码: {response.status_code}")
        # 将没有找到的歌曲写入 not_found_songs.txt
        with file_lock:
            with open(not_found_file, 'a', encoding='utf-8') as nf:
                nf.write(f"{song_name}\n")

# 读取音乐列表文件并启动多线程下载
with open('music.txt', 'r', encoding='utf-8') as file:
    song_names = [line.strip() for line in file]

# 使用 ThreadPoolExecutor 实现多线程下载
with ThreadPoolExecutor(max_workers=5) as executor:  # 你可以根据需要调整 max_workers 的数量
    executor.map(download_song, song_names)
