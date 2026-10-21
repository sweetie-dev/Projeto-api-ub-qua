
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="API Biblioteca de Bairro")


# Modelo de dados de um livro
class Livro(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    isbn: str = Field(min_length=1)
    quantidade: int = Field(ge=0)


# Modelo de resposta, incluindo o ID
class LivroComId(Livro):
    id: int


# Lista que guarda os livros na memoria
livros: list[LivroComId] = []
proximo_id = 1


# GET - Listar todos os livros
@app.get("/livros", response_model=list[LivroComId])
def listar_livros():
    return livros


# GET - Buscar um livro pelo ID
@app.get("/livros/{livro_id}", response_model=LivroComId)
def buscar_livro(livro_id: int):
    for livro in livros:
        if livro.id == livro_id:
            return livro

    raise HTTPException(
        status_code=404,
        detail="Livro nao encontrado"
    )


# POST - Cadastrar um livro
@app.post(
    "/livros",
    response_model=LivroComId,
    status_code=status.HTTP_201_CREATED
)
def cadastrar_livro(livro: Livro):
    global proximo_id

    novo_livro = LivroComId(
        id=proximo_id,
        **livro.model_dump()
    )

    livros.append(novo_livro)
    proximo_id += 1

    return novo_livro


# PUT - Alterar um livro
@app.put("/livros/{livro_id}", response_model=LivroComId)
def alterar_livro(livro_id: int, dados: Livro):
    for indice, livro in enumerate(livros):
        if livro.id == livro_id:
            livro_atualizado = LivroComId(
                id=livro_id,
                **dados.model_dump()
            )

            livros[indice] = livro_atualizado
            return livro_atualizado

    raise HTTPException(
        status_code=404,
        detail="Livro nao encontrado"
    )


# DELETE - Apagar um livro
@app.delete(
    "/livros/{livro_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def apagar_livro(livro_id: int):
    for indice, livro in enumerate(livros):
        if livro.id == livro_id:
            livros.pop(indice)
            return

    raise HTTPException(
        status_code=404,
        detail="Livro nao encontrado"
    )
