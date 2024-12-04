# Dream11 Prediction app

## Project Structure

```
├── README.md                   <- Project overview and usage instructions
├── data                       
│   ├── interim                
│   ├── processed             
│   └── raw                     
│       ├── cricksheet_data     
│       └── additional_data     
├── data_processing             
│   ├── data_download.py       
│   └── feature_engineering.py  
├── docs                       
│   └── video_demo

├── model                       <- Modeling scripts for training and prediction
│   ├── train_model.py          <- Model training script
│   └── predict_model.py        <- Prediction script with trained models
├── model_artifacts             <- Storage for trained models
├── out_of_sample_data          
├── Backend
└── Fronend                          
```

## Frontend

For the product UI we are using React 
use the Following `.env` by adding contents given in the `.env.sample` we have shared a link of backend that we have hosted. This help you use the fronted even if you backend in not working.

Now to use the frontend you should install  [Node.js 20.10.0](https://nodejs.org/en/download/)

if you have node js on you device you can verify it by running `node -v`.

Then navigate to frontend folder
Install the dependencies

```bash
cd frontend
npm i
npm start
```

Now you will have a frontend running the one the port `3000`


## Backend


Download the appropriate version of [Python 3.12](https://www.python.org/downloads/release/python-3120/).

Naviate to the backend folder and install  required packages

```bash
cd backend
pip install venv
python -m venv venv
```
Appropriately activate the virtual environment. 
For Windows
```bash
.\venv\Scripts\activate
```
For Linux
```bash
source venv/bin/activate
```

Make `.env` by adding contents given in the `.env.sample`
```javascript
\\ env.sample
DATABASE_URL=""
GROQ_API_KEY=""
```
we have shared a link of Database and a GROQ key for your assistance that we have hosted. This help you use the fronted even if you backend in not working.


Then we migrations 
```bash
python manage.py makemigrations

python manage.py migrate
```
And start the Server
```bash
python manage.py runserver
```


## Model UI

Download the appropriate version of [Python 3.12](https://www.python.org/downloads/release/python-3120/).

Navigate to the model folder

```bash
cd model
pip install venv
python -m venv venv
```
Appropriately activate the virtual environment. 
For Windows
```bash
.\venv\Scripts\activate
```
For Linux
```bash
source venv/bin/activate
```
Download all the required packages

```bash
pip install -r requirements.txt
```

Then run the streamlit
```bash
streamlit model_ui_app.py
```