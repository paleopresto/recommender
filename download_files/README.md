### Read Data From Lipd files
1. Download the lipd files from LinkedEarthWiki 
Requirements - 
```
pip install requests bs4 lxml beautifulsoup4 html5lib
```
Run the python file
```
py download.py
```

Common errors and Fixes
1. bs4.FeatureNotFound: Couldn't find a tree builder with the features you requested: lxml. Do you need to install a parser library?

2. change the features for BeautifulSoup to 'html5lib'.
```python
soup = bs(data, 'html5lib')
```
3. If this doesn't work as well, then use the default html parser that comes with python. 
```python
soup = bs(data, 'html.parser')
```

After all files are downloaded, we need to read these lipd files and extract the following attributes.
1. Archive Type
2. Proxy Observation Type
3. Units
4. Inferred Variable Type
5. Interpretation Variable
6. Interpretation Variable Detail

Run the Notebook - table_com.ipynb to read the lipd files and extract attributes.
