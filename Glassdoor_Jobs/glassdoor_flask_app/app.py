# Import the dependencies.
from flask import Flask, send_file
import io
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)


# connection = sqlite3.connect('..//Resources//glassdoor_jobs.sqlite')
connection = sqlite3.connect('C:\A_Sheena\Cyber\Module_16Pj3\Project_3\Resources\glassdoor_jobs.sqlite')
query = "SELECT * FROM glassdoor_clean"
glassdoor = pd.read_sql_query(query, connection)


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
            f"<br/>"
            f"Glassdoor Job Postings Data API: (2017 - 2018) in the USA <br/>"
            f"<br/>"
            f"Job-Statistics: <br/>"
            f"<br/>"
            f"/api/v1.0/Average_Salary_and_Number_of_Jobs_by_Sectors<br/>"
            f"/api/v1.0/Number_of_Jobs_Postings_in_Each_sector<br/>"
            f"/api/v1.0/Salaries_by_Job_Title<br/>"
            f"/api/v1.0/Number_of_Each_Job_Type_in_Each_Sector<br/>"
            f"/api/v1.0/Salary_Distribution_by_Programming_Language_and_Application<br/>"
            f"/api/v1.0/Salary_By_Language<br/>"
            f"/api/v1.0/Salary_Distribution_by_Region<br/>"
            f"/api/v1.0/Company_Age_and_Salary_vs_User_Rating"
            )


@app.route("/api/v1.0/Average_Salary_and_Number_of_Jobs_by_Sectors")
def salary_sector_bubble():

    # Create the engine here
    engine = create_engine('sqlite:///Resources/glassdoor_jobs.sqlite')

    # Create our session (link) from Python to the DB
    session = Session(engine)

    avg_sal = round(glassdoor.groupby('Sector')['Avg_Salary'].mean(), 1)   # Create dictionary (below) for y-axis values
    val_count = glassdoor['Sector'].value_counts()  # Create dictionary (below) using value_counts()
    cat_names = glassdoor['Sector'].unique()

    Sector_count = {cat: val_count[cat] for cat in cat_names}  # Dictionary
    
    Sector_count_vals = [Sector_count[cat] for cat in Sector_count.keys()]
    
    scaled_Sector_count_vals = np.multiply(Sector_count_vals, 100)  # Scaled up by 100

    Sector_Sal = {cat: (avg_sal[cat]) for cat in cat_names}
    print(f'Sector name and average salary from data:\n{Sector_Sal} \n')

    colors = np.random.rand(len(cat_names))

    plt.clf()
    plt.figure(figsize=(20,10))

    plt.scatter(Sector_Sal.keys(), Sector_Sal.values(), s = scaled_Sector_count_vals, c = colors, cmap = 'Accent', edgecolors = 'k', alpha = 0.55)

    plt.grid(True, alpha = 0.25)
    plt.xlabel("Sector Names")
    plt.ylabel("Average Annual Salary")
    plt.ylim(ymin = 20, ymax = 150)

    plt.title("Average Annual Salary and Size of Sectors versus Sectors", fontsize = 16)
    plt.xticks(rotation=90)

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0.1)
    img_stream.seek(0)
    
    session.close()

    return send_file(img_stream, mimetype='image/png')
    


       
@app.route("/api/v1.0/Number_of_Jobs_Postings_in_Each_sector")
def numbers_sector_bar():

    # Create the engine here
    engine = create_engine('sqlite:///Resources/glassdoor_jobs.sqlite')

    # Create our session (link) from Python to the DB
    session = Session(engine)

    val_count = glassdoor['Sector'].value_counts()  # Create dictionary (below) for y-axis values
    cat_names = glassdoor['Sector'].unique()   # Create dictionary (below) for x-axis values

    Sector_count = {cat: val_count[cat] for cat in cat_names}
    
    sorted_Sector_count = {r: Sector_count[r] for r in sorted(Sector_count, key=Sector_count.get, reverse=True)}
    print(sorted_Sector_count, '\n')

    plt.clf()
    plt.figure(figsize=(20,12))

    sorted_Sector_count_asc = dict(sorted(sorted_Sector_count.items(), key=lambda item: item[1]))
    plt.barh(list(sorted_Sector_count_asc.keys()), list(sorted_Sector_count_asc.values()), color = 'greenyellow', edgecolor = 'limegreen')

    # Color the top 4 bars in blue
    for i, bar in enumerate(plt.gca().patches):
        if i > 4 and bar.get_width() > 60:
            # bar.set_color('green')
            bar.set_facecolor('skyblue')
            bar.set_edgecolor('b')

    plt.xlabel("Number of Jobs", fontsize = 14)
    plt.ylabel("Sector Names", fontsize = 12)
    plt.title("Job Opportunities", fontsize = 16)
    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)
    plt.grid(True, alpha = 0.25)

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0.1)
    img_stream.seek(0)
    
    session.close()

    return send_file(img_stream, mimetype='image/png')



