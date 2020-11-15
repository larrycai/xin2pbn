# xin2pbn

xinrui bridge online url to pbn converter

xinrui url like [this](http://www.xinruibridge.com/deallog/DealLog.html?bidlog=1C,1D,P%3B1S,P,2C,P%3B2H,P,2S,P%3B4S,P,P,P%3B&playlog=W:KC,4C,9C,8C%3BW:5C,TC,AC,2C%3BE:7C,3S,3C,JC%3BS:3H,6H,QH,2H%3BN:AH,5H,4H,8H%3BN:AD,5D,6D,2D%3BN:KD,7D,9H,QD%3BN:JD,8D,7S,4D%3BS:TH,KH,9S,7H%3BN:TD,6C,AS,QC%3BS:JH,2S,JS,4S%3BN:3D,6S,8S,KS%3BW:5S,9D,TS,QS%3B&deal=K52.K86.Q42.KQ53%20J9.AQ.AKJT93.JT4%20T64.752.875.A976%20AQ873.JT943.6.82&vul=All&dealer=W&contract=4S&declarer=S&wintrick=10&score=620&str=%E9%94%A6%E6%A0%87%E8%B5%9B%20%E7%AC%AC5%E8%BD%AE%20%E7%89%8C%E5%8F%B7%204/12&dealid=442379062&pbnid=76718646&from=singlemessage&isappinstalled=0), it can be converted to standard pbn files

# Usage

````
pip install xin2pbn
xin2pbn "url"
xin2pbn "local.html"
````

# Development

````
# docker run -it  -v $PWD:/app  -w /app python:3.8  bash
# python3 -m pip install --user --upgrade twine
# python3 setup.py sdist clean
# python3 setup.py sdist bdist_wheel
# python3 -m twine upload --skip-existing --verbose dist/*
````


<TODO>
* Web interface
* convert to js to be used by anyone

# Reference

* http://www.tistis.nl/pbn/
* http://xinruibridge.com/