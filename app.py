
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/getdata',methods=["GET"])
def getdata():
    data = requests.get(
        'https://www.moneycontrol.com/stocks/marketstats/bsemact1/index.php').text

    soup = BeautifulSoup(data, 'lxml')

    # company names

    allCompanies = soup.find_all('span', class_='gld13 disin')

    companyNames = []

    for row in allCompanies:
        alink = row.find('a')
        companyNames.append(alink.text)

    # high, low, close, change

    tablerow = soup.find_all('tr')

    companyHigh = []
    companyLow = []
    companyClose = []
    companyChange = []

    for tr in tablerow:
        tablehigh = tr.find_all('td', attrs={'width': 175, 'align': 'right'})
        if len(tablehigh) == 0:
            continue
        for i in tablehigh:
            chigh = i.text.replace(',', '')
            companyHigh.append(chigh)
            break

        tablelow = tr.find_all('td', attrs={'width': 180, 'align': 'right'})
        if len(tablelow) == 0:
            continue
        for i in tablelow:
            clow = i.text.replace(',', '')
            companyLow.append(clow)
            break

        tableclose = tr.find_all(
            'td', attrs={'width': 185, 'align': 'right'})
        if len(tableclose) == 0:
            continue
        for i in tableclose:
            if i.has_attr('class'):
                cclose = i.text.replace(',', '')
                companyClose.append(cclose)
                break

        tablechange = tr.find_all(
            'td', attrs={'width': 175, 'align': 'right'})
        if len(tablechange) == 0:
            continue
        for i in tablechange:
            if i.has_attr('class'):
                cchange = i.text.replace(',', '')
                companyChange.append(cchange)
                break

    companyData = []

    for i in range(len(companyNames)):
        companyData.append({
            'company': companyNames[i],
            'High': float(companyHigh[i]),
            'Low': float(companyLow[i]),
            'Change': float(companyChange[i]),
            'close price': float(companyClose[i])
        })

    new_dict = sorted(companyData, key=lambda i: i['Change'], reverse=True)

    # for i in range(len(new_dict)):

    #     pprint.pprint(new_dict[i])
    #     print(' ')

    print(len(new_dict))
    return jsonify(data=new_dict), 201


if __name__ == '__main__':

    app.run(debug=True)