@app.route("/api/v1.0/Salaries_by_Job_Title")
def salary_title_violin():

    # Create the engine here
    engine = create_engine('sqlite:///Resources/glassdoor_jobs.sqlite')

    # Create our session (link) from Python to the DB
    session = Session(engine)

    plt.clf()
    plt.figure(figsize=(20,5))

    sns.violinplot(x = "Job_Title", y = "Avg_Salary", data = glassdoor)

    plt.title("Average Annual Salary by Job Title", fontsize=14, pad=20)
    plt.xlabel("Job Title", fontsize=14, labelpad=10)
    plt.ylabel("Average Salary", fontsize=16, labelpad=10)
    plt.grid(True, alpha = 0.25)
    
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0.1)
    img_stream.seek(0)
    
    session.close()

    return send_file(img_stream, mimetype='image/png')



@app.route("/api/v1.0/Salary_Distribution_by_Programming_Language_and_Application")
def salary_language_hist():
    
    # Create the engine here
    engine = create_engine('sqlite:///Resources/glassdoor_jobs.sqlite')

    # Create our session (link) from Python to the DB
    session = Session(engine)

    lng = ['Python_y_n', 'R_y_n', 'Spark_y_n', 'AWS_y_n', 'Excel_y_n']  # Column names of Languages
    ln_c = ['blue', 'orangered', 'deeppink', 'green', 'red']  #  Line and fill color
    eg_c = ['skyblue', 'peachpuff', 'violet', 'lightgreen', 'tomato']  #  Edge color
    header = ['Python', 'R', 'Spark', 'AWS', 'Excel']  #  Language names in Titles

    def language(lang, lin_c, edg_c, title, ax):
        gldr_lang = glassdoor[glassdoor[lang].isin([1])]
        gldr_lang_sal = int(gldr_lang.Avg_Salary.median())
        print(f'Median Salary with knowledge of {title}: ${gldr_lang_sal}k')
        sns.histplot(x = 'Avg_Salary', data = gldr_lang, kde=True, lw=0.75, color=lin_c, edgecolor=edg_c, ax = ax)
        ax.grid(True, alpha = 0.2)
        ax.set_title(title)

    plt.clf()
    
    fig, axs = plt.subplots(nrows = 2, ncols = 3, figsize = (15, 10))
    fig.suptitle('\nAnnual Salary Distribution for jobs requiring Programming Language/Application', fontsize = 16)
    fig.subplots_adjust(hspace = 0.4, wspace = 0.3)

    i = j = counter = 0
    for l in range(len(lng)):
        language(lng[l], ln_c[l], eg_c[l], header[l], axs[i][j])
        j += 1
        counter += 1
        if counter > 4:
            plt.delaxes(axs[i][j])
            break

        if j > 2:
            i += 1; j = 0

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0.1)
    img_stream.seek(0)
    
    session.close()

    return send_file(img_stream, mimetype='image/png')




@app.route("/api/v1.0/Salary_Distribution_by_Region")
def salary_region_pie():

    # Create the engine here
    engine = create_engine('sqlite:///Resources/glassdoor_jobs.sqlite')

    # Create our session (link) from Python to the DB
    session = Session(engine)

    Region_Salary = glassdoor.groupby('job_region')['Avg_Salary'].mean().round(0)
    
    job_regions = ['Midwest', 'Northeast', 'Southeast', 'Southwest', 'West']

    plt.clf()
    plt.figure(figsize=(12,12))

    plt.pie(Region_Salary.tolist(),
            labels = job_regions,
            colors = ['r', 'limegreen', 'dodgerblue', 'deeppink', 'yellow'],
            startangle = 90, shadow = True, explode = (0, 0, 0, 0, 0.1), autopct = '%1.1f%%')

    legend_labels = [f'{region}: ${salary:.0f}' for region, salary in zip(job_regions, Region_Salary)]
    plt.legend(
        labels=legend_labels,
        edgecolor = 'white',
        loc = (1.0, 0.9),
        title='Average Salary',
        fontsize= 14
    )
    plt.title("Salary Distribution by Region", fontsize = 16)
    
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0.1)
    img_stream.seek(0)
    
    session.close()

    return send_file(img_stream, mimetype='image/png')



