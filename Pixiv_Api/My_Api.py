#!/usr/bin/env python3
from pixivpy3 import ByPassSniApi
import pixivpy3
import os
import shutil
from pixivpy3.utils import PixivError
import requests
from urllib.parse import urlparse

import sys
sys.path.append('.')
from utils.Single_Instance import single_instance

import cgitb
cgitb.enable(format='text', logdir='log_file')

basestring = str

TIMEOUT = 5

@single_instance
class my_api(ByPassSniApi):
    """docstring for PixivApi"""
    _instance = None
    def __init__(self):
        super().__init__()


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
        url = f'{self.public_api}/v1/me/favorite-users.json'
        params = {
            'target_user_id': user_id,
            'publicity': publicity
        }
        r = self.auth_requests_call('POST', url, params=params)
        return self.parse_result(r)

    def disfollow_user(self, user_id, publicity='public'):
        url = f'{self.public_api}/v1/me/favorite-users.json'
        if type(user_id) == list:
            params = {'delete_ids': ",".join(map(str, user_id)), 'publicity': publicity}
        else:
            params = {'delete_ids': user_id, 'publicity': publicity}
        r = self.auth_requests_call('DELETE', url, params=params)
        return self.parse_result(r)

    def auth_requests_call(self, method, url, headers={}, params=None, data=None):
        self.require_auth()
        if hasattr(self, 'public_api'):
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
        print(f"缓存：{url}")
        isSuccess = self.download(url=url, path=path, name=str(file_name), replace=replace)#, timeout=timeout)
        return {'isSuccess': isSuccess}

    def get_image_size(self, url, Range=None, timeout=TIMEOUT):
        referer='https://app-api.pixiv.net/'
        headers = {'Referer': referer}

        #断点续传， range指定下载范围
        if Range:
            headers['Range'] = Range

        self.requests_kwargs.update({"timeout": timeout})
        headers['host'] = 'i.pximg.net'
        url = url.replace('https://i.pximg.net', self.pximg)

        print(f"image_size: {url}")
        try:
            response = self.requests_call('GET', url, headers=headers, stream=True)
        except pixivpy3.utils.PixivError:
            return {'isSuccess': False}

        self.requests_kwargs.pop('timeout', None)
        image_size1 = dict(response.headers).get('Content-Length', -1)
        image_size2 = dict(response.headers).get('content-length', -1)
        image_size3 = dict(response.headers).get('Content-length', -1)
        image_size4 = dict(response.headers).get('content-Length', -1)

        image_size = max(map(int, [image_size1, image_size2, image_size3, image_size4]))
    
        return {'image_size': int(image_size), 'isSuccess': True, 'response': response}

    def download_has_size_pic(self, response, output_file):
        with open(output_file, 'ab') as f:
            try:
                shutil.copyfileobj(response.raw, f)
            except:
                return {'isSuccess': False}
        return {'isSuccess': True}


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