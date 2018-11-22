from multiprocessing.pool import ThreadPool
import urllib3
import requests
import time
import sys
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
good_url = []
urls = []
i = 0

def fetch_url(url):
    global i
    try:
        response = requests.get(url, timeout=1, allow_redirects=False)
        i =i+1
        return url, response, None
    except requests.exceptions.SSLError as e:
        try:
            url = url.replace('https', 'http')
            response = requests.get(url, verify=False, timeout=1, allow_redirects=False)
            i = i + 1
            return url, response, None
        except:
            return None, None, None
    except:
        return None, None, None


def sendRequests(threads, output, lenght, code):
    print('Started')
    results = ThreadPool(threads).imap_unordered(fetch_url, urls)
    for url, response, error in results:
        if (response) and (results):
            if response.status_code == code and len(response.text) > lenght:
                proc = len(urls)/100
                progr = i/proc
                print(f"\rProgress: {round(progr)}%\r", end="")
                sys.stdout.flush()
                good_url.append(url)
    f = open(output, 'a')
    for url in good_url:
        print(url)
        f.write(url + "\n")
    f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domains', type=str, default='domains.txt',
                        help='List of domains', required=True)
    parser.add_argument('-t', '--threads', type=int, default=50,
                        help='Count of threads')
    parser.add_argument('-o', '--output', type=str, default='results.txt',
                        help='File for output', required=False)
    parser.add_argument('-l', '--lenght', type=int, default='50',
                        help='Minimal lenght of html', required=False)
    parser.add_argument('-c', '--code', type=int, default='200',
                        help='Status code which valid', required=False)
    args = parser.parse_args()

    for url in open(args.domains):
        urls.append('https://' + url.strip())
    print('Loaded: '+str(len(urls))+' urls.')
    sendRequests(args.threads, args.output, args.lenght, args.code)
