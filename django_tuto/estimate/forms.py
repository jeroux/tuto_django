from django import forms

class PropertyForm(forms.Form):
    PostalCode = forms.IntegerField(label="Postal Code", min_value=1000, max_value=9999)
    TypeOfProperty = forms.ChoiceField(label="Type of Property", choices=[(0, "House"), (1, "Apartment")])
    TypeOfSale = forms.ChoiceField(label="Type of Sale", choices=[(0, "Normal"), (1, "Auction")])
    Kitchen = forms.ChoiceField(label="Kitchen", choices=[("installed", "Installed"), ("usa installed", "USA Installed"), ("semi equipped", "Semi Equipped"), ("usa semi equipped", "USA Semi Equipped"), ("hyper equipped", "Hyper Equipped"), ("usa hyper equipped", "USA Hyper Equipped")], required=False)
    StateOfBuilding = forms.ChoiceField(label="State of Building", choices=[("to be done up", "To be done up"), ("to restore", "To restore"), ("to renovate", "To renovate"), ("good", "Good"), ("just renovated", "Just renovated"), ("as new", "As new")], required=False)
    Bedrooms = forms.IntegerField(label="Number of Bedrooms", min_value=0, max_value=10, required=False)
    SurfaceOfGood = forms.FloatField(label="Surface of Good", min_value=0, max_value=10000, required=False)
    NumberOfFacades = forms.IntegerField(label="Number of Facades", min_value=0, max_value=10, required=False)
    LivingArea = forms.FloatField(label="Living Area", min_value=0, max_value=10000)
    GardenArea = forms.FloatField(label="Garden Area", min_value=0, max_value=10000, required=False)
