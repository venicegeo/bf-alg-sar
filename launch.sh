git clone https://github.com/venicegeo/bf-py
mkdir bf
cp -r bf-py/* bf/
echo "" > bf/__init__.py
#pip install -r requirements.txt
nosetests test_bf-algo-sar.py
