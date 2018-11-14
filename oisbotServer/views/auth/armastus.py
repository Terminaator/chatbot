import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
session = HTMLSession()
r = session.get("https://ois2dev.ut.ee/api/user/sso")
arr = r.url.split("AuthState")
p = session.post(arr[0] + "username=x&password=y&AuthState"+arr[1])
soup = BeautifulSoup(p.content.decode("utf8"),features="lxml")
#print(soup.find("input", {"name":"SAMLResponse"})["value"])
#print(soup.find("input", {"name":"RelayState"})["value"])
#print(soup)
payload = {
    'SAMLResponse': soup.find("input", {"name":"SAMLResponse"})["value"],
    'RelayState': soup.find("input", {"name":"RelayState"})["value"]
}
k = session.post("https://ois2dev.ut.ee/Shibboleth.sso/SAML2/POST",data=payload)
s = session.get("https://ois2dev.ut.ee/api/user/sso")
headers = {'X-Access-Token': session.cookies["X-Access-Token"] + " e"}
print(headers)
n = requests.get("https://ois2dev.ut.ee/api/user",headers=headers)
print(n.content)