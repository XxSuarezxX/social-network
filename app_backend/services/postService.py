from schemas.PostSchema import PostSchema, PostToUpdate
from uuid import UUID
from models.posts import Posts
from sqlalchemy import select
from sqlalchemy.orm import joinedload

class PostService:

    def __init__(self, db):
        self.db = db

    async def get_posts_by_user_id(self, user_id: UUID):
        query = select(Posts).options(joinedload(Posts.author)).where(Posts.user_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_new_post(self, post_data : PostSchema, author_id: UUID):
        new_post = Posts(
            user_id = author_id,
            content = post_data.content)
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)

        return new_post
    
    async def update_post(self, post_id: UUID, post_data: PostToUpdate, user_id: UUID):
        query = select(Posts).where(Posts.id == post_id)
        result = await self.db.execute(query)
        post_existing = result.scalar_one_or_none()

        if not post_existing:
            return False 
        if post_existing.user_id != user_id:
            return None
        
        post_existing.content = post_data.content
        await self.db.commit()
        await self.db.refresh(post_existing)

        return post_existing
    
    async def delete_post(self, post_id: UUID, user_id: UUID):
        query = select(Posts).where(Posts.id ==  post_id)
        result = await self.db.execute(query)
        post_existing = result.scalar_one_or_none()

        if not post_existing:
            return False
        if post_existing.user_id != user_id:
            return None
        
        await self.db.delete(post_existing)
        await self.db.commit()
        return True