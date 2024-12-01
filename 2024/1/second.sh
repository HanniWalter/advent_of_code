file="input"
sum=0
touch temp/input
touch temp/left
touch temp/right
touch temp/temp
echo "">temp/left
echo "">temp/right
echo "">temp/temp
cat $file > temp/input
echo "">>temp/input
while read line; do
  var1=$(echo $line | cut -f1 -d' ')
  var2=$(echo $line | cut -f2 -d' ')
  echo $var1 >> temp/left
  echo $var2 >> temp/right
done < "temp/input"

while read line; do
  if [ $line ]; then
    cat temp/right | grep -w $line > temp/temp
    while read line2; do
      if [ $line2 ]; then
        sum=$(expr $sum + $line2)
      fi
    done < temp/temp
  fi
done < temp/left
echo $sum