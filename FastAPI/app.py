import joblib
from xmlrpc.client import Boolean
import uvicorn
import pandas as pd 
from pydantic import BaseModel
from typing import Literal, List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import json
from typing import Literal, List, Union

# description will apear in the doc

description = """
## Predict the rental price per day of your car
"""

# initialise API object
app = FastAPI(
    title="GETAROUND API",
    description=description,
    version="1.0",
    contact={
        "name": "Fanny Malmartel",
        "url": "https://github.com/Fanny-Mlmrtl",
    },
    openapi_tags= [
    {
        "name": "Home",
        "description": "🚗 Get Around API homepage."
    },
    {
        "name": "Predicts",
        "description": "🚕 Get Around API with POST or GET method."
    }
]
)

html = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>🚗 Get Around API</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="🚗 Get Around API">
    <meta name="author" content="Fanny Malmartel">
    <!-- Le styles -->
    <link href="https://getbootstrap.com/2.3.2/assets/css/bootstrap.css" rel="stylesheet">
    <style type="text/css">
      body {
        padding-top: 20px;
        padding-bottom: 40px;
      }
      /* Custom container */
      .container-narrow {
        margin: 0 auto;
        max-width: 700px;
      }
      .container-narrow > hr {
        margin: 30px 0;
      }
      /* Main marketing message and sign up button */
      .jumbotron {
        margin: 60px 0;
        text-align: center;
      }
      .jumbotron h1 {
        font-size: 72px;
        line-height: 1;
      }
      .jumbotron .btn {
        font-size: 21px;
        padding: 14px 24px;
      }
      /* Supporting marketing content */
      .marketing {
        margin: 60px 0;
      }
      .marketing p + h4 {
        margin-top: 28px;
      }
    </style>
    <link href="https://getbootstrap.com/2.3.2/assets/css/bootstrap-responsive.css" rel="stylesheet">
    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="https://getbootstrap.com/2.3.2/assets/js/html5shiv.js"></script>
    <![endif]-->
    <!-- Fav and touch icons -->
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="https://getbootstrap.com/2.3.2/assets/ico/apple-touch-icon-144-precomposed.png">
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="https://getbootstrap.com/2.3.2/assets/ico/apple-touch-icon-114-precomposed.png">
      <link rel="apple-touch-icon-precomposed" sizes="72x72" href="https://getbootstrap.com/2.3.2/assets/ico/apple-touch-icon-72-precomposed.png">
                    <link rel="apple-touch-icon-precomposed" href="https://getbootstrap.com/2.3.2/assets/ico/apple-touch-icon-57-precomposed.png">
                                   <link rel="shortcut icon" href="https://getbootstrap.com/2.3.2/assets/ico/favicon.png">
  </head>
  <body>
    <div class="container-narrow">
      <div class="masthead">
        <ul class="nav nav-pills pull-right">
          <li class="active"><a href="#">Home</a></li>
          <li><a href="/docs#/">Docs</a></li>
        </ul>
        <h3 class="muted">Project Get Around</h3>
      </div>
      <hr>
      <div class="jumbotron">
        <h1>Project 🚗<br>Get Around API</h1>
        <p class="lead">Predict the rental price per day of your car. This <b>/</b> is the most simple and default endpoint. If you want to learn more, check out documentation of the api at <b>/docs</b></p>
        <a class="btn btn-large btn-success" href="/docs#/">See /docs</a>
      </div>
      <hr>
      <div class="footer">
        <p>Projet <a href="https://github.com/Fanny-Mlmrtl/Bloc_5">Bloc n°5</a></p>
        <p>This page come from bootcamp template <a href="https://getbootstrap.com/2.3.2/examples/marketing-narrow.html#">on this page</a></p>
      </div>
    </div> <!-- /container -->
    <!-- Le javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://getbootstrap.com/2.3.2/assets/js/jquery.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-transition.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-alert.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-modal.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-dropdown.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-scrollspy.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-tab.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-tooltip.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-popover.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-button.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-collapse.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-carousel.js"></script>
    <script src="https://getbootstrap.com/2.3.2/assets/js/bootstrap-typeahead.js"></script>
  </body>
</html>
"""

@app.get("/", tags=["Home"]) # here we categorized this endpoint as part of "Name_1" tag
async def get():
    return HTMLResponse(html)


# tags to easily sort roots
tags_metadata = [
    {
        "name": "Preview",
        "description": "Preview of the existing data",
    },

    {
        "name": "Prediction",
        "description": "Prediction of the rental price based on a machine learning model"
    }
]


# Define features used in machine learning
class PredictionFeatures(BaseModel):
    model_key: str = "Mercedes"
    mileage: int = 181672
    engine_power: int = 105
    fuel: str = "diesel"
    paint_color: str = "white"
    car_type: str = "hatchback"
    private_parking_available: bool = True
    has_gps: bool = True
    has_air_conditioning: bool = False
    automatic_car: bool = False
    has_getaround_connect: bool = True
    has_speed_regulator: bool = False
    winter_tires: bool = True


@app.get("/Preview", tags=["Preview"])
async def random_data(rows: int= 3):
    try:
        if rows < 21 :
            data = pd.read_csv("https://full-stack-assets.s3.eu-west-3.amazonaws.com/Deployment/get_around_pricing_project.csv")
            sample = data.sample(rows)
            response0= sample.to_json(orient='records')
        else:
            response0 = json.dumps({"message" : "Error! Please select a row number not more than 20."})
    except:
            response0 = json.dumps({"message" : "Error! Problem in accessing to historical data."})
    return response0


@app.post("/Prediction", tags=["Prediction"])
async def predict(predictionFeatures: PredictionFeatures):
    # Read data 
    df = pd.DataFrame(dict(predictionFeatures), index=[0])
    #print(df)

    # Load the models from local
    model_lr  = 'model.joblib'
    regressor = joblib.load(model_lr)
    prediction = regressor.predict(df)

    # Format response
    response = {"prediction": prediction.tolist()[0]}
    return response

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000, debug=True, reload=True)
