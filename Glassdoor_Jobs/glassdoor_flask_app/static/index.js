

let button = d3.select("#click-me");

const pageURLs = [
  
  "http://127.0.0.1:5000/api/v1.0/Average_Salary_and_Number_of_Jobs_by_Sectors",
  "http://127.0.0.1:5000/api/v1.0/Number_of_Jobs_Postings_in_Each_sector",
  "http://127.0.0.1:5000/api/v1.0/Salaries_by_Job_Title",
  "http://127.0.0.1:5000/api/v1.0/Number_of_Each_Job_Type_in_Each_Sector",
  "http://127.0.0.1:5000/api/v1.0/Salary_Distribution_by_Region",
  "http://127.0.0.1:5000/api/v1.0/Company_Age_and_Salary_vs_User_Rating",
  "http://127.0.0.1:5000/api/v1.0/Salary_Distribution_by_Programming_Language_and_Application",
  "http://127.0.0.1:5000/api/v1.0/Salary_By_Language",
  
];


let index = 0;

button.on("click", function() {

  if (index < pageURLs.length) {
    console.log(`Index: ${index}, URL: ${pageURLs[index]}`)
    
    d3.select("#graph-me")
      .html(`<img src='${pageURLs[index]}' alt='glassdoor job graph' style='display: block; margin: 0 auto; max-width: 100%; max-height: 100%;'>`);
    
    index++; 
  };

  if (index == pageURLs.length) {
    index = 0;
  }
   
});

