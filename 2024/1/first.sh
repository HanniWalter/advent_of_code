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
sort -o temp/left temp/left
sort -o temp/right temp/right
echo "">>temp/left
echo "">>temp/right
paste -d " " temp/left temp/right > temp/temp
echo "">>temp/temp
while read line; do
  var1=$(echo $line | cut -f1 -d' ')
  var2=$(echo $line | cut -f2 -d' ')
  if [ $var1 ]; then
    diff=$(expr $var1 - $var2)
    if [ $diff -lt 0 ]; then
      diff=$(expr $diff \* -1)
    fi
    sum=$(expr $sum + $diff)
  fi
done < temp/temp
echo $sum