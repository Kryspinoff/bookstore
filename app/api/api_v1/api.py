from app.api.api_v1.routers import (
    authors, books, dev, genres, login, orders, profile, register, reviews, users
)
from fastapi import APIRouter


router = APIRouter()

router.include_router(authors.router)
router.include_router(books.router)
router.include_router(dev.router)
router.include_router(genres.router)
router.include_router(login.router)
router.include_router(orders.router)
router.include_router(profile.router)
router.include_router(register.router)
router.include_router(reviews.router)
router.include_router(users.router)
