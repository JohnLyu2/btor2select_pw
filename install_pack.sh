cd btor2kwcount/
./configure.sh
cd build
make
cd ../..
mkdir localpips
pip3.10 install joblib==1.4.2 --target=./localpips
pip3.10 install numpy==1.26.4 --target=./localpips
pip3.10 install xgboost==2.0.3 --target=./localpips
tar -czvf ../btor2select_pw.tar.gz .