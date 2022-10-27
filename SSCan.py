# -*- conding: utf-8 -*-
import pygubu
import tkinter as tk
import wascan
import threading

class ScanThread(threading.Thread):
    def __init__(self,app):
        threading.Thread.__init__(self)
        self.application = app

    def run(self):
        wascan.wascan().main(self.application.method,self.application.url,self.application.header,self.application.data,self.application.attack_type,self.application)

class ScanApp:
    def __init__(self, master):
        self.master = master
        self.builder = builder = pygubu.Builder()
        builder.add_from_file('scan.ui')
        master.title('Secure WebScan v1.0')

        # get Frame
        self.main_Frame = builder.get_object('main_Frame', master)
        self.sub_Frame_1 = builder.get_object('sub_Frame_1', master)
        self.sub_Frame_2 = builder.get_object('sub_Frame_2', master)
        self.sub_Frame_3 = builder.get_object('sub_Frame_3', master)
        self.request_Frame = builder.get_object('request_Frame', master)
        self.response_Frame = builder.get_object('response_Frame', master)

        # get Combo
        self.proto_Combo = builder.get_object('proto_Combo', master)
        self.proto_Combo['values'] = ('HTTP','HTTPS')
        self.attack_Combo = builder.get_object('attack_Combo', master)
        self.attack_Combo['values'] = ('0 : Finger Print','1 : Attacks','2 : Audit','3 : Brute Force', '4 : Disclosure', '5 : Full Scan')
             
        # Scroll Bar
        self.request_Text = builder.get_object('request_Text', master)
        self.request_xScroll = builder.get_object('request_xScroll', master)
        self.request_yScroll = builder.get_object('request_yScroll', master)
        self.request_Text['xscrollcommand'] = self.request_xScroll.set
        self.request_Text['yscrollcommand'] = self.request_yScroll.set
        self.request_xScroll['command'] = self.request_Text.xview
        self.request_yScroll['command'] = self.request_Text.yview

        self.response_Text = builder.get_object('response_Text', master)
        self.response_xScroll = builder.get_object('response_xScroll', master)
        self.response_yScroll = builder.get_object('response_yScroll', master)
        self.response_Text['xscrollcommand'] = self.response_xScroll.set
        self.response_Text['yscrollcommand'] = self.response_yScroll.set
        self.response_xScroll['command'] = self.response_Text.xview
        self.response_yScroll['command'] = self.response_Text.yview

        # Btn
        self.scan_Btn = builder.get_object('scan_Btn', master)        

        # Callback
        callbacks = {
                'on_scan_click': self.on_scan_click
            }
        builder.connect_callbacks(callbacks)

    def on_scan_click(self):
        self.requestMsg = self.request_Text.get("1.0",tk.END).strip()
        self.requestMsg = self.requestMsg.replace('\n','\r\n')
        self.requestMsg = self.requestMsg + "\r\n\r\n"
        self.proto = self.proto_Combo.get().strip()
        self.url = self.get_url(self.proto,self.requestMsg)
        self.header = self.get_headers_dict(self.requestMsg)
        self.data = self.get_body_data(self.requestMsg)
        self.attack_type = self.attack_Combo.get().strip()
        self.method = self.get_method(self.requestMsg)
        th = ScanThread(self)
        th.start()
        

    # Parse Body Data
    def get_body_data(self,requestMsg):
        datas = requestMsg.split('\r\n\r\n')
        return datas[1]
    
    # Parse Header Dict
    def get_headers_dict(self,requestMsg):
        datas = requestMsg.split('\r\n')
        request_Data = datas[0]
        datas.remove(datas[0])
        headers = {}
        for data in datas:
            if data != '':
                header = data.split(':',1)
                headers[header[0].strip()] = header[1].strip()
            else:
                break
        return headers

    # Parse Header
    def get_headers_scan(self,requestMsg):
        datas = requestMsg.split('\r\n')
        request_Data = datas[0]
        datas.remove(datas[0])
        headers = []
        for data in datas:
            if data != '':
                headers.append(data)
            else:
                break
        return ','.join(headers)
    # Get URL : HTTP(0), HTTPS(1)
    def get_url(self,proto,requestMsg):
        if proto == 'HTTP':
            full_url = 'http://'
        else:
            full_url = 'https://'
        full_url += self.get_headers_dict(requestMsg)['Host']
        datas = requestMsg.split('\r\n',1)
        reqData = datas[0].split()
        full_url += reqData[1]
        return full_url

    def get_method(self,requestMsg):
        datas = requestMsg.split('\r\n',1)
        return datas[0].split()[0]
        
if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(width=False, height=False)
    app = ScanApp(root)
    root.mainloop()


