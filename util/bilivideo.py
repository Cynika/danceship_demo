# -*- coding: utf-8 -*-
# 作者:路人
# https://zhuanlan.zhihu.com/p/338744022
import requests
import re
import json
import ffmpeg


class BiliVideo:
    def __init__(self, bv_id, media_dir):
        # 输出视频文件夹,文件名
        self.media_dir = media_dir
        self.play_video_name = 'play.mp4'

        # 视频请求url
        self.bili_url = 'https://www.bilibili.com/video/' + bv_id
        # 视频资源url
        self.video_data = []

        # 请求头
        self.headers = {
            'Referer': 'https://www.bilibili.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'}

        # 串流
        self.video_format = "flv"
        self.server_url = "rtmp://127.0.0.1:1935/video"

    def send_request(self, url):
        response = requests.get(url=url, headers=self.headers)
        return response

    def get_video_data(self):
        """解析视频数据"""
        html_data = self.send_request(self.bili_url).text

        # 提取视频的标题
        try:
            title = re.findall('<span class="tit">(.*?)</span>', html_data)[0]
        except IndexError:
            try:
                title = re.findall('<title data-vue-meta="true">(.*?)</title>', html_data)[0]
            except IndexError as e:
                raise e

        # 提取视频对应的json数据
        json_data = re.findall('<script>window\.__playinfo__=(.*?)</script>', html_data)[0]
        # print(json_data)  # json_data 字符串
        json_data = json.loads(json_data)

        # 提取音频的url地址
        audio_url = json_data['data']['dash']['audio'][0]['backupUrl'][0]
        # 提取视频画面的url地址
        video_url = json_data['data']['dash']['video'][0]['backupUrl'][0]

        self.video_data = [title, audio_url, video_url]

        return title

    def video_download_merge(self):
        title, audio_url, video_url = self.video_data
        video_name = 'out.mp4'
        audio_name = 'out.mp3'
        # 请求数据
        # 正在请求音频数据
        audio_data = self.send_request(audio_url).content
        # 正在请求视频数据
        video_data = self.send_request(video_url).content

        with open(self.media_dir + audio_name, mode='wb') as f:
            f.write(audio_data)
            # 正在保存音频数据
        with open(self.media_dir + video_name, mode='wb') as f:
            f.write(video_data)
            # 正在保存视频数据

        # 视频合成开始
        v1 = ffmpeg.input(self.media_dir + video_name)
        a1 = ffmpeg.input(self.media_dir + audio_name)
        out = ffmpeg.output(v1, a1, self.media_dir + self.play_video_name, vcodec='copy', acodec='aac')
        out.run(overwrite_output=True)
        # 视频合成结束

    def video_stream(self):
        process = (
            ffmpeg
                .input(self.media_dir + self.play_video_name)
                .output(
                self.server_url,
                codec="libx264",  # use same codecs of the original video copy or libx264
                listen=1,  # enables HTTP server
                f=self.video_format)
                .global_args("-re")  # argument to act as a live stream
                .run()
        )


if __name__ == '__main__':
    try:
        bv_id = "BV1Xa411e7yk"
        bili_task = BiliVideo(bv_id, "G:\迅雷下载\\")
        bili_task.get_video_data()
        bili_task.video_download_merge()
    except Exception as e:
        raise e
