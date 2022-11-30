
import requests
import re
import random
from lxml import etree
import time


def login(session):
    url = "http://acm.ocrosoft.com/login.php"
    # 账号密码登一遍看自己的data是啥
    data = {
        "user_id": "200110900240",
        "password": "zxyzxy",
        "submit":""
    }
    res = session.post(url=url,data=data)


def get_oj_pro_list(url, session):#获取需要标记的题目列表
    #fomat [[url,name]]
    res = session.get(url=url).text
    pro = re.findall(r'''<td class="left aligned"><a style="vertical-align: middle; "(.*?)">(.*?)</a>''', res, re.S)
    final = []
    for name in pro:
        final.append([name[0],name[1].replace('&nbsp;', ' ')])
    return final

def get_getkey(session,url):
    res = session.get(url=url).text
    getkey = re.findall(r'&getkey=(.*?)">编辑题目</a>',res,re.S)[0]
    return getkey

def get_postkey(getkey,pro_id,session):
    url = "http://acm.ocrosoft.com/admin/problem_edit.php?id="+pro_id+"&getkey="+getkey
    res = session.get(url=url).text
    postkey = re.findall(r'<input type=hidden name="postkey" value="(.*?)">', res, re.S)[0]
    return postkey

def get_ojdata(getkey,pro_id,session):
    url = "http://acm.ocrosoft.com/admin/problem_edit.php?id="+pro_id+"&getkey="+getkey
    res = session.get(url=url).text
    time_limit = re.findall(r'<input class="input input-mini" type=number min="0.001" max="300" step="0.001" name=time_limit size=20 value="(.*?)"', res, re.S)[0]
    mem_limit = re.findall(r'<input class="input input-mini" type=number min="1" max="1024" step="1" name=memory_limit size=20 value="(.*?)"',res, re.S)[0]
    description = re.findall(r'<textarea class="kindeditor" rows=13 name=description cols=80>(.*?)</textarea>',res, re.S)[0]
    # description = html.unescape(description)
    html = etree.HTML(description)
    description = html.xpath("string(.)")
    print(description)

    return [time_limit,mem_limit,description]


def find(pro_name,data):

    for pro in data:
        # print(pro[1].strip(),len(pro[1].strip()))
        # print(pro_name.strip(),len(pro_name.strip()))
        if (pro[2].strip() == pro_name.strip()):
            code_url = "https://codeforc.es/contest/"+pro[0].strip()[:-1]+"/status/"+pro[0].strip()[-1:]
            # return ["cf"+pro[0].strip()[-5:-2]+pro[0].strip()[-1:]+' '+pro[3].strip(),code_url]
            return [pro[1].strip(), code_url]

    return -1

def get_codeid(url,session):
    res = session.get(url).text
    id = re.findall(r'''<td>(.*?)</td>(.*?)<span class="submissionVerdictWrapper" submissionId="(.*?)" submissionVerdict="(.*?)"''', res, re.S)
    # print(res)
    # print(id)
    all_id = []
    for submit in id:
        # print(submit[0].strip())
        if (submit[3]=="OK" and (submit[0].strip()=="GNU C++11" or submit[0].strip()=="GNU C++14" or submit[0].strip()=="GNU C++17")):
            game = url.split('/')[-3]
            all_id.append("https://codeforc.es/contest/"+game+"/submission/"+submit[2].strip())
    if len(all_id) > 0:
        return all_id
    return -1

def get_ans(url):
    session = requests.session()
    res = session.get(url=url).text

    ans = re.findall(r'<pre id="program-source-text" class="prettyprint lang-cpp linenums program-source" style="padding: 0.5em;">(.*?)</pre>',res,re.S)
    if len(ans) > 0:
        return ans[0]
    else:
        return -1

def send(url,session,postkey,pro_id,pro_name,description,time,mem,getkey,source):
    data = {
        "problem_id": pro_id,
        "title": pro_name,
        "time_limit": time,
        "memory_limit": mem,


        "description": description,
        "input": "",
        "output": "",
        "sample_input": "",
        "sample_output": "",
        "hint": "",
        "spj": "0",
        "source": source,
        "postkey": postkey,
        "submit": "保存",
        "csrf": "A9tnlssMguFndziTvtkTcVdBfFE4XDAC",
    }


    res = session.post(url = "http://acm.ocrosoft.com/admin/problem_edit.php",data=data)

