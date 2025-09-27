import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ---- Calorie Formula (Mifflin–St Jeor) ----
def mifflin_bmr(weight, height, age, sex):
    if sex == "male":
        return 10 * weight + 6.25 * height - 5 * age + 5
    return 10 * weight + 6.25 * height - 5 * age - 161

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        age = int(request.form["age"])
        sex = request.form["sex"]
        goal = request.form["goal"]

        bmr = mifflin_bmr(weight, height, age, sex)
        tdee = bmr * 1.55  # moderate activity by default

        if goal == "bulking":
            calories = tdee + 300
        elif goal == "cutting":
            calories = tdee - 500
        else:
            calories = tdee

        # Example food recommendations
        if goal == "bulking":
            foods = ["Chicken breast", "Brown rice", "Oats", "Almonds"]
        elif goal == "cutting":
            foods = ["Egg whites", "Broccoli", "Grilled fish", "Quinoa"]
        else:
            foods = ["Balanced salad", "Lean meat", "Whole grains", "Fruits"]

        result = {
            "bmr": round(bmr, 1),
            "tdee": round(tdee, 1),
            "calories": round(calories, 1),
            "foods": foods
        }
        return render_template("result.html", result=result)
    return render_template("index.html")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    prediction = None
    filename = None
    if request.method == "POST":
        file = request.files["image"]
        if file and file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(path)

            # ---- ML STUB ----
            # TODO: Replace with actual model inference
            # Example: prediction = predict_weight(path)
            prediction = "Predicted weight: ~70 kg (demo)"

    return render_template("upload.html", prediction=prediction, filename=filename)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
