from txtai.embeddings import Embeddings
from flask import Flask, request, render_template
import json

app = Flask(__name__)
embeddings = Embeddings({"path": "sentence-transformers/all-MiniLM-L6-v2"})

with open("data/vol7.json", "r") as f:
    aciklama = json.load(f)["aciklama"]
with open("data/vol7.json", "r") as f:
    baslik = json.load(f)["baslik"]

txtai_data = []
txtai_databaslik = []
txtai = []
i=0

for text in aciklama:
    txtai_data.append((i, text, None))
    i=i+1
i=0
for text in baslik:
    txtai_databaslik.append((i, text, None))
    i=i+1

@app.route("/", methods=["POST", "GET"])
def home():
     if request.method == "GET":
        return render_template("index.html", languages=baslik)
     if request.method =="POST":
        txtai = []
        search =request.form.get('search')
        if search != "":
            embeddings.index(txtai_data)
            res = embeddings.search(search,10)
            for r in res:
                txtai.append((r[1],baslik[r[0]],aciklama[r[0]]))
            embeddings.index(txtai_databaslik)
            res = embeddings.search(search,10)
            for r in res:
                txtai.append((r[1],baslik[r[0]],aciklama[r[0]]))
            x=sorted(txtai,reverse=True)
            return render_template("index.html", baslik=x,languages=baslik)
        else:
            return render_template("index.html", languages=baslik)
        
 

if __name__ == '__main__':
    app.run(debug=True)

