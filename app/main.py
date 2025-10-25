from fastapi import FastAPI

from app.routers import (authroization_route, ticket_route,
                         user_route)

app = FastAPI(title="Async FastAPI Example")

# 🔹 Реєструємо роутер
app.include_router(user_route.router)
app.include_router(authroization_route.router)
app.include_router(ticket_route.router)
