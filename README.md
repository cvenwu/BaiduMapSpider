# BaiduMapSpider
线路爬取

## 使用说明
1. clone项目到本地
2. 修改项目目录下的config.json 
    - 将input_file_path参数修改为输入文件(地铁站以及对应坐标的csv文件)所在的路径
    - 将input_file_name参数修改为输入文件(地铁站以及对应坐标的csv文件)对应的文件名字(.csv文件)
3. 配置项目编译器：Python3.5+
4. 运行项目下的main.py文件

### 需要的模块
- os
- json
- requests
- csv
- concurrent
- time
- concurrent

## Recent News
### v1: 使用concurrent的并发线程池进行多线程爬取

### v1_1: 添加newline='' 防止在爬取数据为None是出现空行的情况

```python
with open('results.csv', 'a+', newline='') as f:
with open('null.txt', 'a+', newline='') as f:
```