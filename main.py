from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
		id: int #How can this field be made unique, cos i noticed i can more than 1 data entries with the same id
		content: str
		created_at: datetime = datetime.now()
		

my_posts = []        

def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post
	
#when using this function, you use it to get the post data that matches the id, but for you to update the my_posts db you need to get the index of this post data you've, only then can you manipulate it in the db

def find_index(id):
	for i, p in enumerate(my_posts):
		if p["id"] == id:
			return i

# to see all routes
@app.get("/")
def routes():
	routes = ["/posts"]
	return {"data": routes}


# get all posts
@app.get("/posts")
def get_all_post():
	return {"data": my_posts}


# create post
@app.post("/posts")
def create_posts(data : Post):
	new_post = data.dict()
	my_posts.append(new_post)
	return {"data": new_post}


# get post detail
@app.get("/posts/{id}")
def get_post(id: int):
	existing_post = find_post(id)
	if not existing_post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} not found")
	return {"post_detail": existing_post}


# update a post
@app.put("/posts/{id}")
def update_post(id: int, data: Post):
	existing_post = find_post(id)
	if not existing_post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} not found")
	
	updated_post = data.dict()
	index_of_existing_post = my_posts.index(existing_post)
	# Find the index of the previous post and replace it with the new
	my_posts[index_of_existing_post] = updated_post

	return {"post_detail": updated_post}


# delete
@app.delete("/posts/{id}")
def delete_post(id: int):
	existing_post = find_post(id) 
	if not existing_post:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} not found")
	
	my_posts.remove(existing_post)
	""" 
		#Or you can use the below code 
		#my_posts.pop(my_posts.index(existing_post))	
	"""
	return {"message": "deleted successfully"}