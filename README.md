# blog_post_service

Step-1 : Create a virtual environment

        python3 -m venv venv 
        source venv/bin/activate 

Step-2 : Install requirements 

        pip install requirements.txt

Step-3 : Add env's of database credientials in .env file

Step-4 : Start the service 

        uvicorn api.main:app --reload --port=8000
