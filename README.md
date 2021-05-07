# Take Home Assignment

## Instructions (Windows)

### Step 1: Clone Repo

``` 
git clone https://github.com/divyam28/ISI-TakeHome-Assignment 
cd ISI-TakeHome-Assignment
```

### Step 2: Create VirtualEnv
```
python -m venv env
env\Scripts\activate.bat
```
### Step 3: Build and Run Docker Container
This also starts the backend service
```
docker-compose up --build -d
```

### Step 4: Run Test Suite on running container
```
docker exec app python test.py
```
