#!/usr/bin/python3
# -*- coding:utf-8 -*-

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib
import re
import time
from Core import Ulits

data = {'msg': '', 'code':0}
host = ('0.0.0.0', 58760)

class Resquest(BaseHTTPRequestHandler):
    def do_GET(self):
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        if '?' in self.path :
            # queryString = urllib.parse.unquote(self.path.split('?',1)[1])
            # params = urllib.parse.parse_qs(queryString)        
            params = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(self.path).query))
        else :
            params = {}

        # 添加邮箱
        if  '/add' in self.path:
            try:
                if ('email' in params) == False :
                    data['msg'] = '请输入邮箱'
                elif Ulits.is_valid_email(params['email']) == False :
                    data['msg'] = '邮箱不合法'
                else :
                    data['msg'] = '订阅成功,疫情有最新动态第一时间推送到您的邮箱\n\r邮件内支持退订'
                    data['code'] = 1
                    email = params['email']
                    db = Ulits.DBTool()
                    dataIsAdd = db.executeQuery("SELECT * FROM emails WHERE email=?" ,(email,))
                    dataIsAdd = dataIsAdd.fetchall()
                    if len(dataIsAdd) == 0 :
                        if db.executeUpdate("INSERT INTO emails (email, create_time) \
                            VALUES (?,?)", [(email, time.time())]) == False :
                            data['msg'] = '添加失败,请稍后重试'
                            data['code'] = 0
                    elif dataIsAdd[0][5] == 0 :
                        if db.executeUpdate("UPDATE emails SET is_notice = 1 WHERE id =?", [(dataIsAdd[0][0],)]) == False :
                            data['msg'] = '添加失败,请稍后重试'
                            data['code'] = 0
                    db.close()
                self.wfile.write(json.dumps(data).encode())
            except Exception as identifier:
                print(identifier)
                self.send_error(404)

        # 取消订阅
        elif '/cancel' in self.path:
            try:
                if ('code' in params) :
                    aes = Ulits.USE_AES()
                    email = aes.decodebytes(params['code'])
                    if Ulits.is_valid_email(email):
                        db = Ulits.DBTool()
                        dataIsAdd = db.executeQuery("SELECT * FROM emails WHERE email=?" ,(email,))
                        dataIsAdd = dataIsAdd.fetchall()
                        if len(dataIsAdd) > 0:
                            db.executeUpdate("UPDATE emails SET is_notice = 0 WHERE id =?", [(dataIsAdd[0][0],)])
                            data['code'] = 1
                            data['msg'] = '操作成功'
                        else:
                            data['msg'] = '邮箱不存在'
                        db.close()
                    else :
                        data['msg'] = '邮箱不合法'
                else:
                    data['msg'] = '标识符不存在'

                if ('html' in params) :
                    htmlFp = open('Template/cancel-html.html','r',encoding='utf-8')
                    html = htmlFp.read()
                    htmlFp.close()
                    html = html.replace('{{text}}', str(data['msg']))
                    self.wfile.write(html.encode())
                else :
                    self.wfile.write(json.dumps(data).encode())
            except Exception as identifier:
                print(identifier)
                self.send_error(404)
        else :
            htmlFp = open('Template/index.html','r',encoding='utf-8')
            html = htmlFp.read()
            htmlFp.close()
            self.wfile.write(html.encode())
                

if __name__ == '__main__':
    server = HTTPServer(host, Resquest)
    print("Starting server, listen at: %s:%s" % host)
    server.serve_forever()