from src.exceptions.exceptions import ErrorParseData, ErrorSaveJson
from src.controller.main_controller import Controller
from src.helper.parse import Parse
from src.helper.save_json import SaveJson
from src.s3.token import upload_to_s3

import asyncio
import pprint


async def main():
    url = 'https://id.wikipedia.org/wiki/Daftar_pemilihan_umum_kepala_daerah_di_Indonesia_2024'
    selector = await Parse.selector(url)

    # ! delete [1] if want to get all links
    urls = selector.xpath('//*[@id="mw-content-text"]/div[1]/ul/li')
    for url in urls:
        url_page_raw = url.xpath('.//a/@href').get()
        title_prov = url.xpath('ancestor::ul[1]/preceding-sibling::div[1]/h3/text()').get()

        if 'http:' not in url_page_raw:
            url_page = 'https://id.wikipedia.org/'+url_page_raw

            print(url_page)


        try:
            check_status = await Parse.get_status_code(url_page)
            if  check_status == 200:

                selector_page = await Parse.selector(url_page)
                deskripsi_halaman, potensial = await Controller.get_content(selector_page)

                title_page = selector_page.xpath('//*[@id="firstHeading"]/span/text()').get()


                data_calon = {}
                tabless = selector_page.xpath('//*[@id="mw-content-text"]/div[1]/table[@class="wikitable" and @style]')

                calons = []

                for table in tabless:
                    tbody = table.xpath('./tbody')


                    kandidat = tbody.xpath('./tr[1]/th/big/text()').get()

                    calon_rows = tbody.xpath('./tr[2]/th')
                    jabatan_rows = tbody.xpath('./tr[3]/td')
                    tahun_jabatan_rows = tbody.xpath('./tr[5]/td')

                    for i, calon in enumerate(calon_rows):
                        name = calon.xpath('./a/span/text() | ./span/text()').get()
                        link = calon.xpath('./a/@href').get()
                        detail_calon = {}

                        try:
                            if link:
                                if 'http' not in link:
                                    link = 'https://id.wikipedia.org' + link
                                detail_calon = await Controller.detail_calon_page(link)
                        except Exception as e:
                            print(e)

                        jabatan = jabatan_rows[i].xpath('./b/text()').get() if i < len(jabatan_rows) else None
                        tahun_jabatan_raw = tahun_jabatan_rows[i].xpath('./a/text() | ./text()').getall() if i < len(tahun_jabatan_rows) else []
                        tahun_jabatan = ' '.join(tahun_jabatan_raw)

                        if name is None:
                            detail_calon = {}

                        calons.append({
                            'kandidat': kandidat,
                            'name': name,
                            # 'link': link,
                            'jabatan': jabatan,
                            'deskripsi': tahun_jabatan,
                            'detail_calon': detail_calon
                        })

                data_calon['detail_calon'] = calons  

                data = {
                    'desc': deskripsi_halaman,
                    'calon': calons,
                    'potensial': potensial  
                }

                filename_json = f'{title_page}.json'.replace(' ','_').lower()
                data_name = 'Daftar pemilihan umum kepala daerah di Indonesia 2024'.lower().replace(' ','_')
                local_path = f'data/{title_prov.replace(' ','_').lower()}/{filename_json}'
                s3_path = f's3://ai-pipeline-raw-data/data/data_descriptive/wikipedia/{data_name}/{title_prov.replace(' ','_').lower()}/json/{filename_json}'

                try:
                    dj = SaveJson(url_page, title_prov, title_page, title_page, s3_path, data)
                    await dj.save_json_local(provinsi=title_prov, filename=filename_json)
                    print(f'Successfully saved JSON for {filename_json}')
                except Exception as e:
                    raise ErrorSaveJson(f'Error when saving JSON => {e}')
                
                try:
                    upload_to_s3(local_path, s3_path)
                except Exception as e:
                    raise e
                

            else:
                print(check_status == url_page)
        except Exception as e:
            raise ErrorParseData(e)

asyncio.run(main())