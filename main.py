import requests
import os
if __name__ == '__main__':
    print("Version: 0.1\n")
    getImageUrl = 'https://kd.nsfc.gov.cn/api/baseQuery/completeProjectReport'  #获取文献图片地址信息
    getInfoUrl = 'https://kd.nsfc.gov.cn/api/baseQuery/conclusionProjectInfo/'  #获取文献信息
    data = {    #请求数据
        'id': '',
        'index': 0
    }
    headers = {  # 请求头,ua
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.42'
    }
    minn = 0    #搜索最小值
    maxn = 120  #搜索最大值
    while True:
        paper_id = input("输入文献ID：")
        if paper_id == '0':
            break
        data['id'] = paper_id
        print("正在获取文献信息...\t预计耗时15秒")
        for t in range(7):                      #使用二分法搜索
            ave = int((minn + maxn) / 2)
            data['index'] = ave
            response = requests.post(url=getImageUrl, headers=headers, data=data)
            json_ids = response.json()
            judge = requests.get(url='https://kd.nsfc.gov.cn' + json_ids['data']['url'])
            if judge.text[0] != '<':
                #flag = True
                minn = ave
            else:
                #flag = False
                maxn = ave
            #if flag:
            #else:
        response.close()
        judge.close()
        info = requests.get(url=getInfoUrl+paper_id,headers=headers)
        jsonInfo = info.json()
        print("\n\n文献名称：\t《"+jsonInfo['data']['projectName']+"》")
        print("项目负责人：\t"+jsonInfo['data']['projectAdmin'])
        print("依托单位：\t"+jsonInfo['data']['dependUnit'])
        print("总页数：  \t"+str(ave-2)+"\n\n")
        info.close()
        i = int(input("输入抓取的起始页："))#1
        j = int(input("输入抓取的终止页："))#100
        if os.path.exists('Image'):
            if os.path.exists(os.path.join('Image',jsonInfo['data']['projectName'])):
                print("目录已存在")
            else:
                os.mkdir('Image/' + jsonInfo['data']['projectName'])
                print("目录创建成功")
        else:
            os.mkdir('Image')
            os.mkdir('Image/'+jsonInfo['data']['projectName'])
            print("目录创建成功")
        if i != 1: i += 1
        for x in range(i,j+2):
            data['index'] = x
            response = requests.post(url=getImageUrl, headers=headers, data=data)
            json_ids = response.json()
            response.close()
            imageUrl = 'https://kd.nsfc.gov.cn'+json_ids['data']['url']
            imgResp = requests.get(url=imageUrl,headers=headers)
            image = imgResp.content
            ImgName = str(x-1)+'.png'
            with open(os.path.join(os.getcwd(),'Image',jsonInfo['data']['projectName'],ImgName), 'wb') as file:
                file.write(image)
            imgResp.close()
            print('Index =', x-1, 'END')
        print('Complete!\n')