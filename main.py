from flask import Flask, request, redirect, url_for, abort, render_template
from werkzeug import secure_filename
import pytesseract
from gtts import gTTS

app = Flask(__name__)

def prep_audio(fname):
    text = pytesseract.image_to_string("./static/images/%s"%fname)
    audobj = gTTS(text=text, lang='en')
    audname = fname.rstrip(".jpegpng")+".mp3"
    audobj.save("./static/audios/%s"%audname)
    return audname, text

@app.route("/", methods=['POST', 'GET'])
def main():
    if request.method=='POST':
        f = request.files.get('file')
        if f is None:
            return "No image uploaded", 400
        imgname = secure_filename(f.filename)
        try:
            f.save("./static/images/%s"%imgname)
        except:
            return "No image uploaded", 400
        audname, text = prep_audio(imgname)
        return redirect(url_for("play", image=imgname, audio=audname, text=text))
    return render_template('index.html')

@app.route("/play/")
def play():
    image = request.args.get('image')
    audio = request.args.get('audio')
    text = request.args.get('text')
    if not image or not audio or not text:
        abort(404)
    return render_template('read_it.html', audio=audio, image=image, text=text)

if __name__=="__main__":
    app.run(debug=True)
