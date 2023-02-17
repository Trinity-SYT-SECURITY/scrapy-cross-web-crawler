import scrapy
import re
import os
from googletrans import Translator
import string

#headers請按F12後Network底下查看詳細資訊，每台機器不太一樣
headers = {'User-Agent': ' ',
           'Accept':' ',
           'Accept-Encoding':' ',
           'Accept-Language':' ',
           'content-type':' ', 
           'Referer': ''}#要爬蟲的主網頁連結

class scrapytxt(scrapy.Spider):#class名稱必須跟檔名一樣
    name = 'scrapytxt'
    allowed_domains = [' ']#網站的domain

    start_urls = [' '] #起始的主網頁連結
    download_delay = 10

    def parse(self, response):
        # 爬取主页面中的所有超連結
        links = response.css("div.row a::attr(href)").getall()
        if links is not None:
            if not links[0].startswith("https"):
                pass
            for i, link in enumerate(links):
                if "CVE" in link:
                    #if 'CVE' in link:
                    yield response.follow(link, self.parse_link, meta={'index': i + 1})
        


    def parse_link(self, response):
        
        contenthead = response.css("td span::text").get() #跨網站後的元素定位，這裡需要根據要爬取的網站在跨連結爬取後你要的元素位置，每個網站位置不同response.css後都要自行更改
        
        if contenthead is not None:
            
            contenthead = ''.join(contenthead)
            contenthead = contenthead.strip()
            contenthead = "".join(contenthead)
            
        else:
            contenthead = ""
        
       
        content = response.css('div.col-lg-9.col-md-7.col-sm-12  p::text').getall()
        if content is not None:
            
            #content = str(content)
            content = ''.join(content) # 將內容轉成字串
                                 
            #del the content while appear the some html grammar and newline symbol
            content = re.sub(r'<.*?>', '', content)
            content = content.replace('\r', '')
            content = content.replace('\n', '') # 去除\n
            content = content.replace('\t', '') # 去除\t
            content = re.sub(r'\s{3,}','',content)
            content = content.strip()
            #content = "".join( x for x in content if x not in characters)
            content = "".join(content)
        else:
            content=""
        
        
        summary = response.css("div.row.bs-callout.bs-callout-success.cvssVulnDetail ::text").getall()
        if summary is not None:
            
            summary =  ''.join(summary)
            summary = re.sub(r'<.*?>', '', summary)
            summary = summary.replace('\r', '')
            summary = summary.replace('\n', '') # 去除\n
            summary = summary.replace('\t', '') # 去除\t
            summary = re.sub(r'\s{3,}','',summary)
            summary = summary.strip()
            summary = "".join(summary)
        else:
            summary = ""
               
        Othermess = response.css("div.row.col-sm-12 ::text").getall()
        if Othermess is not None:
            Othermess = "\n".join(Othermess)
            
            Othermess = re.sub(r'<.*?>', '', Othermess)
            Othermess = Othermess.replace('\r', '')
            Othermess = Othermess.replace('\n', '') # 去除\n
            Othermess = Othermess.replace('\t', '') # 去除\t
            Othermess = re.sub(r'\s{3,}','',Othermess)
            Othermess = Othermess.strip()
            #content = "".join( x for x in content if x not in characters)
            Othermess = "".join(Othermess)
        else:
            Othermess = ""
             
        
        ###########################################
        folder_name = ' '#在於你爬下來資料後想要創建的目錄名稱，這會保存所有爬取結果
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        
        # 寫入文件
        #filename = f'{response.meta["index"]}.txt'
        filename = response.url.split("/")[-1] + ".txt"
        file_path=os.path.join(folder_name, filename)
        with open(file_path, 'w') as f:
            f.write(contenthead+"\n"+content+"\n"+summary+"\n"+Othermess)
            
     
        
