from flask import Flask, request, render_template, g
import pprint
import xml.sax
import uuid
import os
import subprocess
from io import StringIO

app = Flask(__name__)

class MyObject:
  def __init__(self):
    self.data = ""
    self.chars = ""

  def __repr__(self):
    return "%s" % (self.data)


class MyContentHandler(xml.sax.ContentHandler):
  def __init__(self, object):
    xml.sax.ContentHandler.__init__(self)
    self.object = object

  def startElement(self, name, attrs):
    self.chars = ""

  def endElement(self, name):
    if name=="name":
     self.object.data += self.chars +"\r\n"

  def characters(self, content):
    self.chars += content

@app.route("/")
def index():

  return render_template('xxe-standard.html')

@app.route("/standard", methods=['POST'])
@app.route("/standard/", methods=['POST'])
def standard():
  obj = MyObject()
  xmlin = request.form['xml']

  try:
    contentParser = MyContentHandler(obj)
    xml.sax.parseString(xmlin, contentParser)
  except:
    return render_template('xxe-error.html')

  return render_template('xxe-response.html', xml=obj.__repr__())

@app.route("/blind", methods=['POST'])
@app.route("/blind/", methods=['POST'])
def blind():
  obj = MyObject()
  xmlin = request.form['xml']

  try:
    contentParser = MyContentHandler(obj)
    xml.sax.parseString(xmlin, contentParser)
  except:
    return render_template('xxe-error.html')

  return render_template('xxe-response.html', xml="Thanks for submitting!")

@app.route("/cdata", methods=['POST'])
@app.route("/cdata/", methods=['POST'])
def cdata():
  xmlin = request.form['xml'].encode('utf-8')

  #write to a file
  filename = str(uuid.uuid4())
  filename += ".xmltmp"
  f = open(filename, "w")
  f.write(xmlin)
  f.flush()
  f.close

  #send the xml content to our vulnerable parse 
  data = subprocess.check_output("java parse %s & sleep 2 && rm %s" % (filename, filename), shell=True)

  return render_template('xxe-response.html', xml=data)

@app.route("/remote", methods=['POST'])
@app.route("/remote/", methods=['POST'])
def remote():
  xmlin = request.form['xml'].encode('utf-8')

  #write to a file
  filename = str(uuid.uuid4())
  filename += ".xmltmp"
  f = open(filename, "w")
  f.write(xmlin)
  f.flush()
  f.close

  #send the xml content to our vulnerable parse 
  os.system("java parse %s & sleep 2 && rm %s" % (filename, filename))


  return render_template('xxe-response.html', xml="Thanks for submitting!")


if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
