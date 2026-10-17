from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from .forms import PredictionForm
from .predictor import MODEL_MAE, MODEL_R2, predict_tip


def index(request):
    return render(
        request,
        "ml_app/index.html",
        {"form": PredictionForm(), "mae": MODEL_MAE, "r2": MODEL_R2},
    )


@require_POST
def predict(request):
    form = PredictionForm(request.POST)
    if not form.is_valid():
        errors = {field: msgs[0] for field, msgs in form.errors.items()}
        return JsonResponse({"ok": False, "errors": errors}, status=400)
    return JsonResponse({"ok": True, **predict_tip(form.cleaned_data)})
