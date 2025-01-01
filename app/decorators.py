import functools, json
from flask import jsonify, request
from app.database import redis_client

def cache_fetch_movies():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Check cache
            ## preprocess
            user_id = request.args.get("user_id", -1) # Mandatory
            title = request.args.get("title", None)
            genre = request.args.get("genre", None)
            director = request.args.get("director", None)
            year = request.args.get("year", None)        
            rating = request.args.get("rating", None)
            limit = request.args.get("limit", 5, type=int)
            if user_id == -1: return jsonify({"error", "Missing Required Fields"}), 400
            params = {
                "user_id": user_id,
                "title": title,
                "director": director,
                "genre": genre,
                "year": year,
                "rating": rating,
                "limit": limit
            }

            cache_params = {}
            for k, v in params.items():
                if v != None and k != 'user_id' and k != 'limit': cache_params[k] = v
            
            ## Get from cache if present
            cache_key = f"movies:{str(cache_params)}"
            cached_response = redis_client.get(cache_key)
            if cached_response:
                print("Returning from cache!")
                return jsonify(json.loads(cached_response)), 200

            kwargs["params"] = params
            print(args, kwargs)
            response, statuscode = func(*args, **kwargs)            
            
            if "error" in response: return jsonify(response), statuscode
            
            # store in cache (task_id -> params)
            serialized_response = json.dumps(cache_params, default=str)
            task_id = f"movie_params:{str(response["task_id"])}"
            redis_client.set(task_id, serialized_response, ex=1000)
            return jsonify(response), statuscode
        
        return wrapper
    return decorator

def cache_store_movie():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task_id = request.args.get("task_id", -1)

            if task_id == -1:  return jsonify({"error": "Missing required information"}), 400            
            kwargs["task_id"] = task_id
            response, statuscode = func(*args, **kwargs)

            # params -> movies
            if statuscode == 200:
                cache_key = f"movie_params:{str(task_id)}"
                params = redis_client.get(cache_key)
                if params:
                    serialized_response = json.dumps(response)
                    params = json.loads(params)
                    store_key = f"movies:{str(params)}"
                    redis_client.set(store_key, serialized_response,ex=100)
            return jsonify(response), statuscode

        return wrapper
    return decorator
