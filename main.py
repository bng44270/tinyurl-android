#qpy:webapp:TinyURLClientAndroid
#qpy://127.0.0.1:8080/

from flask import Flask, render_template, redirect, url_for, request
import re
import requests

def GetTinyURL(longurl):
  r = requests.post("http://tinyurl.com/create.php", data={'url': str(longurl)})
  if r.status_code == 200:
    return re.sub("\".*$","",re.sub("^.*text=\"","",str([a for a in r.text.split('\n') if a.find("data-clipboard-text") > 0][0])))
  else:
    return False

app = Flask(__name__)

@app.route("/")
def GetRoot():
  return render_template("root.html")
  
@app.route("/gettinyurl/", methods = ["POST"])
def TunyURL():
  longurl = str(request.form['longurl'])

  tinyurl = GetTinyURL(longurl)

  if tinyurl:
    return render_template("root.html", tinyurl = tinyurl, longurl = longurl)
  else:
    return render_template("error.html", errortext="Bad HTTP Response")
  
@app.errorhandler(500)
def internal_error(exception):
  app.logger.error(exception)
  return render_template('error.html', errortext = exception), 500

@app.route("/__exit", methods = ['GET','HEAD'])
def __exit():
  StopFlask()

@app.route("/__ping", methods=['GET','HEAD'])
def __ping():
  return "ok"

app.run("0.0.0.0",8080)
