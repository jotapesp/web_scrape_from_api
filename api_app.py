from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

@app.get("/usuario/{id}")
async def profile(id: int):
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        match = cursor.execute("SELECT * FROM users WHERE id = ?", (id,)).fetchone()
        return {"nome":f"{match['nome']}",
                "nascimento":f"{match['nascimento']}",
                "cpf":f"{match['cpf']}",
                "genero":f"{match['genero']}"}
    except Exception as error:
        raise HTTPException(status_code=404, detail="Not Found")
    finally:
        cursor.close()

@app.get("/dados")
async def dados():
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        cursor.row_factory = sqlite3.Row
        match = cursor.execute("SELECT * FROM users").fetchall()
        total = len(match)
        today = datetime.now()
        total_age = 0
        women, men, non = 0, 0, 0
        for person in match:
            date_obj = datetime.strptime(person["nascimento"], "%d/%m/%Y")
            age_days = today - date_obj
            age_years = int(age_days.days / 365)
            total_age += age_years
            if person["genero"].lower() == 'm':
                men += 1
            elif person["genero"].lower() == 'f':
                women += 1
            else:
                non += 1
        avg_age = total_age / total
        return {"total_usuarios":f"{total}",
                "media_idade":f"{avg_age}",
                "mulheres":f"{women}",
                "homens":f"{men}",
                "nao-binario_outros":f"{non}"}
    except Exception as error:
        raise HTTPException(status_code=404, detail=f"{error}")
    finally:
        cursor.close()

class Resp(BaseModel):
     nome: str
     nascimento: str
     cpf: str
     genero: str

@app.post("/novo")
async def novo(resp: Resp):
    try:
        conn = sqlite3.connect("data.db")
        cursor = conn.cursor()
        nascimento = str(resp.nascimento)
        if nascimento.find("/") == -1:
            if len(nascimento) != 8:
                raise HTTPException(status_code=500, detail="Nascimento deve estar no formato dd/mm/aaaa")
            elif len(nascimento) == 8:
                lista = list(nascimento)
                lista.insert(2, "/")
                lista.insert(5, "/")
                nascimento = "".join(lista)
        if nascimento.count("/") != 2:
            raise HTTPException(status_code=500, detail="Nascimento deve estar no formato dd/mm/aaaa")
        genero = str(resp.genero)
        if genero.lower() != "f" and genero.lower() != "m" and genero.lower() != "n":
            raise HTTPException(status_code=404, detail="Genero deve ser M, F ou N")
        cursor.execute("""INSERT INTO users(nome, nascimento, cpf, genero)
                       VALUES (?, ?, ?, ?)""", (resp.nome, nascimento, resp.cpf, resp.genero))
        conn.commit()
        return {"nome": resp.nome, "nascimento": nascimento, "cpf": resp.cpf, "genero": resp.genero}
    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"{error.detail}")
    finally:
        cursor.close()
