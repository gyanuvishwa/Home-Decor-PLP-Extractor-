const https = require('https');
const fs = require('fs');

const slugs = [
// TEXTILE candidates
"furnishing-accessories-bags",
"furnishing-accessories-bottlecovers",
"furnishing-accessories-chaircovers",
"furnishing-accessories-mats",
"furnishing-accessories-padsandmats",
"furnishing-accessories-sofacovers",
"furnishing-accessories-yogamats",
"furnishing-appliancecovers-appliancecoversandmats",
"furnishing-bedding-bedcovers",
"furnishing-bedding-beddingsets",
"furnishing-bedding-bedsheets",
"furnishing-bedding-blanketsandquilts",
"furnishing-bedding-comforters",
"furnishing-bedding-cottonbedsheets",
"furnishing-bedding-diwanset",
"furnishing-bedding-doublebedsheets",
"furnishing-bedding-duvetandduvetcovers",
"furnishing-bedding-fittedbedsheets",
"furnishing-bedding-mattresstoppers",
"furnishing-bedding-pillowsandpillowcovers",
"furnishing-bedding-singlebedsheets",
"furnishing-bedding-throws",
"furnishing-curtains-blackoutcurtains",
"furnishing-curtains-blinds",
"furnishing-curtains-curtainrods",
"furnishing-curtains-decorativecurtains",
"furnishing-curtains-doorcurtains",
"furnishing-curtains-floralcurtains",
"furnishing-curtains-officecurtains",
"furnishing-curtains-rodsandaccessories",
"furnishing-curtains-sheercurtains",
"furnishing-curtains-windowcurtains",
"furnishing-cushions-chairpads",
"furnishing-cushions-cushioncovers",
"furnishing-cushions-cushionfilling",
"furnishing-cushions-filledcushions",
"furnishing-cushions-floorcushions",
"furnishing-floorcoverings-carpets",
"furnishing-floorcoverings-dhurries",
"furnishing-floorcoverings-doormats",
"furnishing-floorcoverings-mats",
"furnishing-floorcoverings-rugs",
"bathandlaundry-bath-bathmats",
"bathandlaundry-bath-mask",
"bathandlaundry-bath-robes",
"bathandlaundry-bath-towel",
"bathandlaundry-bathaccessories-showercurtains",
"kitchen-kitchenlinens-aprons",
"kitchen-kitchenlinens-covers",
"kitchen-kitchenlinens-gloves",
"kitchen-kitchenlinens-kitchentowels",
"kitchen-kitchenlinens-potholders",
"kitchen-kitchenlinens-runnersandmats",
"kitchen-kitchenlinens-sets",
"livingroom-sofas-sofacovers",
"diningroom-diningchairs-diningchaircovers",
// STORAGE candidates
"kitchen-storageandcontainers-bags",
"kitchen-storageandcontainers-bottles",
"kitchen-storageandcontainers-breadbins",
"kitchen-storageandcontainers-containersandjars",
"kitchen-storageandcontainers-drawerorganisers",
"kitchen-storageandcontainers-dustbins",
"kitchen-storageandcontainers-flask",
"kitchen-storageandcontainers-glassbottles",
"kitchen-storageandcontainers-glassjars",
"kitchen-storageandcontainers-lunchboxandbags",
"kitchen-storageandcontainers-organisers",
"kitchen-storageandcontainers-saltandpeppershakers",
"kitchen-storageandcontainers-trays",
"bathandlaundry-bathaccessories-storageandmirrors",
"bathandlaundry-laundry-laundrybinsandbaskets",
"bathandlaundry-laundry-storage",
"bathandlaundry-laundry-wicker",
"bathandlaundry-laundry-hangersandhooks",
"bathandlaundry-laundry-dustbins",
"livingroom-shoeracks-diyfabricshoeracks",
"livingroom-shoeracks-shoecabinets",
"livingroom-shoeracks-shoecabinetswithseating",
"livingroom-shoeracks-shoeopenshelves",
"livingroom-wallshelves-utilityshelves",
"livingroom-wallshelves-utilitystand",
"livingroom-benchandstools-storagebenches",
"livingroom-benchandstools-storagestools",
];

function fetchOne(slug) {
  return new Promise((resolve) => {
    const url = `https://www.homecentre.in/in/en/c/${slug}`;
    https.get(url, {headers: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36'}}, (res) => {
      let body = '';
      res.on('data', (c) => body += c);
      res.on('end', () => {
        try {
          const m = body.match(/<script id="__NEXT_DATA__" type="application\/json">([\s\S]*?)<\/script>/);
          if (!m) { resolve({slug, status: res.statusCode, error: 'no NEXT_DATA'}); return; }
          const data = JSON.parse(m[1]);
          const state = data.props.initialState;
          const h1 = state.metaDataReducer && state.metaDataReducer.data && state.metaDataReducer.data.h1;
          const listing = state.unbxdListingPageReducer && state.unbxdListingPageReducer.data;
          const numberOfProducts = listing && listing.response && listing.response.numberOfProducts;
          const pFilter = listing && listing.searchMetaData && listing.searchMetaData.queryParams && listing.searchMetaData.queryParams.p;
          const breadcrumbs = state.unbxdCategoryDataReducer && state.unbxdCategoryDataReducer.data && state.unbxdCategoryDataReducer.data.breadcrumbs;
          resolve({slug, status: res.statusCode, h1, numberOfProducts, pFilter, breadcrumbs});
        } catch (e) {
          resolve({slug, status: res.statusCode, error: e.message});
        }
      });
    }).on('error', (e) => resolve({slug, error: e.message}));
  });
}

async function main() {
  const results = [];
  for (const slug of slugs) {
    const r = await fetchOne(slug);
    results.push(r);
    console.log(slug, '=>', JSON.stringify(r));
  }
  fs.writeFileSync('batch_results.json', JSON.stringify(results, null, 1));
}
main();
