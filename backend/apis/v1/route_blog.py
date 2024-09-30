from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from schemas.blog import CreateBlog,ShowBlog, UpdateBlog
from typing import List
from db.models.user import User
from apis.v1.route_login import get_current_user


from db.repository.blog import create_new_blog , retrieve_blog, list_blogs, update_blog_by_id, delete_blog_by_id

router = APIRouter()

@router.post("/", response_model=ShowBlog, status_code=status.HTTP_201_CREATED) 
def create_blog(blog: CreateBlog, db: Session = Depends(get_db)):
    current_user = 1
    blog = create_new_blog(blog, db, current_user)
    return blog

@router.get("/{id}", response_model=ShowBlog)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = retrieve_blog(id, db)
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")
    return blog

@router.get("",response_model=List[ShowBlog])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = list_blogs(db=db)
    return blogs

@router.put("/{id}",response_model=ShowBlog)
def update_a_blog(id: int, blog: UpdateBlog, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    blog = update_blog_by_id(id=id, blog=blog, db=db, author_id=current_user.id)  
    if isinstance(blog, dict):
            raise HTTPException(
                 status_code=status.HTTP_400_BAD_REQUEST, 
                 detail=blog.get("error")   
            )
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")    
    return blog

@router.delete("/{id}")
def delete_a_blog(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    message = delete_blog_by_id(id=id, db=db, author_id=current_user.id)
    if message.get("error"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} is not found")    
    return {"msg": "Deleted successfully"}