import scrapy
import re
import os
from googletrans import Translator
import string

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0',
           'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
           'Accept-Encoding':'gzip, deflate, br',
           'Accept-Language':'en-US,en;q=0.5',
           'content-type':'text/html;charset=UTF-8',
           'Referer': 'https://nvd.nist.gov/vuln/full-listing/2023/2'}

class testbase(scrapy.Spider):
    name = 'testbase'
    allowed_domains = ['nvd.nist.gov']

    start_urls = ['https://nvd.nist.gov/vuln/full-listing/2023/2/']
    download_delay = 10

    def parse(self, response):
        # 爬取主页面中的所有超链接
        links = response.css("div.row a::attr(href)").getall()
        if links is not None:
            if not links[0].startswith("https"):
                pass
            for i, link in enumerate(links):
                if "CVE" in link:
                    #if 'CVE' in link:
                    yield response.follow(link, self.parse_link, meta={'index': i + 1})
        


    def parse_link(self, response):
        
        contenthead = response.css("td span::text").get()#Detail CVE-20xx-xxxxx
        
        if contenthead is not None:
            
            contenthead = ''.join(contenthead)
            contenthead = contenthead.strip()
            contenthead = "".join(contenthead)
            
        else:
            contenthead = ""
        
         # 爬取文字内容#Description
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
        
        
        summary = response.css("div.row.bs-callout.bs-callout-success.cvssVulnDetail ::text").getall()#Severity 
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
        folder_name = 'CVE-2'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        
        # 写入txt文件中
        #filename = f'{response.meta["index"]}.txt'
        filename = response.url.split("/")[-1] + ".txt"
        file_path=os.path.join(folder_name, filename)
        with open(file_path, 'w') as f:
            f.write(contenthead+"\n"+content+"\n"+summary+"\n"+Othermess)
            
        '''
        for lines in f.readlines():
            ...
        '''
    
        
