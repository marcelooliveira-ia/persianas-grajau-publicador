"""Publica no Instagram e Facebook (Graph API) os itens de agenda.json cujo horario ja chegou.
Segredos (variaveis de ambiente, configuradas no GitHub): META_TOKEN (token da Pagina), FB_PAGE_ID, IG_USER_ID, BASE_URL (GitHub Pages com a pasta midia/).
Estado em publicado.json (evita duplicar)."""
import json, os, sys, time, datetime as dt, requests
V = "https://graph.facebook.com/v21.0"
TOKEN, PAGE, IG, BASE = (os.environ[k] for k in ("META_TOKEN","FB_PAGE_ID","IG_USER_ID","BASE_URL"))
TOKEN = requests.get(V+"/"+PAGE, params={"fields":"access_token","access_token":TOKEN}, timeout=60).json().get("access_token", TOKEN)
DRY = os.environ.get("DRY_RUN") == "1"

def post(path, **data):
    data["access_token"] = TOKEN
    if DRY: print("DRY", path, {k: v for k, v in data.items() if k != "access_token"}); return {"id": "dry"}
    r = requests.post(f"{V}/{path}", data=data, timeout=120)
    if r.status_code >= 400: raise RuntimeError(f"{path}: {r.text}")
    return r.json()

def get(path, **p):
    p["access_token"] = TOKEN
    return requests.get(f"{V}/{path}", params=p, timeout=60).json()

def url(f): return f"{BASE.rstrip('/')}/{f}"

def espera_container(cid):
    if DRY: return
    for _ in range(60):
        s = get(cid, fields="status_code").get("status_code")
        if s == "FINISHED": return
        if s == "ERROR": raise RuntimeError(f"container {cid} com erro")
        time.sleep(10)
    raise RuntimeError(f"container {cid} nao ficou pronto")

def ig_publicar(**kw):
    c = post(f"{IG}/media", **kw)["id"]; espera_container(c)
    return post(f"{IG}/media_publish", creation_id=c)

def publicar(it):
    t, fs, leg = it["tipo"], [url(f) for f in it["arquivos"]], it["legenda"]
    if t == "foto":
        ig_publicar(image_url=fs[0], caption=leg)
        post(f"{PAGE}/photos", url=fs[0], caption=leg)
    elif t == "carrossel":
        kids = [post(f"{IG}/media", image_url=u, is_carousel_item="true")["id"] for u in fs]
        for k in kids: espera_container(k)
        ig_publicar(media_type="CAROUSEL", children=",".join(kids), caption=leg)
        ids = [post(f"{PAGE}/photos", url=u, published="false")["id"] for u in fs]
        post(f"{PAGE}/feed", message=leg, **{f"attached_media[{i}]": json.dumps({"media_fbid": x}) for i, x in enumerate(ids)})
    elif t == "reel":
        ig_publicar(media_type="REELS", video_url=fs[0], caption=leg, share_to_feed="true")
        post(f"{PAGE}/videos", file_url=fs[0], description=leg)
    elif t == "story_video":
        ig_publicar(media_type="STORIES", video_url=fs[0])
        # Story no Facebook nao e publicado aqui (evita virar post de feed); ver LEIA-ME.
    else: raise ValueError(t)

def main():
    est = json.load(open("publicado.json")) if os.path.exists("publicado.json") else []
    agora = dt.datetime.now(dt.timezone.utc)
    for it in json.load(open("agenda.json", encoding="utf-8")):
        if it["id"] in est: continue
        quando = dt.datetime.fromisoformat(it["quando"])
        if quando > agora: continue
        if (agora - quando).total_seconds() > 6*3600:
            print("pulado (atrasado >6h):", it["id"]); continue
        print("publicando", it["id"]); publicar(it); est.append(it["id"])
        json.dump(est, open("publicado.json", "w"))
if __name__ == "__main__": main()
