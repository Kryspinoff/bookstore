from app import models
from sqlalchemy.orm import Session


class Toggle:

    @staticmethod
    def wishlist_book(db: Session, *, book: models.Book, user: models.User) -> models.User:
        if not user.wishlist:
            wishlist = models.Wishlist()
            user.wishlist = wishlist

        if book not in user.wishlist.books:
            user.wishlist.books.append(book)
        else:
            user.wishlist.books.remove(book)

        db.add(user)
        db.commit()
        db.refresh(user)
        return user.wishlist


toggle = Toggle()
