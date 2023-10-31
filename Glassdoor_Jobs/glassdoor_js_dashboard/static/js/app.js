
// Get the Samples data
const link = "static/data/job_data.json";

// Fetch the JSON data and console log it
d3.json(link).then(function(data) {
  console.log(data);
});

// Initiallize a dashboard
function init() {

    let dropdownMenu = d3.select("#selDataset");

    // Subject ID for dropdown menu
    d3.json(link).then((data) => {
      dataStates = data;
        
      let codes = data.states
        codes.forEach((id) => {

          dropdownMenu.append("option").text(id).attr("value", id);
          console.log(id);

        });

        // Initialize with the first state_code in 'states'
        let code_0 = codes[0];
        console.log(code_0);
        
        // Initialize state_data, bar-plot, bubble-plot, gauge for subject_0
        stateData(code_0, data);
        barPlot(code_0, data);
        bubblePlot(code_0, data);
        gaugeDial(code_0, data);
                
    });

};

let West = ['WA', 'CA', 'CO', 'OR', 'UT', 'ID']
let Southwest = ['NM', 'TX', 'AZ']
let Midwest = ['IL', 'MI', 'OH', 'MO', 'IN', 'WI', 'NE', 'MN', 'IA', 'KS']
let Southeast = ['FL', 'VA', 'KY', 'AL', 'GA', 'LA', 'NC', 'TN', 'SC']
let Northeast = ['MD', 'NY', 'MA', 'NJ', 'CT', 'DC', 'PA', 'DE', 'RI']


// // -------------------------------------------------
// Function to display state_data of a subject
function stateData(codeId, data) {

      // Retrieve all state_data
      let state_data = data.state_data;

      // Filter using state_code
      let code = state_data.filter(sdata => sdata.State_code == codeId);

      // Log the array of state_data objects
      console.log(code)

      // Get the first index of state_data objects
      let codeData = code[0];

      // Clear out state_data
      d3.select("#state-data").html("");

      const keyMappings = {
        State_code: " ",
        State: " ",
        job_count: "Postings  ",
        avg_ann_sal: "Salary  ",
        job_types: " ",
        Region: "Region  ",
        Region_Salary: "Salary    ",
      };

      Object.entries(codeData).forEach(([key, value]) => {
        
        const textKey = keyMappings[key] || key;
      
        if (key.includes("sal") || key.includes("Sal")) {
          value = `$${value}k`; // Format salary-related keys
        }
      
        console.log(textKey, value);
        d3.select("#state-data").append("h5").html(`${textKey}   <strong>${value}</strong>`)
          .style("margin-bottom", "10px");
      });

};

// -------------------------------------------------
// Function for bar plot
function barPlot(codeId, data) {

      // Retrieve all state_job_types data
      let state_job_types = data.state_job_types;

      // Filter based on the value of the state_id
      let code = state_job_types.filter(job_type => job_type.state_code == codeId);
      console.log(code)

      // Get the first index from the array
      let codeData = code[0];

      // Get the job_titles, job_numbers
      let job_titles = codeData.job_titles;
      let job_numbers = codeData.job_numbers;
      let state_code = codeData.state_code;

      // Log the data to the console
      console.log(job_titles, job_numbers);

      function chooseColor(state_code) {
        if (West.includes(state_code)) return "hotpink";
        else if (Midwest.includes(state_code)) return "red";
        else if (Southwest.includes(state_code)) return "orange";
        else if (Northeast.includes(state_code)) return "deepskyblue";
        else if (Southeast.includes(state_code)) return "limegreen";
        else return "black";
      }

      // Set top 7 job_titles listed in the state in descending order
      let yValues = job_titles.slice(0,10).map(titles => `<b>${titles}  </b>`).reverse();
      let xValues = job_numbers.slice(0,10).reverse();
      

      // Set up the trace for the bar chart
      let traceBar = [{
          x: xValues,
          y: yValues,
          type: "bar",
          orientation: "h",
          marker: {
            color: chooseColor(state_code),
          }
      }];

      // Setup the layout
      let layout = {    
          title: {
            text: "<b>Job Titles Posted in   " + codeData.state_code + "</b>",
            font: {color: "black", size: 17}
          },
          xaxis: {
                  gridcolor: 'rgba(0,0,0,0.1)',
          },
          yaxis: {
            automargin: true,
        },
          width: 550,
          // height: 300, 
          
      };

      // Call Plotly to plot the bar chart
      Plotly.newPlot("bar", traceBar, layout)
  
};

