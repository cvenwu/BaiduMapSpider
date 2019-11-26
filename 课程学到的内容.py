# python使用线程池进行编程
import concurrent
from concurrent import futures  # 做多线程和多进程编程
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

# 线程池
## 为什么需要线程池
## 主线程中可以获取某一个线程的状态或者某一个任务的状态以及返回值
## 当一个线程完成的时候我们主线程也可以立即知道
## futures可以让多线程和多进程编码一致

import time
def get_html(times):
    time.sleep(times)  # 休眠

    print('get page {} success'.format(times))
    return times



def main():
    executor = ThreadPoolExecutor(max_workers=2)

    # 提交任务
    ## 通过submit函数提交执行的函数到线程池中
    ## submit是非阻塞的，将会立即返回
    task1 = executor.submit(get_html, (3))  # 第一个参数是函数名称，第二个参数是函数的参数
    task2 = executor.submit(get_html, (10))  # 会有一个返回结果

    # done 方法用于判定某个任务是否完成
    print(task1.done())  # 判断这个函数是否执行成功
    time.sleep(4)
    print(task2.done())

    # result 方法得到task执行的返回结果
    print(task2.result())
    print(task1.result())

    # 将某一个任务cancel掉， 在submit返回的对象上进行操作，
    task2.cancel()  # 只有在还没有执行的时候cancel掉


# 获取已经成功的task的返回as_completed 是一个生成器
executor = ThreadPoolExecutor(max_workers=4)
urls = [10, 10, 10]
all_tasks = [executor.submit(get_html, url) for url in urls]

# 异步运行
# for future in as_completed(all_tasks):  # 返回已经完成的future
    # data = future.result()  # 得到执行的结果
    # print(data)

# 通过executor获取已经完成的task， 会按照urls中的元素的顺序执行，但也是并发只是会等待
# for data in executor.map(get_html, urls):  # 直接返回执行的结果
#     print(data)

