from flask import Flask, render_template, request
from deepface import DeepFace
import os

app = Flask(__name__)

def get_uplifting_sentence(emotion):
    uplifting_sentences = {

    'angry': "Hey there! Take a deep breath. I know it's tough, but trust me, everything will be okay. Remember what they say, 'This too shall pass.' You've got this, Control your anger and drink some water or count upto 10 and see the magic ✨.",
    'disgust': "Hey, I see you're feeling a bit disgusted. It's alright, we all have those moments. Let's try to focus on the positive things in your life 😊 . Remember, every cloud has a silver lining. Hang in there!",
    'fear': "Hey, I can see fear creeping in, but you know what? You're stronger than you think 💪. Face your fears head-on with courage and determination. You've conquered challenges before, and you'll do it again. I believe in you!",
    'happy': "Well, look at that smile! It's great to see you happy. Keep celebrating 🎉 those small victories and finding joy in the present moment. As they say, 'Happiness is not a destination, it's a journey.' Enjoy the ride!",
    'sad': "Hey, you look a bit down. It's okay to feel sad sometimes, you know? Just remember, brighter days are ahead 🌟. Keep your chin up, my friend. As someone wise once said, 'The sun will shine after every storm.'",
    'surprise': "Whoa! That was unexpected 😲! But hey, life is full of surprises, right? Let's embrace this moment and stay open to new possibilities . You never know what wonderful things might come your way next!",
    'neutral': "Hey, you seem pretty chill right now 😎. Finding peace in the present moment, huh? That's awesome. Remember to take care of yourself and enjoy this moment of tranquility. Sometimes, a little 'me time' goes a long way."
    }

    return uplifting_sentences.get(emotion, "Stay positive and keep smiling!")

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return render_template('index.html', message='No file part')
    
    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', message='No selected file')
    
    if file:
        filename = file.filename
        file_path = os.path.join("uploads", filename)
        file.save(file_path)
        
        try:
            result = DeepFace.analyze(file_path, actions=['gender', 'age', 'emotion'])
            gender = result[0]['dominant_gender']
            age = result[0]['age']
            emotion = result[0]['dominant_emotion']
            
            uplifting_sentence = get_uplifting_sentence(emotion)
            
            os.remove(file_path)
            
            return render_template('result.html', filename=filename, gender=gender, age=age, uplifting_sentence=uplifting_sentence)
        except Exception as e:
            os.remove(file_path)
            return render_template('index.html', message='Error analyzing image: {}'.format(str(e)))

if __name__ == '__main__':
    app.run(debug=True)
