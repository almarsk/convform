
# make dirs for flask if they aren't there
if [ ! -d "templates" ]; then
    mkdir templates
fi
if [ ! -d "assets" ]; then
    mkdir assets
fi

# remove previous content
rm assets/*.js
rm assets/*.css

# build current version of frontend
cd convfront
npm run build

# expose bundle to flask
cp -r dist/assets/* ../assets
cp dist/index.html ../templates

cd ..
