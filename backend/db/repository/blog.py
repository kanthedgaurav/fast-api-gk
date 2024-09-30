from sqlalchemy.orm import Session
from schemas.blog import CreateBlog, UpdateBlog
from db.models.blog import Blog

def create_new_blog(blog: CreateBlog, db: Session, current_user: int):
    blog = Blog(title=blog.title, slug=blog.slug, content=blog.content, author_id=current_user)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog

def retrieve_blog(id: int, db: Session):
    blog = db.query(Blog).filter(Blog.id == id).first()
    return blog

def list_blogs(db: Session):
    blogs = db.query(Blog).filter(Blog.is_active == True).all()
    return blogs

def update_blog_by_id(id: int, blog: UpdateBlog, db: Session, author_id: int = 1):
    blog_in_db = db.query(Blog).filter(Blog.id == id).first()
    if not blog_in_db:
        return {"error" : f"Blog with id {id} not found"}   
    if blog_in_db.author_id == author_id:
        return {"error" : "Not authorized to update the blog"}
    blog_in_db.title = blog.title
    blog_in_db.content = blog.content
    db.add(blog_in_db)
    db.commit()
    db.refresh(blog_in_db)
    return blog_in_db

def delete_blog_by_id(id: int, db: Session, author_id: int = 1):
    blog_in_db = db.query(Blog).filter(Blog.id == id)
    if not blog_in_db.first():
        return {"error" : f"Blog with id {id} not found"}
    if not blog_in_db.author_id == author_id:
        return {"error" : "Not authorized to delete the blog"}
    blog_in_db.delete(synchronize_session=False)
    db.commit()
    return {"message": f"Deleted Successfully with id {id}"}