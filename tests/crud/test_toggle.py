from app import crud, models
from sqlalchemy.orm import Session


def test_add_book_to_user_wishlist(db: Session, db_wishlist: models.Wishlist) -> None:
    db_user = crud.user.get_by_username(db, username="william_smith")
    assert isinstance(db_user.wishlist, models.Wishlist)
    assert db_user.wishlist.books[0].title == "Think again: the power of knowing what you don't know"


def test_remove_book_from_user_wishlist(db: Session, db_wishlist: models.Wishlist) -> None:
    db_user = crud.user.get_by_username(db, username="william_smith")
    db_book = crud.book.get_by_title(db, title="Think again: the power of knowing what you don't know")
    crud.toggle.wishlist_book(db, book=db_book, user=db_user)
    assert db_user.wishlist.books == []