def submit(ans,pro_id,session):
    data = {
        "id": pro_id,
        "language": "1",
        "source": ans,
    }
    session.post(url="http://acm.ocrosoft.com/submit.php",data=data)

def HTML_parse(s):
    s = s.replace('&lt;', '<')
    s = s.replace('&nbsp;', ' ')
    s = s.replace('&gt;', '>')
    s = s.replace('&amp;', '&')
    s = s.replace('&quot;', '"')

    return s

if __name__ == '__main__':
    page_st = 63#想要爬取的题目在codeforces题目列表所在的页码区间
    page_ed = 63
    cf_session = requests.session()
    data = []#将爬取的信息缓存下来不需要对每一题爬一遍，防止访问过多
    while page_st < page_ed+1:
        print("正在缓存第" + (str)(page_st) + "页")
        url = "https://codeforc.es/problemset/page/" + (str)(page_st)
        res = cf_session.get(url=url).text
        html = etree.HTML(res)

        for i in range(2,102):
            tihao = html.xpath('/html/body/div[4]/div[4]/div[2]/div[2]/div[6]/table/tr['+str(i)+']/td[1]/a/text()')
            name = html.xpath('/html/body/div[4]/div[4]/div[2]/div[2]/div[6]/table/tr['+str(i)+']/td[2]/div[1]/a/text()')
            hard = html.xpath('/html/body/div[4]/div[4]/div[2]/div[2]/div[6]/table/tr['+str(i)+']/td[4]/span/text()')
            tags = html.xpath('/html/body/div[4]/div[4]/div[2]/div[2]/div[6]/table/tr['+str(i)+']/td[2]/div[2]/a/text()')
            temp = "cf" + tihao[0].strip()
            for j in hard:
                temp = temp + ' ' + j.strip()
            for j in tags:
                j = '_'.join(j.strip().split())
                temp = temp + ' ' + j
            data.append([tihao[0].strip(),temp, name[0].strip()])
        page_st = page_st + 1


    p = 23#zufe_oj上的页数
    pro_list_url = "http://acm.ocrosoft.com/problemset.php?page="+str(p)
    session = requests.session()
    login(session)#涉及到信息的post需要一个管理员账号   登录并保存对话
    pro_list = get_oj_pro_list(pro_list_url,session)#获取需要标记的题目列表
    print(pro_list)

    for pro in pro_list:
        # pro = ['href="problem.php?id=2873','【例6.5】活动选择']
        pro_id = pro[0][-4:]
        pro_name = pro[1].strip()
        data1 = find(pro_name, data)
        if (data1 == -1):
            print(pro_name)
            print("该题不是codeforces上的题或不在所在页码范围内")
            continue #没找到
        else:
            print("已找到对应题目")
        print("----------------------------------------------")

        pro_url = "http://acm.ocrosoft.com/problem.php?id="+pro_id
        getkey = get_getkey(session,pro_url) #getkey是后续post请求需要的参数

        tim,mem,description = get_ojdata(getkey, pro_id, session)
        postkey = get_postkey(getkey,pro_id,session)

        print("----------------------------------------------")
        source = data1[0]
        status_url = data1[1]
        print(status_url)

        #发送标签，标记题目的tag
        send("", session, postkey, pro_id, pro_name,description,tim,mem,getkey,source)
        print("tag添加成功")


        # 提交代码一次AC代码
        submit_url = get_codeid(status_url,cf_session)#返回c++的AC代码的提交id
        if(submit_url==-1):
            print("第一页提交页面找不到正确的c++代码")
            continue
        else:
            random.shuffle(submit_url)
            for id in submit_url:
                print(id)
                ans = get_ans(id)
                if (ans == -1):
                    continue
                ans = HTML_parse(ans)
                print(ans)
                submit(ans,pro_id,session)
                print("提交成功")
                time.sleep(8)#学校oj有提交频率限制
                break
