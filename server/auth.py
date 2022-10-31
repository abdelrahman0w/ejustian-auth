import re
import requests
from bs4 import BeautifulSoup


def auth_user(uid: str, pwd: str) -> dict:
    def get_name() -> str:
        with requests.Session() as session:
            base = "https://sis.ejust.edu.eg/Default.aspx"
            index_res = session.get(base)
            soup = BeautifulSoup(index_res.content, features="lxml")
            VIEWSTATE = soup.find(id="__VIEWSTATE")['value']
            VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value']
            EVENTVALIDATION = soup.find(id="__EVENTVALIDATION")['value']
            login_data = {
                "__EVENTTARGET": "",
                "__EVENTARGUMENT": "",
                "__VIEWSTATE": VIEWSTATE,
                "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
                "__EVENTVALIDATION": EVENTVALIDATION,
                "txtUsername": uid,
                "txtPassword": pwd,
                "btnEnter": "Log In"
            }
            login_res = session.post(base, data=login_data)

            if name := re.findall(
                "\s*\"ctl00_lblUser\" title=\s*\".*\"><span style='font-size:9px'>(.*?)(?=</)",
                login_res.text
            )[0]:
                return " ".join(name.split())
            else:
                return ""

    try:
        return {"auth": True, "name": get_name()} if get_name else {"auth": False}
    except Exception:
        return {"auth": False}
