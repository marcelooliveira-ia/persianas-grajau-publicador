import os,requests,time
V="https://graph.facebook.com/v21.0"
T=os.environ["META_TOKEN"];P=os.environ["FB_PAGE_ID"];I=os.environ["IG_USER_ID"];B=os.environ["BASE_URL"].rstrip("/")
def post(path,tok,**d):d["access_token"]=tok;return requests.post(V+"/"+path,data=d,timeout=120).json()
def get(path,tok,**d):d["access_token"]=tok;return requests.get(V+"/"+path,params=d,timeout=60).json()
pt=get(P,T,fields="access_token").get("access_token") or T
c=post(I+"/media",pt,image_url=B+"/midia/2026-11-02_carrossel_1_capa.png",caption="TESTE de publicacao automatica. Sera apagado em instantes.")
cid=c.get("id");print("container:",cid or c.get("error"))
s=None;n=0
while cid and s not in ("FINISHED","ERROR") and n<40:s=get(cid,pt,fields="status_code").get("status_code");n+=1;time.sleep(4)
r=post(I+"/media_publish",pt,creation_id=cid) if s=="FINISHED" else {}
print("status:",s);print("publicado:",r.get("id") or r.get("error"))
