import requests


def downloadImg(url, path):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        open(path, 'wb').write(r.content)  # 将内容写入图片
        print(f"CODE: {r.status_code} download {url} to {path}")  # 返回状态码
        r.close()
        return path
    else:
        print(f"CODE: {r.status_code} download {url} Failed.")
        return "error"
