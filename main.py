
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="API Biblioteca de Bairro")


#modelo de como os dados de um livro irão aparecer
class Livro(BaseModel):
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1)
    isbn: str = Field(min_length=1)
    quantidade: int = Field(ge=0)

class LivroComId(Livro):
    id: int


#a lista que guarda os livros
livros: list[LivroComId] = []
proximo_id = 1


#metodo get que lista os livros
@app.get("/livros", response_model=list[LivroComId])
def listar_livros():
    return livros


#metodo get busca os livros pelo Id
@app.get("/livros/{livro_id}", response_model=LivroComId)
def buscar_livro(livro_id: int):
    for livro in livros:
        if livro.id == livro_id:
            return livro

    raise HTTPException(
        status_code=404,
        detail="Livro nao encontrado"
    )


#metodo post postar um livro novo
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


#metodo put atualizar/ alterar informações em um livro
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


#metodo delete para apagar um livro
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
