from .common import InfoExtractor
from ..compat import compat_str
from ..utils import (
    parse_duration,
    urljoin,
)
import base64
import re
import urllib.parse


# This JavaScript code translated to Python below:

# $.each(vidsnfo, function(pid, src) {
# 	var tmp = src.split("/");
# 	tmp[1]+= "8" + "/" + boo(ssut51(tmp[6]),ssut51(tmp[7]));
# 	tmp = preda(tmp);
# 	var src = tmp.join("/");
# 	if ($('.combo_mode[data-postid="'+pid+'"]').length) $('.combo_mode[data-postid="'+pid+'"]').attr('data-vidsrc',src);
# 	if ($('.player_el_nc[data-postid="'+pid+'"]').length) $('.player_el_nc[data-postid="'+pid+'"]').attr('src',src);
# 	if ($('[itemprop="contentUrl"]').length) $('[itemprop="contentUrl"]').attr('content',src);
# });
# function preda(arg){
# 	arg[5]-= parseInt(ssut51(arg[6]))+parseInt(ssut51(arg[7]));
# 	return arg;
# }
# function ssut51(arg){
# 	var str = arg.replace(/[^0-9]/g,'');
# 	var sut = 0;
# 	for (var i = 0; i < str.length; i++) {
# 	sut += parseInt(str.charAt(i), 10);
# 	}
# 	return sut;
# }
# function boo(ss,es){
# 	var b = btoa(ss + "-" + window.location.host + "-" + es);
# 	return b.replace(/\+/g, '-').replace(/\//g, '_').replace(/\=/g, '.');
# }


def preda(arg):
    arg[5] = str(int(arg[5]) - (ssut51(arg[6]) + ssut51(arg[7])))
    return arg

def ssut51(arg):
    str_val = re.sub(r'[^0-9]', '', arg)
    sut = 0
    for char in str_val:
        sut += int(char)
    return sut

def boo(ss, es, host):
    combined_string = f"{ss}-{host}-{es}"
    encoded_bytes = base64.b64encode(combined_string.encode('utf-8'))
    encoded_string = encoded_bytes.decode('utf-8')
    return encoded_string.replace('+', '-').replace('/', '_').replace('=', '.')


class YourPornIE(InfoExtractor):
    _VALID_URL = r'https?://(?:www\.)?sxyprn\.com/post/(?P<id>[^/?#&.]+)'
    _TESTS = [{
        'url': 'https://sxyprn.com/post/57ffcb2e1179b.html',
        'md5': '6f8682b6464033d87acaa7a8ff0c092e',
        'info_dict': {
            'id': '57ffcb2e1179b',
            'ext': 'mp4',
            'title': 'md5:c9f43630bd968267672651ba905a7d35',
            'thumbnail': r're:^https?://.*\.jpg$',
            'duration': 165,
            'age_limit': 18,
        },
        'params': {
            'skip_download': True,
        },
    }, {
        'url': 'https://sxyprn.com/post/57ffcb2e1179b.html',
        'only_matching': True,
    }]

    def _real_extract(self, url):
        video_id = self._match_id(url)

        webpage = self._download_webpage(url, video_id)

        parts = self._parse_json(
            self._search_regex(
                r'data-vnfo=(["\'])(?P<data>{.+?})\1', webpage, 'data info',
                group='data'),
            video_id)[video_id].split('/')

        hostname = urllib.parse.urlparse(url).hostname
        parts[1] += "8" + "/" + boo(ssut51(parts[6]), ssut51(parts[7]), hostname)
        video_url = urljoin(url, '/'.join(preda(parts)))

        title = (self._search_regex(
            r'<[^>]+\bclass=["\']PostEditTA[^>]+>([^<]+)', webpage, 'title',
            default=None) or self._og_search_description(webpage)).strip()
        thumbnail = self._og_search_thumbnail(webpage)
        duration = parse_duration(self._search_regex(
            r'duration\s*:\s*<[^>]+>([\d:]+)', webpage, 'duration',
            default=None))

        return {
            'id': video_id,
            'url': video_url,
            'title': title,
            'thumbnail': thumbnail,
            'duration': duration,
            'age_limit': 18,
            'ext': 'mp4',
        }
