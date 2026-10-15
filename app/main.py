from fastapi import FastAPI

from app.routers import autores, emprestimos, livros

app = FastAPI(title="API Biblioteca", version="1.0.0",
              description="Gerenciamento de autores, livros e empréstimos.")

app.include_router(autores.router)
app.include_router(livros.router)
app.include_router(emprestimos.router)


@app.get("/", tags=["Root"])
def raiz():
    return {"mensagem": "API Biblioteca no ar. Acesse /docs"}
