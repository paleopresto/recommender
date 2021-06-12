from bs4 import BeautifulSoup as bs
import requests

url = 'http://wiki.linked.earth/Special:WTLiPD'

response = requests.get(url)
data = response.text
# soup = bs(data,features = 'lxml')
# soup = bs(html, "html5lib")
soup = bs(data, 'html.parser')

l_list = []
for link in soup.find_all('a') :
    #print(link.get('href'))
    if link.get('href') == None :
        continue
    if link.get('href').startswith('?op=export&lipdid=') :
        print(link.get('href'))
        l_list.append(link.get('href'))
        full_url = url + link.get('href')
        #urllib.request.urlretrieve(full_url, sys.argv[1]+'{}.lpd'.format(link.get('href').split('=')[2]))
        r = requests.get(url + link.get('href'))
        open(link.get('href').split('=')[2]+'.lpd','wb').write(r.content)
print("num of lpd files: ", len(l_list))

