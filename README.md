
# GetAround!

Project carried out within the framework of my training Data Fullstack, Jedha's Bootcamp Paris. 

GetAround is the Airbnb for cars. You can rent cars from any person for a few hours to a few days!
Client are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.
This can generate high friction for the next driver if the car was supposed to be rented again on the same day.
 
The project is divided into two parts:

Part 1 : Web dashboard to help product manager to decide: 
- threshold: how long should the minimum delay be?
- scope: should we enable the feature for all cars?, only Connect cars?

Part 2 : Machine learning to predict price rental car per day and make it available through an API. 












## Installation

To install my project in local, you just need to git clone the repository (https://github.com/Fanny-Mlmrtl/Bloc_5). Then, create a virtual environment (see Environment Variables section).

    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file. Also, you will get all the requirements needed in the requirements.txt.

- Streamlit app:
`numpy`
`pandas`
`streamlit`
`plotly.express`
`statsmodels`
`openpyxl`
`defusedxml`

- Machine learning 
`numpy`
`pandas`
`joblib`
`sklearn`

- Save model
`joblib`

- API
`joblib`
`pandas`
`xmlrpc.client`
`uvicorn`
`pydantic`
`typing`
`fastapi`
`json`









## Demo

https://share.vidyard.com/watch/Zjb8DXGPxzkMD3NQgPpUsC



## Links

- Web dashboard: https://getaround-app.herokuapp.com/
- API: https://getaround-api-fm.herokuapp.com/
## Screenshots: 

!["Web dashboard"](https://github.com/Fanny-Mlmrtl/Bloc_5/blob/main/Streamlit.png)
!["API"](https://github.com/Fanny-Mlmrtl/Bloc_5/blob/main/API.png)
!["API"](https://github.com/Fanny-Mlmrtl/Bloc_5/blob/main/API_bis.png)
## Roadmap

To go further with this project it will be interesting to use MLFlow to track models and register them. 
Also, it will be interesting to build an API with more informations. 
## Acknowledgements

 A big thank you to Coralie for her help and support :)



## Author

[Fanny Malmartel ](https://github.com/Fanny-Mlmrtl)
- contact: fannymalmartel@gmail.com


