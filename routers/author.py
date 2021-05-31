# from fastapi import APIRouter, Depends, HTTPException
# from odmantic import AIOEngine, ObjectId
#
# from db.mongodb import mongo_engine
# from models.author import Author  # AuthorUpdate
#
# router = APIRouter(
#     tags=["author"],
#     prefix="/author"
# )
#
#
# @router.get("/")
# async def get_all(page: int = 1, engine: AIOEngine = Depends(mongo_engine)):
#     skip: int = 20 * (page - 1)
#     authors = await engine.find(Author, skip=skip, limit=20)
#     return authors
#
#
# @router.get("/{id}")
# async def get(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
#     author = await engine.find_one(Author, Author.id == id)
#     if author is None:
#         raise HTTPException(404)
#     return author
#
# # @router.put("/", response_model=Author)
# # async def create(author: Author, engine: AIOEngine = Depends(mongo_engine)):
# #     await engine.save(author)
# #     return author
# #
# #
# # @router.patch("/{id}", response_model=Author)
# # async def update(id: ObjectId, patch: AuthorUpdate, engine: AIOEngine = Depends(mongo_engine)):
# #     author = await engine.find_one(Author, Author.id == id)
# #     if author is None:
# #         raise HTTPException(404)
# #
# #     patch_dict = patch.dict(exclude_unset=True)
# #     for name, value in patch_dict.items():
# #         setattr(author, name, value)
# #     await engine.save(author)
# #     return author
# #
# #
# # @router.delete("/{id}")
# # async def delete(id: ObjectId, engine: AIOEngine = Depends(mongo_engine)):
# #     author = await engine.find_one(Author, Author.id == id)
# #     if author is None:
# #         raise HTTPException(404)
# #     await engine.delete(author)
# #     return author
