import requests
import os

getImageUrl = 'https://kd.nsfc.gov.cn/api/baseQuery/completeProjectReport'  #获取文献图片地址信息
getInfoUrl = 'https://kd.nsfc.gov.cn/api/baseQuery/conclusionProjectInfo/'  #获取文献信息
data = {    #请求数据
    'id': '',
    'index': 0
}
headers = { 
    'Accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Dnt': '1',
    'Host': 'kd.nsfc.gov.cn',
    'Referer': '',
    'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Gpc': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.9'
}


print("Files will be saved in " + os.getcwd() + '\\Image\n')

while True:

    minn = 0
    maxn = 120

    paper_id = input("输入文献ID：")
    if paper_id == '0':
        break

    data['id'] = paper_id
    print("正在获取文献信息...\t预计耗时15秒")

    while minn < maxn:              #look for the last page
        ave = (minn + maxn + 1) // 2
        data['index'] = ave
        response = requests.post(url = getImageUrl, headers = headers, data = data)
        json_ids = response.json()
        judge = requests.get(url = 'https://kd.nsfc.gov.cn' + json_ids['data']['url'], headers = headers)
        if judge.ok:
            minn = ave
        else:
            maxn = ave - 1
    response.close()
    judge.close()

    info = requests.get(url = getInfoUrl + paper_id, headers = headers)
    jsonInfo = info.json()
    print("\n\n文献名称：\t《" + jsonInfo['data']['projectName'] + "》")
    print("项目负责人：\t" + jsonInfo['data']['projectAdmin'])
    print("依托单位：\t" + jsonInfo['data']['dependUnit'])
    print(f"总页数：  \t{minn - 1}\n\n")
    info.close()

    if os.path.exists('Image'):
        if os.path.exists(os.path.join('Image', jsonInfo['data']['projectName'])):
            print("目录已存在")
        else:
            os.mkdir('Image/' + jsonInfo['data']['projectName'])
            print("目录创建成功")
    else:
        os.mkdir('Image')
        os.mkdir('Image/' + jsonInfo['data']['projectName'])
        print("目录创建成功")
    
    i = int(input("输入抓取的起始页："))
    j = int(input("输入抓取的终止页："))
    if i != 1:      # download the cover when i == 1
        i += 1
    for x in range(i, j + 2):
        data['index'] = x

        print('Downloading index ', x - 1)

        response = requests.post(url = getImageUrl, headers = headers, data = data)
        json_ids = response.json()
        response.close()
        imageUrl = 'https://kd.nsfc.gov.cn' + json_ids['data']['url']
        imgResp = requests.get(url = imageUrl,headers = headers)
        if imgResp.ok:
            image = imgResp.content
            ImgName = str(x - 1) + '.png'
            with open(os.path.join(os.getcwd(), 'Image', jsonInfo['data']['projectName'], ImgName), 'wb') as file:
                file.write(image)
            print('successful\n')
        else:
            print('failed\n')
        imgResp.close()
        
    print('Complete!\n')