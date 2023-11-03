<h1 style = 'text-align: center'> STEAM™ Game Recommendation System </h1>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Steam](https://img.shields.io/badge/steam-%23000000.svg?style=for-the-badge&logo=steam&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Render](https://img.shields.io/badge/Render-%46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

![Steam™ Logo](https://github.com/PatoMarzi/Steam_ML/blob/main/assets/images/steam.png)

# This project simulates what a MLOps Engineer responsibilites and tasks are

**_NOTE:_** This just covers the basics of a MLOps Engineer, it should be taken as a guide. The aim of this project is to create a Minimum Value Product (MVP) with just enough features to be usable for early-access customers.

# _Extraction, Transfrom & Load (ETL)_

![ETL Process](./assets/images/ETL.png)

- Our first step is to see what type of data are we working with, if it is text, images, videos, etc. We extract this data from a wide range of sources, depending our goal.

- Once our data has been identified, we move on to the second step which is manipulate said data. We do so by removing, changing, normalising any value that is of no use for the project. This part is key, since it will determine how our data will be loaded into a server or a web application. It will also impact on the program eficiency. For this particular case, we had to be very careful on how big our files were, since the server that we used **`(FastAPI)`** only allowed us to load up to 512MB.

- The last step is to load our cleaned data into a web application. As mentioned before, the server allowed us to allocate 512MB of storage. An impetuous transformation process could delay the whole deploying process, causing setbacks and jeopardize the project.

#### [Click Here To See The Whole Process](https://github.com/PatoMarzi/Steam_ML/blob/main/ETL.ipynb)

# _Exploratory Data Analysis (EDA)_
