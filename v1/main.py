import os
import json
import requests
import csv
# Global Parameters
config = None  # config class object
station_information = {}  # store station information as dict


# 开发者API, 一旦配额超限用于更换API
aks = ["YwjKptDEqMrzW0YpHWvy3yvVMGhyQqpi", "2H7iph6CzNbPOxUFzaGwRs9gwaVrSgqN", "luVuXu9Zgg5lsiwS019nE1E85iujpsap", "16uXHj0MG0ezMOMoLVfbh5TkkOFAdk1P"]
# 交通方式
routetype = ["walking", "driving", "riding", "transit"]
# 输入坐标类型，默认bd09ll
coordtype = ["bd09ll", "wgs84", "bd09mc", "gcj02"]


class Config(object):
    def __init__(self, config_file='./config.json'):
        '''
        读取config配置文件
        :param config_file: 配置文件所在的路径已经名称，用于打开配置文件
        '''
        f = open(config_file, 'r', encoding='utf-8')
        config_file_content = json.load(f)
        self.input_file_path = config_file_content['input_file_path']
        self.input_file_name = config_file_content['input_file_name']
        print(type(self.input_file_path), self.input_file_name)  # first type is str


def get_input_information(input_file_path, input_file_name):
    '''
    将输入文件的信息进行整理
    :param input_file_path: 输入文件的路径
    :param input_file_name: 输入文件的名字
    :return: 返回一个字典，键是每个站点的名字，值是一个列表(由站点id,站点Y坐标,站点X坐标组成)
    '''
    global station_information
    input_information_list = []
    with open(os.path.join(input_file_path, input_file_name), 'r', encoding='gb18030') as f:
        for line_content in f.readlines()[1:]:
            line_content = line_content.strip('\n')
            input_information_list.append(line_content)  # 去掉读取到的每行末尾换行符
            # 将每行信息开始分割, 分割后分别对应站点id, 站点名称，站点Y坐标，站点X坐标
            station_id, station_name, station_Y_position, station_X_position = line_content.split(',')
            # 以站点名称为键，站点id, 站点Y坐标，站点X坐标为值组成一个字典
            station_information[station_name] = [station_id, station_Y_position, station_X_position]


def url_concact(origin_point_position, destin_point_position, ak):
    '''
    拼接url字符串
    对应的API文档请查看：http://lbsyun.baidu.com/index.php?title=webapi/direction-api-v2
    :param origin_point_position: 起点的坐标, origin=22.62345900,114.04741900
    :param destin_point_position: 终点的坐标, destination=22.49430500,113.92633200
    :return:
    '''
    print(origin_point_position, destin_point_position)
    base_url = 'http://api.map.baidu.com/direction/v2/transit?output=json'
    # &origin=22.623459,114.047419&destination=22.629272,113.820643&ak=2H7iph6CzNbPOxUFzaGwRs9gwaVrSgqN&
    last_url = '&coord_type=bd09ll&page_size=1&tactics_incity=4'
    origin_point_position = '&origin=' + origin_point_position
    destin_point_position = '&destination=' + destin_point_position
    # 最后拼接成的url

    final_url = base_url + origin_point_position + destin_point_position + '&ak=' + ak + last_url
    print('最后拼接成的url:', final_url)
    return final_url

# 第一行是可以运行的
# http://api.map.baidu.com/direction/v2/transit?output=json&origin=22.57371800,114.10437200&destination=22.62123000,114.11716400&ak=YwjKptDEqMrzW0YpHWvy3yvVMGhyQqpi&coord_type=bd09ll&page_size=1&tactics_incity=4
# http://api.map.baidu.com/direction/v2/transit?output=json&origin=113.820643,22.629272&destination=113.820643,22.629272&YwjKptDEqMrzW0YpHWvy3yvVMGhyQqpi&coord_type=bd09ll&page_size=1&tactics_incity=4


def spider():
    '''
    爬取对应的url参数
    :param url: 要爬取的url地址
    :return: 返回爬取到的经过字典化处理的内容
    '''
    global aks
    global station_information
    count_total = 0
    for origin_key, origin_value in station_information.items():
        count_temp = 0
        for dest_key, dest_value in station_information.items():
            count_temp += 1
            count_total += 1
            print('共需要{}次爬取，已累计爬取{}次'.format(len(station_information) * len(station_information), count_total))
            print('本轮爬取共{}次,开始第{}次爬取 {}------>{})'.format(len(station_information), count_temp, origin_key, dest_key))
            # 将起点和终点坐标传递过去，拼接url
            website_url = url_concact(origin_value[2] + ',' + origin_value[1], dest_value[2] + ',' + dest_value[1], aks[0])
            # 爬取网页内容并将其转换为字典
            website_url_content_dict = json.loads(requests.get(website_url).text)
            # website_url_content_dict['status'] 是 int类型
            if website_url_content_dict['status'] != 0:
                print('{}------>{}爬取失败'.format(origin_key, dest_key))
                # 将要爬取的Url以及站点名称写入到failure文件中
                with open('failure.txt', 'a+') as f:
                    writer = csv.writer(f)
                    writer.writerow([origin_key, dest_key, website_url])
            else:
                if len(website_url_content_dict['result']['routes']) != 0:
                    # 说明有返回结果
                    # 得到距离
                    distance = website_url_content_dict['result']['routes'][0]['distance']
                    # 得到持续时间
                    duration = website_url_content_dict['result']['routes'][0]['duration']
                    with open('results.csv', 'a+') as f:
                        writer = csv.writer(f)
                        writer.writerow([origin_value[0], origin_key, dest_value[0], dest_key, str(distance), str(duration)])
                else:
                    # 网页有返回，但是返回的result下的routes为空
                    ## 例如：http://api.map.baidu.com/direction/v2/transit?output=json&origin=22.629272,113.820643&destination=22.629272,113.820643&ak=YwjKptDEqMrzW0YpHWvy3yvVMGhyQqpi&coord_type=bd09ll&page_size=1&tactics_incity=4
                    with open('null.txt', 'a+') as f:
                        writer = csv.writer(f)
                        writer.writerow([origin_key, dest_key, website_url])


def initialize():
    global config
    global station_information
    config = Config()
    get_input_information(config.input_file_path, config.input_file_name)
    spider()


if __name__ == '__main__':
    initialize()
    print(station_information)
