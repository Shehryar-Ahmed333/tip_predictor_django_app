from django import forms

# Choices match the labels in the original tips dataset.
SEX_CHOICES = [("Female", "Female"), ("Male", "Male")]
SMOKER_CHOICES = [("No", "No"), ("Yes", "Yes")]
DAY_CHOICES = [("Thur", "Thursday"), ("Fri", "Friday"), ("Sat", "Saturday"), ("Sun", "Sunday")]
TIME_CHOICES = [("Lunch", "Lunch"), ("Dinner", "Dinner")]


class PredictionForm(forms.Form):
    """Validates the six inputs the XGBoost model was trained on."""

    total_bill = forms.FloatField(label="Total bill ($)", min_value=1, max_value=500)
    sex = forms.ChoiceField(label="Payer's sex", choices=SEX_CHOICES)
    smoker = forms.ChoiceField(label="Smoking section", choices=SMOKER_CHOICES)
    day = forms.ChoiceField(label="Day", choices=DAY_CHOICES)
    time = forms.ChoiceField(label="Meal", choices=TIME_CHOICES)
    size = forms.IntegerField(label="Party size", min_value=1, max_value=12)