// -------------------------------------------------
// Function for bubble plot
function bubblePlot(codeId, data) {

      // Retrieve all state_sector_types data
      let state_sector_types = data.state_sector_types;
      
      // Filter based on the value of sector_type
      let code = state_sector_types.filter(sector_type => sector_type.state_code == codeId);
      console.log(code)

      // Get the first index from the array
      let codeData = code[0];
      
      // Get the Sectors, Average_Avg_Salary, Number_of_Jobs
      let Sectors = codeData.Sectors;
      let Average_Avg_Salary = codeData.Average_Avg_Salary;
      let Number_of_Jobs = codeData.Number_of_Jobs;
                  
      // Log the data to the console
      console.log(Sectors, Average_Avg_Salary, Number_of_Jobs);

      let customColorScale = [ 
      "#E6E6FA", "#FFA07A", "#FFB366", "#87CEEB", "#F0FFFF", "#98FB98", "#FFF0F5",
      "#B0E0E6", "#F0F8FF", "#FFE4E1", "#FFFFE0", "#F0FFF0", "#FFDAB9","#E0FFFF",
      "#AFEEEE", "#ADFF2F", "#F08080", "#FAFAD2", "#FFFACD", "#FFB6C1", "#FFF0F5"
    ];      
      // Set up the trace for the bar chart
      let traceBubble = [{
          x: Sectors,
          y: Average_Avg_Salary,

          mode: "markers",
          marker: {
            size: Number_of_Jobs.map(size => size * 7), 
            color: customColorScale,
            colorscale: "Accent",
            line: {
              width: 1.25, 
              color: 'black'
            }   
          }
      }];

      // Layout setup
      let layout = {
        title: {
          text: "<b>Sectors and Job Numbers in   " + codeData.state_code + "</b>",
          font: {color: "black", size: 17}
        },
        hovermode: "closest",
        xaxis: {
          title: "Sectors",
          showgrid: true,
          gridcolor: 'rgba(0,0,0,0.1)',
          tickangle: -45,
          // dtick: 0,
        },
        yaxis: {
          title: "Average Salary ('k') (Size: Job-Counts)",
          showgrid: true,
          gridcolor: 'rgba(0,0,0,0.1)',
          tickformat: "$.1s",
        },
        width: 1250, 
        height: 550,
        margin: {t: 50, b:70}

      };

      // Call Plotly to plot the bubble chart
      Plotly.newPlot("bubble", traceBubble, layout)
  
};


// // -------------------------------------------------
// Function for Gauge Chart
function gaugeDial(codeId, data) {

      // Retrieve all state_data
      let state_data = data.state_data;

      // Filter using state_code
      let code = state_data.filter(sdata => sdata.State_code == codeId);

      // Log the array of state_data objects
      console.log(code)

      // Get the first index of state_data objects
      let codeData = code[0];

      let Region_Salary = (codeData.Region_Salary);
      let state_code = (codeData.State_code);
      console.log(Region_Salary);

      function chooseColor(state_code) {
        if (West.includes(state_code)) return "hotpink";
        else if (Midwest.includes(state_code)) return "red";
        else if (Southwest.includes(state_code)) return "orange";
        else if (Northeast.includes(state_code)) return "deepskyblue";
        else if (Southeast.includes(state_code)) return "limegreen";
        else return "black";
      }

      // https://plotly.com/javascript/gauge-charts/
      let traceGauge = [{

        value: Region_Salary,
        domain: {x: [0,1], y: [0,1]},
        title: {  
            text: "<b>REGION:   " + codeData.Region.toUpperCase() + "    SALARY ($k)</b>",
            font: {color: "black", size: 15},
            margin: { t: 0, b: 0 },
        },

        type: "indicator",
        mode: "gauge+number",
        
        gauge: {
            axis: {range: [60,150], tickmode: "linear", tick0: 60, dtick: 10},
            
            bar: {color: chooseColor(state_code)},
            steps: [

              {range: [60, 70], color: "rgba(255, 245, 245, 0.5)"},
              {range: [70, 80], color: "rgba(255, 240, 235, 0.5)"},
              {range: [80, 90], color: "rgba(255, 235, 220, 0.5)"},
              {range: [90, 100], color: "rgba(255, 225, 205, 0.5)"},
              {range: [100, 110], color: "rgba(255, 210, 200, 0.5)"},
              {range: [110, 120], color: "rgba(255, 200, 200 , 0.5)"},
              {range: [120, 130], color: "rgba(255, 190, 180, 0.5)"},
              {range: [130, 140], color: "rgba(255, 170, 170, 0.5)"},
              {range: [140, 150], color: "rgba(255, 150, 160, 0.5)"},
             
            ],
            
        } 
    }];

    // Set Layout
    let layout = {
        width: 550, 
        height: 550,
        margin: {t: 0, b:0}
    };

    // Call Plotly to plot the gauge chart
    Plotly.newPlot("gauge", traceGauge, layout)

};


// // -------------------------------------------------
// Function that updates dashboard when state_code is changed
function chooseOption(codeId) { 

  // Log the new value
  console.log(codeId); 

  // Call all functions 
  barPlot(codeId, dataStates);
  bubblePlot(codeId, dataStates);
  stateData(codeId, dataStates);
  gaugeDial(codeId, dataStates);
        
};

// Call the 'initialize' function
init();

// *****************************************************************
