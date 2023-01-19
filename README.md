# Bookstore Project

### Description
This is the repository of bookstore (database with app). The project shows my skills.


### Deployment
```bash
git clone https://github.com/Kryspinoff/bookstore
cd Bookstore/
```

Create and activate the virtual environment and then install all dependencies from the requirements.txt.
Then configure the `.env.development` file and run the following code to 
migrate and initialize the super admin in the application.

```bash
bash prestast.sh
```

Run the following code to start the services:

```bash
uvicorn app.main:app --port 8000
```

Run the following code to start the tests:

```bash
bash tests-start.sh
```