@app.route("/api/v1.0/Company_Age_and_Salary_vs_User_Rating")
def age_salary_rating_scatter():

    # Create the engine here
    engine = create_engine('sqlite:///Resources/glassdoor_jobs.sqlite')

    # Create our session (link) from Python to the DB
    session = Session(engine)

    mask = glassdoor['Usr_Rating'] > 0

    plt.clf()
    if mask.any():
        
        plt.figure(figsize=(20,10))

        dot_size = np.multiply(glassdoor[mask]['Avg_Salary'], 0.75)
        colors = np.random.rand(len(glassdoor[mask]['Sector']))
        
        plt.scatter(
        glassdoor[mask]['Usr_Rating'],
        glassdoor[mask]['Company_Age'],
        s=dot_size,
        c=colors,
        cmap='PuRd',    
        edgecolor='navy',
        linewidths=0.75,
        alpha=0.9
        )
        plt.title(f'Company Age vs Glassdoor User Rating\n\n', fontsize=14, pad=20)
        plt.suptitle('Dot size Represents Average Salary', fontsize=12, y=0.92)
        plt.xlabel("User Rating", fontsize=12)
        plt.ylabel("Company Age", fontsize=14, labelpad=10)
        
        filtered_rating = glassdoor[mask]
        mean = round(filtered_rating['Usr_Rating'].mean(), 1)
        median = round(filtered_rating['Usr_Rating'].median(), 1)
        mode = round(filtered_rating['Usr_Rating'].mode(), 1)
        std = round(filtered_rating['Usr_Rating'].std(), 1)

        stat_param = {'mean': mean, 'median': median, 'mode': mode[0]}
        
        for i in range(-4, 2):
            if (i + 1) == 0:
                continue
            else:
                new_val = (mean + (i + 1) * std).round(1)
                new_key = f'{i + 1} std'
                stat_param[new_key] = new_val
        
        ln_clr = ['black', 'forestgreen', 'purple', 'orangered', 'orangered', 
                  'orangered', 'orangered', 'orangered', 'orangered']

        for i, (k, v) in enumerate(stat_param.items()):
            plt.axvline(v, color=ln_clr[i], linestyle='dashed', lw=0.75)
            plt.text(v, -45, k, color='k', ha='center', va='top', rotation=90, fontsize=9, weight='bold')

    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0.1)
    img_stream.seek(0)
    
    session.close()

    return send_file(img_stream, mimetype='image/png')



@app.route("/api/v1.0/Number_of_Each_Job_Type_in_Each_Sector")
def number_jobtype_sector_bar():

    # Create the engine here
    engine = create_engine('sqlite:///Resources/glassdoor_jobs.sqlite')

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # count job titles within each sector
    sector_job_counts = glassdoor.groupby(['Sector', 'Job_Title']).size().unstack(fill_value=0)

    # Sort the data by total job counts within each sector in descending order
    sorted_sectors = sector_job_counts.sum(axis=1).sort_values(ascending=False).index

    plt.clf()
    plt.figure(figsize=(20,10))

    # Create the countplot with the sorted sectors
    sns.countplot(x='Job_Title', data=glassdoor, hue='Sector', edgecolor='k',
              palette=sns.color_palette(('violet', 'chartreuse', 'maroon', 'm', 
                                         'sandybrown', 'red', 'sienna', 'yellow',
                                         'gray', 'gold', 'palegreen', 'olivedrab',
                                         'mediumspringgreen', 'deepskyblue', 'blue',
                                         'g', 'darkorchid', 'plum', 'y', 'mistyrose',
                                         'mediumslateblue', 'pink', 'yellow'),
                            n_colors=len(sorted_sectors)),
              hue_order=sorted_sectors)

    plt.legend(loc=(0.8, 0.3))
    plt.xlabel("Job Title")
    plt.ylabel("Number of Job Postings")
    plt.title("Number of Each Job-Type in Each Sector", fontsize = 16)
    plt.grid(True, alpha=0.2)
        
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0.1)
    img_stream.seek(0)
    
    session.close()

    return send_file(img_stream, mimetype='image/png')




@app.route("/api/v1.0/Salary_By_Language")
def salary_language_bar():

    # Create the engine here
    engine = create_engine('sqlite:///Resources/glassdoor_jobs.sqlite')

    # Create our session (link) from Python to the DB
    session = Session(engine)

    plt.clf()
    plt.figure(figsize=(10,10))

    lang_list = ['Python_y_n', 'R_y_n', 'Spark_y_n', 'AWS_y_n', 'Excel_y_n']
    lang_names = ['Python', 'R', 'Spark', 'AWS', 'Excel']

    lang_Sal = {}
    for i in range(len(lang_list)):    
        lang_Y = round(glassdoor.loc[glassdoor[lang_list[i]] == 1].groupby(glassdoor[lang_list[i]])['Avg_Salary'].mean(), 1)
        lang_Y = lang_Y.values[0]   # Extract the 1st value of array
        lang = lang_names[i] 

        lang_Sal[lang] = lang_Y  # Adding element to dictionary

    # print(lang_Sal)
    sorted_lang_Sal = {r: lang_Sal[r] for r in sorted(lang_Sal, key = lang_Sal.get, reverse=True)}
    
    plt.bar(sorted_lang_Sal.keys(), sorted_lang_Sal.values(), color = 'c')

    plt.xlabel("Language")
    plt.ylabel("Average Annual Salary")
    plt.ylim(ymin = 60, ymax = 120)
    plt.title("Average Annual Salary by Lanuage", fontsize=16)
    plt.grid(True, alpha=0.25)
        
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png', bbox_inches='tight', pad_inches=0.1)
    img_stream.seek(0)
    
    session.close()

    return send_file(img_stream, mimetype='image/png')




if __name__ == '__main__':
    app.run(debug=True)



