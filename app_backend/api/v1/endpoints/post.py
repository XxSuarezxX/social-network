from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from services.postService import PostService
from schemas.PostSchema import PostSchema, PostResponse, PostToUpdate
from core.database import get_db
from core.security import get_current_user
from uuid import UUID

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostResponse)
async def createPost(post: PostSchema, 
                     db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    post_data = PostService(db)

    new_post = await post_data.create_new_post(post, current_user.id)

    if not new_post:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= "Problema al crear el post")
    return new_post

@router.get ("/", response_model=list[PostResponse])
async def getPost(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    post_data = PostService(db)

    posts = await post_data.get_posts_by_user_id(current_user.id)

    if not posts:
        return []
    return posts

@router.put("/{post_id}", response_model=PostResponse)
async def updatePost(post_id: UUID, post: PostToUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    post_data = PostService(db)

    post_updated = await post_data.update_post(post_id, post, current_user.id)

    if not post_updated:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                            detail="Problema al crear el post")
    return post_updated

@router.delete("/{post_id}")
async def delete_post(post_id: UUID, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    post_data = PostService(db)

    post_deleted = await post_data.delete_post(post_id, current_user.id)

    if post_deleted is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post no encontrado")
    if post_deleted is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permiso para eliminar este post")
    return True