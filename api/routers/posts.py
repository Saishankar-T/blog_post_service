from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.models.post import Post
from api.models.user import User  
from api.lib.database import get_db
from api.lib.auth_handler import get_current_user

router = APIRouter()

# Helper function to get owner_id from username
def get_owner_id_by_username(username: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.id

@router.get("/posts" , description= "GET ALL POSTS")
def get_all_posts(db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    owner_id = get_owner_id_by_username(username, db)
    return db.query(Post).filter(Post.owner_id == owner_id).all()

@router.get("/posts/{post_id}", description= "GET SINGLE POST WITH POST_ID")
def get_post_with_post_id(post_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    owner_id = get_owner_id_by_username(username, db)
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == owner_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    return post

@router.post("/posts", description= "POST WITH TITLE AND CONTENT")
def create_post(title: str, content: str, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    owner_id = get_owner_id_by_username(username, db)
    post = Post(title=title, content=content, owner_id=owner_id)
    db.add(post)
    db.commit()
    return {"message": "Post created", "post": post}

@router.put("/posts/{post_id}", description= "UPDATE POST WITH POST_ID")
def update_post(post_id: int, title: str, content: str, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    owner_id = get_owner_id_by_username(username, db)
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == owner_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    
    # Updating post fields
    post.title = title
    post.content = content
    db.commit()
    return {"message": "Post updated", "post": post}

@router.delete("/posts/{post_id}", description= "DELETE POST WITH POST_ID")
def delete_post(post_id: int, db: Session = Depends(get_db), username: str = Depends(get_current_user)):
    owner_id = get_owner_id_by_username(username, db)
    post = db.query(Post).filter(Post.id == post_id, Post.owner_id == owner_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found or not authorized")
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}
