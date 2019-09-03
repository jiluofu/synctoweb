echo $1;
rm -rf $1/img/output;
mkdir $1/img/output;
echo "output:"$1
echo "resize photos1"
cd $1/img
find . -type f -name "*.jpg" -o -name "*.JPG"|xargs -I {} convert -resize 1240x1240 {} output/{}
cp output/* .
rm -rf output
# echo "compress photos"
# cd output
# find . -type f -name "*.jpg" -o -name "*.JPG"|xargs -I {} jpegoptim  -m80 {}


