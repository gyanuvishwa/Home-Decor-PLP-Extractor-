const https = require('https');
const fs = require('fs');

const slugs = [
"furnishing-accessories",
"furnishing-appliancecovers",
"furnishing-bedding",
"furnishing-curtains",
"furnishing-cushions",
"bathandlaundry-bath",
"bathandlaundry-bathaccessories",
"bathandlaundry-laundry",
"kitchen-kitchenlinens",
"kitchen-storageandcontainers",
"livingroom-shoeracks",
"livingroom-wallshelves",
"livingroom-benchandstools",
"diningroom-diningchairs",
"livingroom-sofas",
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
          const facets = listing && listing.facets && listing.facets.text && listing.facets.text.list;
          const catFacet = facets && facets.find(f => f.facetName === 'categoryFacetValue_uFilter');
          resolve({slug, status: res.statusCode, h1, numberOfProducts, catFacetValues: catFacet ? catFacet.values : null});
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
    console.log('===', slug, '===');
    console.log('h1:', r.h1, '| total:', r.numberOfProducts);
    if (r.catFacetValues) {
      for (let i = 0; i < r.catFacetValues.length; i += 2) {
        const code = r.catFacetValues[i].split('#')[0];
        const name = r.catFacetValues[i].split('#')[1];
        const count = r.catFacetValues[i+1];
        console.log('  ', code, '|', name, '|', count);
      }
    } else {
      console.log('  NO FACET / ERROR:', r.error);
    }
  }
  fs.writeFileSync('facet_results.json', JSON.stringify(results, null, 1));
}
main();
