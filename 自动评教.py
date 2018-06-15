# -*- coding: utf-8 -*-
from requests import *
from re import *
import sys


class CourseLink:
    def __init__(self, wjbm, bpr, pgnr):
        self.wjbm = wjbm
        self.bpr = bpr
        self.pgnr = pgnr
        self.zgpj = "很棒的课程"


def getLt(url):
    html = sess.get(url).text
    return findall("<input type=\".+\" name=\"lt\" value=\"(.+)\" />", html)[0]


def Login(uname, passwd, lt):
    t = 10
    while t:
        html = sess.post("http://ids.xidian.edu.cn/authserver/login?service=http%3A%2F%2Fjwxt.xidian.edu.cn%2Fcaslogin.jsp",
                         data={
                             "username": uname,
                             "password": passwd,
                             "lt": lt,
                             "execution": "e1s1",
                             "_eventId": "submit"
                         }
                         ).text
        if "errorSpot" not in html:
            break

        t -= 1
        sys.exit("Login Failed!")


def DOIT():
    CourseLinks = []
    html = sess.get("http://jwxt.xidian.edu.cn/jxpgXsAction.do?oper=listWj&pageSize=300").text
    rows = findall("jxpgXsAction.do\?totalrows=([0-9]+)", html)
    if not rows:
        sys.exit("You have done these.")

    # for i in izip_longest(*[iter(findall('<td align="center">(.*)</td>', html))]*4):
    #    print ' '.join(i)
    for i in findall('<img name="(.+)" style=', html):
        info = i.split("#@")
        CourseLinks.append(CourseLink(info[0], info[1], info[-1]))
        print ' '.join(info)

    for link in CourseLinks:
        html = sess.post("http://jwxt.xidian.edu.cn/jxpgXsAction.do", data={
            "wjbm": link.wjbm,
            "bpr": link.bpr,
            "pgnr": link.pgnr,
            "oper": "wjShow"
        }).text

        datas = findall('<input type="radio" name="(.+)"\s*value="(.+1)">', html)
        datas.extend((("wjbm", link.wjbm), ("bpr", link.bpr),
                      ("pgnr", link.pgnr), ("zgpj", link.zgpj), ("xumanyzg", "zg"+findall("(DA_[0-9]+)", html)[0])))

        Post(datas)


def Post(datas):
    data = dict(datas)
    #print data
    print findall('alert\("(.+)"\);', sess.post(
        "http://jwxt.xidian.edu.cn/jxpgXsAction.do?oper=wjpg", data=data).text)[0]


uname = '你的学号'
passwd = '你的密码'
sess = session()

url = "http://jwxt.xidian.edu.cn/"
lt = getLt(url)
Login(uname, passwd, lt)

DOIT()
print "All Done!"
