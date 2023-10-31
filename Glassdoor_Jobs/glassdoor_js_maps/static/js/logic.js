
// Creating the map object
let myMap = L.map("map", {
  center: [37.09024, -95.712891],
  zoom: 5
});

// Adding the tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(myMap);

// File to get the GeoJSON data.
let link = "static/data/gz_2010_us_040_00_20m_states.json";

let West = ['Washington', 'Montana', 'Oregon', 'Idaho', 'Wyoming', 'California', 'Nevada', 'Utah', 'Colorado', 'Alaska', 'Hawaii']
let Southwest = ['Arizona', 'New Mexico', 'Oklahoma', 'Texas']
let Midwest = ['North Dakota', 'South Dakota', 'Nebraska', 'Kansas', 'Minnesota', 'Iowa', 'Missouri', 'Wisconsin', 'Illinois', 'Michigan', 'Indiana', 'Ohio']
let Southeast = ['Kentucky', 'West Virginia', 'Virginia', 'Arkansas', 'Tennessee', 'North Carolina', 'South Carolina', 'Georgia', 'Alabama', 'Mississippi', 'Louisiana', 'Florida']
let Northeast = ['Pennsylvania', 'New York', 'Vermont', 'Maine', 'New Hampshire', 'Massachusetts', 'Rhode Island', 'Connecticut', 'New Jersey', 'Delaware', 'Maryland', 'Washington DC']

// Function to determine the color of a region based on the states in the region
function chooseColor(State) {
  if (West.includes(State)) return "pink";
  else if (Midwest.includes(State)) return "red";
  else if (Southwest.includes(State)) return "orange";
  else if (Northeast.includes(State)) return "yellow";
  else if (Southeast.includes(State)) return "green";
  else return "black";
}

// Getting our GeoJSON data
d3.json(link).then(function(data) {
  // Creating a GeoJSON layer with the retrieved data
  L.geoJson(data, {
    style: function(feature) {
      return {
        color: "white",
        fillColor: chooseColor(feature.properties.State),
        fillOpacity: 0.5,
        weight: 2.5
      };
    },

    // This is called on each feature.
    onEachFeature: function(feature, layer) {
      // Set the mouse events to change the map styling.
      layer.on({
        // When the cursor is on a map feature, opacity increases to 90%.
        mouseover: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.9
          });
        },
        // When the cursor is off a map feature, opacity reverts back to 50%.
        mouseout: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.5
          });
        },

        // When a feature (state) is clicked, it enlarges.
        click: function(event) {
          myMap.fitBounds(event.target.getBounds());
        }
      });
      
      // var popupStyle = "width: 300px;"; 
      // Giving each feature a popup with information that's relevant to each state
      layer.bindPopup(

        "<h1>" + feature.properties.State + "</h1> <hr> " +
        "<h2> State Code: " + feature.properties.State_code + "</h2> " +
        "<h2> Job Postings: " + feature.properties.job_count + "</h2> " +
        "<h2> Average Annual Salary: $" + feature.properties.avg_ann_sal + "k</h2> " +
        "<h2> Job Types: " + feature.properties.job_types + "</h2>",
        {
          maxWidth: 600,
          minWidth: 100 
        }
      );

    }

  }).addTo(myMap);
});
