# Lamudi API

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Installing

1. Clone Repository

       git clone https://github.com/bal-19/lamudi-api.git

2. Navigate to Project Directory

        cd lamudi-api

3. Create Virtual Environment (Optional)

        python3 -m venv env

4. Activate Virtual Environment (Optional)

   - Windows: 

            .\env\Scripts\activate

   - macOS/Linux:

            source env/bin/activate

5. Install Dependencies

        pip install -r requirements.txt

6. Run the FastAPI Server

        uvicorn main:app --reload

7. Access the Api

    [FastAPI Docs](http://127.0.0.1:8000/docs)    

## License

[MIT](LICENSE)
