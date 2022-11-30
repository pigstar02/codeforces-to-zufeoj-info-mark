# codeforces-to-zufeoj-info-mark

## 快速开始
- 下载main.py，安装需要的包
- 131行和132行设置查找题目在cf所在页码范围
- 156行设置需要添加tag和AC代码的zufe-oj代码
- 运行


## 函数介绍
- login
  修改tag需要管理员权限，先账号登录保存会话
- get_oj_pro_list
  从题目列表中获取本页所有题目的名字和链接
- get_getkey
  由于后台的题目管理的修改请求只能覆盖不能添加，需要将原先的题目信息爬取保存，还有最后提交数据都需要用到getkey参数
- get_postkey
  返回最后提交数据需要用到postkey
- get_ojdata
  根据题目id和getkey获取题面信息
- find
  输入zufe-oj上的题目名字，在从codeforces上缓存的data中查找并返回本题所有提交代码status页面
- get_codeid
  返回本页所有通过的C++代码的详情链接，如果不存在则返回-1
- get_ans
  输入代码详情链接，返回完整的代码
- send
  把所有题面信息还有新加的tag打包成一个post请求发送
- submit
  在zufe-oj上提交代码
- HTML_parse
  爬取的代码属于html格式，其中包括很多转义字符，将其转化为正确的字符
