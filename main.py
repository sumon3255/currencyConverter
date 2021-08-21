from flask import Flask,render_template,request
import  requests
import json

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def hello_world():
   if request.method == "POST":
         url = "https://api.exchangerate-api.com/v4/latest/USD"
         response = requests.get(url)
         data = response.json()

         country = data['rates']
         class CurrencyConverter:
                def __init__(self,url):
                        self.data = requests.get(url).json()
                        self.currencies = self.data['rates']

                def convert(self,fromcurrency,tocurrency,amount):
                    if fromcurrency != 'USD':
                        amount = float(amount)/float(self.currencies[fromcurrency])

                    amount = round(float(amount) *float(self.currencies[tocurrency]),4)

                    return amount

         formcurrency = request.form['formcurrency']   
         tocurrency = request.form['tocurrency'] 
         amount =  request.form['amount'] 
         converter = CurrencyConverter(url)
         finalconv = converter.convert(formcurrency,tocurrency,amount)
         return render_template("index.html",formcurrency=formcurrency,tocurrency=tocurrency,amount=amount,finalconv=finalconv,country=country)

   url = "https://api.exchangerate-api.com/v4/latest/USD"
   data = requests.get(url).json()
   country = data['rates']
    
   return render_template("index.html",country=country)

if __name__ == '__main__':
    app.run(debug=True)
    