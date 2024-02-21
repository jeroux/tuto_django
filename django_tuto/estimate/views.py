from django.shortcuts import render

import pandas as pd
import numpy as np
import json,pickle
from fastapi.encoders import jsonable_encoder
from regression.features import feature_engineering
from regression.preprocessing import encode_dataframe
import os

from .forms import PropertyForm


# Create your views here.
def mainPage(request):
    if request.method == "GET":
        form = PropertyForm()
        return render(request, "main.html", {"form": form})
    
    form = PropertyForm(request.POST)

    if not form.is_valid():
        return render(request, "main.html", {"form": form})
    
    config=json.load(open("resources/config.json"))

    model=pickle.load(open(config['model_path'],"rb"))
    encoder_struct=pickle.load(open(config["encoder_path"],"rb"))
    print("model and encoders loaded!")
    data = {
        "PostalCode": form.cleaned_data["PostalCode"],
        "TypeOfProperty": form.cleaned_data["TypeOfProperty"],
        "TypeOfSale": form.cleaned_data["TypeOfSale"],
        "Kitchen": form.cleaned_data["Kitchen"],
        "StateOfBuilding": form.cleaned_data["StateOfBuilding"],
        "Bedrooms": form.cleaned_data["Bedrooms"],
        "SurfaceOfGood": form.cleaned_data["SurfaceOfGood"],
        "NumberOfFacades": form.cleaned_data["NumberOfFacades"],
        "LivingArea": form.cleaned_data["LivingArea"],
        "GardenArea": form.cleaned_data["GardenArea"],
    }

    df=pd.DataFrame.from_dict(jsonable_encoder(data),orient="index").transpose()
    df=df.reindex(columns=["PostalCode"]+model.feature_names_in_.tolist())
    df=feature_engineering(df)
    df.drop("PostalCode",axis=1,inplace=True)
    df,e=encode_dataframe(df,encoder_struct)
    score=np.abs(model.predict(df))

    return render(request, "main.html", {"form": form, "estimation": str(round(score[0], 2))})