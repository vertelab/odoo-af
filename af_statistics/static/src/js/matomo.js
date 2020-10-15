console.log("Matomo script commencing...");
console.log("0a");

if (_mtm) {
  console.log("Matomo declared.");

  const entry1 = {
    "mtm.startTime": new Date().getTime(),
    "event": "mtm.Start"
  };

  const entry2 = {
    "mtm.startTime": new Date().getTime(),
    "timestamp": new Date(),
    "event": "crm_test"
  };

  // _mtm.push(entry1);
  // _mtm.push(entry2);
  console.log("Matomo script completed.", entry1, entry2);
} else {
  console.error("Matomo global object not found.");
}




// var matomo_data = matomo_data || [];
// const matomo_entry = {
//   "mtm.startTime": new Date().getTime(),
//   "event": "mtm.Start"
// };
// matomo_data.push(matomo_entry);

// const html = document;
// const matomo_tag = html.createElement("script");
// const script_tag = html.getElementsByTagName("script")[0];

// matomo_tag.type = "text/javascript";
// matomo_tag.async = true;
// matomo_tag.defer = true;
// // matomo_tag.src = "https://af-staging.analytics.elx.cloud/js/container_ew8X7e8B.js";
// // matomo_tag.src = "http://af-staging.analytics.elx.cloud/js/container_ew8X7e8B.js";
// // matomo_tag.src = "af-staging.analytics.elx.cloud/js/container_ew8X7e8B.js";
// // matomo_tag.src = "//af-staging.analytics.elx.cloud/js/container_ew8X7e8B.js";
// matomo_tag.src = "//af-staging.analytics.elx.cloud/js/container_ew8X7e8B.js";

// // console.log("Matomo script completed.", matomo_tag);
// script_tag.parentNode.insertBefore(matomo_tag, script_tag);

// console.log("Matomo script completed.", matomo_data);



