#运行环境win7
import requests
import re
import traceback
from bs4 import BeautifulSoup
import os

'''
从你喜欢的诗人的诗词中获得字频排序
version:0.0.1
author:Owen.Lee   weixin:leaqea
'''

def main():

	#获得诗人名字输入,及该诗人的首页地址
	poet = input('请输入你喜欢的诗人的名字: ')
	url = 'http://www.shicimingju.com/chaxun/zuozhe_list/' + poet
	#文件命名与输入有关
	file_path='d:/' + poet +'.txt'
	if os.path.exists(file_path):
		os.remove(file_path)
	try:
		#获取诗人主页地址
		r = requests.get(url)
		r.raise_for_status
		r.encoding = r.apparent_encoding
		soup = BeautifulSoup(r.text, 'html.parser')
		tag = soup.find_all('h3')[0]
		text = tag.a['href']
		poet_url = 'http://www.shicimingju.com' + text
		print('你选择的诗人为{},其首页为{}'.format(poet, poet_url))
	except:
		traceback.print_exc()
		print('好像没有这个人,请输入正确的诗人名字!')
		os.system('pause')

	#根据诗人首页信息,返回总作品数
	try:
		r = requests.get(poet_url)
		r.raise_for_status
		r.encoding = r.apparent_encoding
		soup = BeautifulSoup(r.text, 'html.parser')
		#获得该诗人作品总数
		tag = soup.title
		match = re.search(r'[1-9][\d]*', str(tag))
		total = int(match.group(0))
		print(poet + '的作品总数为{}'.format(total))
	except:
		traceback.print_exc()
		print('无法连接,请确保输入正确或重新调试程序!')


	#根据诗人创作总数和作品列表页面地址,返回其所有作品的地址列表
	print('正在解析作品地址……')
	url_list=[]
	#观察发现页面地址呈规律性变化,根据首页地址获得翻页地址列表
	poet_urls = [poet_url]
	if total % 40 > 0:
		scale = total // 40
	else:
		scale = total // 40 - 1
	for i in range(scale):
		poet_urls.append(poet_url[:42] + '_' + str(i+2) + '.html')
	#根据所有翻页地址列表,获得各个诗词内容对应的地址列表
	for url in poet_urls:
		try:
			r = requests.get(url)
			r.raise_for_status
			r.encoding = r.apparent_encoding
			soup = BeautifulSoup(r.text, 'html.parser')
			for tg in soup.find_all('h3'):
				if tg.a != None:
					url_list.append('http://www.shicimingju.com' + tg.a['href'])
		except:
			traceback.print_exc()
			continue

	#根据诗词地址列表,把诗词内容写入文件
	n = 0
	for url in url_list:
		try:
			r = requests.get(url)
			r.raise_for_status
			r.encoding = r.apparent_encoding
			soup = BeautifulSoup(r.text, 'html.parser')
			txt = soup.find_all(class_='shici-content')[0].text
			if txt != None:
				with open(file_path, 'a+') as f:
					f.write(txt)
					n += 1
			print('\r已写入{}首诗词'.format(n, end=''))
		except:
			traceback.print_exc()
			continue

	#根据诗词文本,返回字频列表排序结果
	ch_dict={}
	with open(file_path, 'r') as f:
		txt = f.read()
		f.close()
	ch_set = set(txt)
	for i in ['\n', ',', '。', '!', '！', '！' '?', '？' ' ', ' ', '，']:
		ch_set.discard(i)
	for ch in ch_set:
		ch_dict[ch] = 0
	#统计字频并存储于字典
	for ch in txt:
		if ch in ch_set:
			ch_dict[ch] += 1
	item_list = list(ch_dict.items())
	item_list.sort(key=lambda x:x[1], reverse=True)
	#打印前Num个字及字频
	Num = int(input('你想取多少个字: '))
	if Num > len(item_list):
		Num = len(item_list)
		print('对不起,最多可以取{}个字哦!'.format(Num))
	print('='*15)
	print('{:<5}{:>5}'.format('字','频数' ))
	print('='*15)
	for i in range(Num):
		ch, count = item_list[i]
		print('{:<5}{:>5}'.format(ch, count))
	os.system('pause')


if __name__ == '__main__':
	main()
