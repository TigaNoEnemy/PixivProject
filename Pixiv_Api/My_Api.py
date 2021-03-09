#!/usr/bin/env python3
from pixivpy3 import ByPassSniApi
import pixivpy3
import os
import shutil
from pixivpy3.utils import PixivError, JsonDict
import requests
import json
from urllib.parse import urlparse

import sys
sys.path.append('.')
from utils.Single_Instance import single_instance

import cgitb
cgitb.enable(format='text', logdir='log_file')

basestring = str

TIMEOUT = 10
FILE = '\033[37mMy_Api\033[0m'

@single_instance
class my_api(ByPassSniApi):
    """docstring for PixivApi"""
    _instance = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    # def _requests_call(self, method, url, timeout, headers={}, params=None, data=None, stream=False):
    #     """ requests http/https call for Pixiv API """
    #     headers.update(self.additional_headers)

    #     try:
    #         if (method == 'GET'):
    #             return self.requests.get(url, params=params, headers=headers, stream=stream, timeout=timeout, **self.requests_kwargs)
    #         elif (method == 'POST'):
    #             return self.requests.post(url, params=params, data=data, headers=headers, stream=stream, timeout=timeout, 
    #                                       **self.requests_kwargs)
    #         elif (method == 'DELETE'):
    #             return self.requests.delete(url, params=params, data=data, headers=headers, stream=stream, timeout=timeout, 
    #                                         **self.requests_kwargs)
    #     except requests.exceptions.Timeout:
    #         return

    #     except Exception as e:
    #         return

    #     raise PixivError('Unknow method: %s' % method)

    def download(self, url, prefix='', path=os.path.curdir, name=None, replace=False, fname=None,
                 referer='https://app-api.pixiv.net/'):
        """Download image to file (use 6.0 app-api)"""
        host_ip = {
            'i.pximg.net': self.pximg,
            's.pximg.net': self.default_head,
            }

        if fname is None and name is None:
            name = os.path.basename(url)
        elif isinstance(fname, basestring):
            name = fname

        if name:
            name = prefix + name
            img_path = os.path.join(path, name)

            if os.path.exists(img_path) and not replace:
                return False

        url_result = urlparse(url)
        host = url_result.netloc
        url = url.replace(f"https://{host}", host_ip[host])
        response = self.requests_call('GET', url, headers={'Referer': referer, 'Host': host}, stream=True)
        if name:
            with open(img_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
        else:
            shutil.copyfileobj(response.raw, fname)
        del response
        return True

    def follow_user(self, user_id, publicity='public'):
        url = f'{self.hosts}/v1/me/favorite-users.json'
        params = {
            'target_user_id': user_id,
            'publicity': publicity
        }
        r = self.auth_requests_call('POST', url, params=params)
        return self.parse_result(r)

    def disfollow_user(self, user_id, publicity='public'):
        url = f'{self.hosts}/v1/me/favorite-users.json'
        if isinstance(user_id, list): #type(user_id) == list:
            params = {'delete_ids': ",".join(map(str, user_id)), 'publicity': publicity}
        else:
            params = {'delete_ids': user_id, 'publicity': publicity}
        r = self.auth_requests_call('DELETE', url, params=params)
        return self.parse_result(r)

    def auth_requests_call(self, method, url, headers={}, params=None, data=None):
        headers['host'] = 'public-api.secure.pixiv.net'
        headers['Referer'] = 'http://spapi.pixiv.net/'
        headers['User-Agent'] = 'PixivIOSApp/5.8.7'
        headers['Authorization'] = 'Bearer %s' % self.access_token
        r = self.requests_call(method, url, headers, params, data)
        r.encoding = 'utf-8'  # Manually set the encoding due to #11 #18 #26, thanks @Xdynix
        return r

    def require_appapi_hosts(self, hostname="app-api.pixiv.net", timeout=3):
        """
        通过cloudflare的 DNS over HTTPS 请求真实的ip地址
        """
        url = "https://1.0.0.1/dns-query"   # 先使用1.0.0.1的地址
        params = {
            'ct': 'application/dns-json',
            'name': hostname,
            'type': 'A',
            'do': 'false',
            'cd': 'false',
        }

        try:
            response = requests.get(url, params=params, timeout=timeout)
        except Exception:
            # 根据 #111 的反馈，部分地区无法访问1.0.0.1，此时尝试域名解析
            url = "https://cloudflare-dns.com/dns-query"
            response = requests.get(url, params=params, timeout=timeout)

        # 返回第一个解析到的IP
        hosts = "https://" + response.json()['Answer'][0]['data']
        return hosts

    # 自定义
    def cache_pic(self, url, path, file_name, replace=False, timeout=TIMEOUT):
        # 缓存图片
        print(f"{FILE}: 缓存：{url}")
        isSuccess = self.download(url=url, path=path, name=str(file_name), replace=replace)#, timeout=timeout)
        return {'isSuccess': isSuccess}

    def get_image_size(self, url, Range=None, timeout=TIMEOUT):
        referer='https://app-api.pixiv.net/'
        headers = {'Referer': referer, 'host': 'i.pximg.net'}
        url = url.replace('https://i.pximg.net', self.pximg)

        #断点续传， range指定下载范围
        #had_size = 0
        if Range:
            headers['Range'] = Range
            #had_size = int(Range.replace('bytes=', '').replace('-', ''))

        self.requests_kwargs.update({"timeout": timeout})
        headers['host'] = 'i.pximg.net'
        url = url.replace('https://i.pximg.net', self.pximg)

        print(f"{FILE}: image_size: {url}")
        print(f"{FILE}: {headers}")
        try:
            response = self.requests_call('GET', url, headers=headers, stream=True)
        except pixivpy3.utils.PixivError as e:
            print(f'{FILE}: {e}')
            return {'isSuccess': False}

        self.requests_kwargs.pop('timeout', None)
        dict_headers = dict(response.headers)
        print(f"{FILE}: {dict_headers}")
        print(f"{FILE}: Content-Range: {dict_headers.get('Content-Range', None)}")
        image_size0 = dict_headers.get('Content-Range', 'bytes 196608-4982434/-1')
        image_size = int(image_size0.split('/')[-1])
        image_size1 = dict_headers.get('Content-Length', -1)
        image_size2 = dict_headers.get('content-length', -1)
        image_size3 = dict_headers.get('Content-length', -1)
        image_size4 = dict_headers.get('content-Length', -1)

        #image_size = max(map(int, [image_size1, image_size2, image_size3, image_size4]))
        # if image_size != -1:
        #     image_size += had_size
        print(f"{FILE}: <{url}>\033[41m{image_size}\033[0m")
        return {'image_size': int(image_size), 'isSuccess': True, 'response': response}

    def download_has_size_pic(self, response, output_file):
        with open(output_file, 'ab') as f:
            try:
                shutil.copyfileobj(response.raw, f)
            except:
                return {'isSuccess': False}
        return {'isSuccess': True}

    def parse_json(self, json_str):
        data = json.loads(json_str, object_hook=JsonDict)

        if 'illusts' in data:
            data['illusts'] = [i for i in data['illusts'] if 'R-18' not in str(i['tags'])]

        elif 'user_previews' in data:
            for i in range(len(data['user_previews'])):
                data["user_previews"][i]['illusts'] = [j for j in data["user_previews"][i]['illusts'] if 'R-18' not in str(j['tags'])]

        return data


if __name__ == '__main__':
    from utils.Process_Token import login_info_parser

    cfg = login_info_parser()
    info = cfg.get_token()

    l = my_api()
    l.pximg = l.require_appapi_hosts("i.pximg.net")
    l.hosts = l.require_appapi_hosts("public-api.secure.pixiv.net")
    l.default_head = l.require_appapi_hosts("s.pximg.net")
    #print(l.default_head)
    res = l.auth(refresh_token=info['token'])
    print(res)
    print('down')
    l.cache_pic('https://i.pximg.net/c/600x1200_90_webp/img-master/img/2016/04/07/07/36/15/56232434_p0_master1200.jpg', path='.', file_name='test')

    print('complete')