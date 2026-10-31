import os,requests
V="https://graph.facebook.com/v21.0"
T=os.environ["META_TOKEN"];P=os.environ["FB_PAGE_ID"];I=os.environ["IG_USER_ID"]
def g(path,f):return requests.get(V+"/"+path,params={"fields":f,"access_token":T},timeout=60).json()
p=g(P,"name,access_token");i=g(I,"username")
print("pagina:",p.get("name") or p.get("error"))
print("token_de_pagina_disponivel:",bool(p.get("access_token")))
print("instagram:",i.get("username") or i.get("error"))
