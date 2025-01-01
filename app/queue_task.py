from mysql.connector import connect
import sys, json

def fetch_recommendations(params: dict):    

    def get_db():        
        db = connect(
            host="localhost",
            user="root",
            password="your_new_password",
            database="movies_api",
        )        
        if not db: sys.exit()
        return db

    try:
        # Create cursor
        conn = get_db()        
        cursor = conn.cursor()

        # Form the query
        # params = {
        #     "user_id": user_id,
        #     "title": title,
        #     "director": director,
        #     "genre": genre,
        #     "year": year,
        #     "rating": rating,
        #     "limit": limit
        # }

        # precheck if everything is none
        count = 0
        for k, v in params.items(): 
            if v == None: count += 1
            
        conditions = []
        query2 = ""
        # If no filters passed, fetch users exisiting preferences
        if count == len(params) - 2:
            # Fetch from db preferences            
            fetch_query = """
            SELECT pref_json FROM preferences WHERE user_id = %(user_id)s
            """
            cursor.execute(fetch_query, params)
            data = cursor.fetchone()
            preferences: dict = json.loads(data[0])
            for k, v in preferences.items(): params[k] = v            
        
        # Form query2
        def create_placeholder(arr: list):
            placeholder = ', '.join(['%s'] * len(arr))
            return placeholder

        query_params = []
        for k, v in params.items(): 
            if v and k != 'limit' and k != 'user_id': 
                if isinstance(v, str): 
                    conditions.append(f"{k} = %s")
                    query_params.append(v)
                elif isinstance(v, list):  
                    conditions.append(f"{k} IN ({create_placeholder(v)})")                
                    for i in v: query_params.append(i)
        query_params.append(params['limit'])

        if conditions: 
            conditions = ' AND '.join(conditions)
            query2 = "WHERE " + conditions
        
        # Form final query
        query1 = """SELECT * FROM movies"""        
        query3 = """LIMIT %s;"""        
        query = ' '.join([query1, query2, query3])  
        # print(params, query_params)
        # print("$$$$$$$$Q:", query)            
        
        # Fetch data
        cursor.execute(query, query_params)        
        results = cursor.fetchall()
                
        return {"data": results}

    except Exception as e: raise 
    finally:
        cursor.close()
        conn.close()