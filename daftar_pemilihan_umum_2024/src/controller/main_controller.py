from src.helper.parse import Parse

import requests
import pprint
import json
from bs4 import BeautifulSoup

class Controller:

    async def get_content(selector):
        deskripsi_halaman_raw = selector.xpath('//*[@id="mw-content-text"]/div[1]/p//text()').getall()
        deskripsi_halaman = ' '.join(deskripsi_halaman_raw)


        all_potential = []
        potensials = selector.xpath('/html/body/div[2]/div/div[3]/main/div[3]/div[3]/div[1]/ul[1]/li')
        for orang in potensials:
            nama = orang.xpath('./a[1]/text()').get()
            if nama == None:
                nama = orang.xpath('./text()').get()

            jabatan = orang.xpath('./a[2]/text()').get()
            if jabatan == None:
                jabatan = orang.xpath('./text()').get()

            if nama is not None or jabatan is not None:
                all_potential.append({'nama': nama, 'jabatan': jabatan})


        return deskripsi_halaman, all_potential
    


    async def detail_calon_page(link_calon_page:str):
        response = requests.get(link_calon_page)
        if response.status_code == 200:

            selector = await Parse.selector(link_calon_page)

            head = selector.xpath('/html/head/title/text()').get()
            title = selector.xpath('/html/body/div[2]/div/div[3]/main/header/h1/span/text()').get()


            data_infobox = {}
            response = requests.get(link_calon_page)
            soup = BeautifulSoup(response.content, 'html.parser')

            #  ! mnengambil dari table infobox
            infobox = soup.find('table', class_='infobox vcard')
            if infobox:
                rows = infobox.find_all('tr')
                
                for row in rows:
                    key = None
                    value = None
                    
                    if row.th and row.td:
                        key = row.th.get_text(" ", strip=True)
                        value = row.td.get_text(" ", strip=True)
                    elif row.th:
                        key = row.th.get_text(" ", strip=True)
                        if row.th.a:
                            value = row.th.a.get_text(strip=True)
                    elif row.td:
                        if row.td.a:
                            key = row.td.a.get_text(strip=True)
                            value = row.td.get_text(" ", strip=True)

                    if key:
                        key = key.lower().replace(' ', '_')
                        if 'sunting' not in key and value:  
                            data_infobox[key] = value
            # ! akhir dari mengambil infobox


            # ! mengambil content pada page 
            content = {}
            deskripsi_content_raw = selector.xpath('//*[@id="mw-content-text"]/div[1]/p//text()').getall()
            deskipsi_content = ' '.join(deskripsi_content_raw)

            content['desc'] = deskipsi_content
            div_subtitles = selector.xpath('//div[@class="mw-heading mw-heading2"]')

            for div in div_subtitles:
                heading_text = div.xpath('./h2/text()').get()
                
                if heading_text:
                    heading_text = heading_text.strip().replace(' ', '_').lower()
                    
                    if heading_text == 'sumber':
                        continue
                    
                    next_sibling = div.xpath('./following-sibling::*[1]')
                    second_sibling = div.xpath('./following-sibling::*[2]')

                    uls = None

                    if next_sibling and next_sibling.xpath('name()').get() == 'ul':
                        uls = next_sibling
                    
                    elif second_sibling and second_sibling.xpath('name()').get() == 'ul':
                        uls = second_sibling

                    
                    if uls is not None:
                        all_li_texts = []
                        
                        li_elements = uls.xpath('.//li')
                        for li in li_elements:
                            text_raw = li.xpath('.//text()').getall()
                            text = ' '.join(text_raw).strip()
                            if text:
                                all_li_texts.append(text)
                        
                        if all_li_texts:
                            content[heading_text] = all_li_texts

            detail_calon = {
                'title' : title,
                'infobox': data_infobox,
                'content' : content
            }

            return detail_calon
        else:
            return {}
