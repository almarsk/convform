cd convfront
npm run build

if [ ! -d "assets" ]; then
    mkdir assets
fi

cp -r dist/assets/* ../assets

if [ ! -d "templates" ]; then
    mkdir templates
fi

cp dist/index.html ../templates
cd ..
