from flask import Flask, request, render_template,flash,redirect,session,abort,jsonify
from models import Model
from depression_detection_tweets import DepressionDetection
from TweetModel import process_message
import os

app = Flask(__name__)


@app.route('/')
def root():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else :
        flash('wrong password!')
    return root()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return root()


@app.route("/sentiment")
def sentiment():
    return render_template("sentiment.html")

@app.route("/quizBased")
def quizBased():
    return render_template("quizbase.html")    



@app.route("/predictSentiment", methods=["POST"])
def predictSentiment():
    message = request.form['form10']
    pm = process_message(message)
    result = DepressionDetection.classify(pm, 'bow') or DepressionDetection.classify(pm, 'tf-idf')
    suggestion = DepressionDetection.classify(pm, 'bow') or DepressionDetection.classify(pm, 'tf-idf')
    return render_template("tweetresult.html",result=result, suggestion=suggestion,)


@app.route('/predict', methods=["POST"])
def predict():
    q1 = int(request.form['a1'])
    q2 = int(request.form['a2'])
    q3 = int(request.form['a3'])
    q4 = int(request.form['a4'])
    q5 = int(request.form['a5'])
    q6 = int(request.form['a6'])
    q7 = int(request.form['a7'])
    q8 = int(request.form['a8'])
    q9 = int(request.form['a9'])
    q10 = int(request.form['a10'])

    values = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]
    model = Model()
    classifier = model.svm_classifier()
    prediction = classifier.predict([values])
    if prediction[0] == 0:
            result = 'Your Depression test result : No Depression'
            suggestion = 'Working to improve the quality of interpersonal relationships can reduce feelings of loneliness while offering some protection against depression. First, Try to meditate. Second, Listen to music'
    if prediction[0] == 1:
            result = 'Your Depression test result : Mild Depression'
            suggestion = 'Use writing or journaling to express your feelings Consider writing or journaling about what you’re experiencing. Then, when the feelings lift, write about that, too. Research has shown that keeping a journal can be a beneficial add-on method for managing mental health conditions. Do the opposite of what the ‘depression voice’ suggests The automatic, unhelpful voice in your head may talk you out of self-help. However, if you can learn to recognize it, you can learn to work through it. If you believe an event won’t be fun or worth your time, say to yourself, “You might be right, but it’ll be better than just sitting here another night.” You may soon see the automatic thought isn’t always helpful.'
    if prediction[0] == 2:
            result = 'Your Depression test result : Moderate Depression'
            suggestion = 'Exercise and eat healthfully. Your mood can be significantly improved by engaging in moderate exercise five times each week for 30 minutes each session. When exercising at a moderate intensity, it becomes challenging to sing from the diaphragm. Pay close attention to how the foods and beverages you are consuming affect your mood. You dont have to follow fad diets, however anyone who regularly binges on carbohydrates, junk food, and sports drinks can experience depression. Keep in mind the benefits of moderation.'
    if prediction[0] == 3:
            result = 'Your Depression test result : Moderately severe Depression'
            suggestion = ' Do the opposite of what the ‘depression voice’ suggests The automatic, unhelpful voice in your head may talk you out of self-help. However, if you can learn to recognize it, you can learn to work through it. If you believe an event won’t be fun or worth your time, say to yourself, “You might be right, but it’ll be better than just sitting here another night.” You may soon see the automatic thought isn’t always helpful.'
    if prediction[0] == 4:
            result = 'Your Depression test result : Severe Depression'
            suggestion = 'Consider clinical treatment You may also find it helpful to speak to a professional about what you’re going through. A  general practitioner may be able to refer you to a therapist or other specialist. They can assess your symptoms and help develop a clinical treatment plan tailored to your needs. This may include various options, such as medication and therapy. Finding the right treatment for you may take some time, so be open with your doctor or healthcare professional about what is and isn’t working. They’ll work with you to find the best option.'

    return render_template("result.html", result=result, suggestion=suggestion,)

app.secret_key = os.urandom(12)
app.run(port=5987, host='0.0.0.0', debug=True)