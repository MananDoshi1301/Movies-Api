import json
from flask import Flask, request
from app.database import mysql, redis_conn
from app.decorators import cache_fetch_movies, cache_store_movie
# from worker.tasks import fetch_recommendations
from redis import Redis
from app.queue_task import fetch_recommendations
from rq import Queue
from rq.job import Job

def register_routes(server: Flask):          

    @server.route("/recommendations/status", methods=["GET"])
    @cache_store_movie()
    def get_movies(task_id):
        queued = {"status": "queued", "message": "Task is queued!"}
        started = {"status": "processing", "message": "Recommendation task is still in progress."}
        complete = {"status": "completed", "data": []}
        failed = {"status": "failed", "error": "An error occurred while processing the task. Please try again later."}        
        
        job = Job.fetch(task_id, connection=redis_conn)
        status = job.get_status()
        if status == "queued": return queued, 202
        elif status == "started": return started, 202
        elif status == "finished": 
            result = job.result
            complete["data"] = result
            return complete, 200
        else:
            return {"status": status, "error": "Some error"}, 500        

    # Check if the cache has the response
    @server.route("/recommendations", methods=["GET"])   
    @cache_fetch_movies()     
    def get_recommendations(params):                
        try:            
            q = Queue('high', connection=redis_conn)
            job = q.enqueue(fetch_recommendations, params, ttl=30)                        
            return {    
                    "task_id": job.id, 
                    "message": "Recommendations are being calculated!"                    
                }, 202
            
        except Exception as e:
            print("Error on route", e)
            return {"error": "Internal Server Error"}, 500        

    @server.route("/preferences", methods=["POST"])
    def set_preferences():
        # preferences (JSON or text): genre, liked movies, etc
        data: dict = request.get_json()
        user_id: int = data.get('user_id', -1)
        preferences: dict = data.get('preferences', {})
        print(user_id, preferences)
        if user_id == -1 or not preferences: return "Missing required information", 400
        preference_dump = json.dumps(preferences)
        try:
            cursor = mysql.connection.cursor()
            query = """
            INSERT INTO preferences (user_id, pref_json)
            VALUES (%s, %s)
            ON DUPLICATE KEY
            UPDATE pref_json = VALUES(pref_json);
            """
            cursor.execute("START TRANSACTION")
            cursor.execute(query, (user_id, preference_dump))
            mysql.connection.commit()

        except Exception as e:
            mysql.connection.rollback()
            print(e)
            return "Internal Server Error", 500                    
        finally:
            cursor.close()
        
        res = { "message": "Preferences updated successfully", "data": preferences }
        return res, 200