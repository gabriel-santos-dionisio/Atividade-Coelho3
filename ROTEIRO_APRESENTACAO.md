# Roteiro de apresentação (≈ 8 min)

1. **Introdução (1 min)** – tema: biblioteca; 3 entidades; relacionamentos Autor→Livro→Empréstimo (mostrar diagrama do README).
2. **Arquitetura (1 min)** – pastas `core`, `models`, `schemas`, `routers`; por que separar Create/Update/Response.
3. **Migrations (1 min)** – mostrar `alembic/versions/`, rodar `alembic upgrade head`.
4. **Demo no Swagger `/docs` (4 min)**
   - POST `/autores/` → 201
   - POST `/livros/` com `autor_id: 999` → 404 (integridade); depois com autor válido → 201
   - POST `/livros/` repetindo ISBN → 409
   - POST `/emprestimos/` → 201; ver `exemplares_disponiveis` cair para 0 em GET `/livros/{id}`
   - POST `/emprestimos/` de novo → 409 (sem estoque)
   - PATCH `/emprestimos/{id}/devolver` → estoque volta
   - POST `/autores/` com nome de 1 letra → 422
   - DELETE `/autores/{id}` com livros → 409
5. **Encerramento (1 min)** – divisão de tarefas do grupo e dificuldades.

Lembrete: cada integrante deve ter commits no repositório.
