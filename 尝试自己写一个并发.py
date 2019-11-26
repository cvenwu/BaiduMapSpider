from concurrent.futures import ThreadPoolExecutor
import concurrent
import requests
urls = [
            'https://www.baidu.com/',
            'http://www.sina.com/',
            'http://www.csdn.net/',
            'https://juejin.im/',
            'https://www.zhihu.com/'
]

def sppider(url):
    print('开始爬取：', url)
    return requests.get(url).text


def run():
    thread_pool = ThreadPoolExecutor(max_workers=4)
    futures = dict()
    for url in urls:
        future = thread_pool.submit(sppider, url)
        print(future)
        print(type(future))
        futures[future] = url

    for future in concurrent.futures.as_completed(futures):
        url = futures[future]
        try:
            data = future.result()
            print(type(data))
            print(data)
        except Exception as e:
            print('Run thread url (' + url + ') error. ' + str(e))
        else:
            print(url + 'Request data ok. size=' + str(len(data)))
    print('Finished!')



if __name__ == '__main__':
    run()