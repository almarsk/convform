
if [ ! -d "assets" ]; then
    mkdir assets
fi

cd convfront
npm run build

rm assets/*.js
rm assets/*.css

cp -r dist/assets/* ../assets

if [ ! -d "templates" ]; then
    mkdir templates
fi

cp dist/index.html ../templates
cd ..
