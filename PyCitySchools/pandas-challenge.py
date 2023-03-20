#!/usr/bin/env python
# coding: utf-8

# # PyCity Schools Analysis
#  - Charter schools had a higher overall passing percentage then district scores (approx. 90% vs. 54%). This carries over into both reading and math passing percentages as well. 
#  - All schools, including district and charter, had consistently higher reading scores than math scores, on average. This was regardless of size of overall budget or spending per student. 
#  - Overall, medium-sized schools (1000-2000 students) performed better in both subjects regardless of school type (charter or district). This was true for average scores as well as passing percentages of both subjects.

# In[36]:


# Dependencies and Setup
import pandas as pd

# File to Load (Remember to Change These)
school_data_to_load = "/Users/helenamabey/Git files/pandas-challenge/PyCitySchools/Resources/schools_complete.csv"
student_data_to_load = "/Users/helenamabey/Git files/pandas-challenge/PyCitySchools/Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas DataFrames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine the data into a single dataset.  
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# ## District Summary

# In[37]:


# Calculate the total number of unique schools
school_count = (school_data_complete['school_name'].nunique())
school_count


# In[38]:


# Calculate the total number of students
student_count = (school_data_complete['Student ID'].nunique())
student_count


# In[39]:


# Calculate the total budget
total_budget = school_data_complete.drop_duplicates(subset=['school_name'])['budget'].sum()
total_budget


# In[40]:


# Calculate the average (mean) math score
average_math_score = school_data_complete['math_score'].mean()
average_math_score


# In[41]:


# Calculate the average (mean) reading score
average_reading_score = school_data_complete['reading_score'].mean()
average_reading_score


# In[42]:


# Use the following to calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# In[43]:


# Calculate the percentage of students who passed reading (hint: look at how the math percentage was calculated)  
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage


# In[44]:


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate


# In[45]:


# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary = pd.DataFrame([[school_count,student_count,total_budget,average_math_score,
                                  average_reading_score,passing_math_percentage,passing_reading_percentage,
                                  overall_passing_rate]], columns=["Total Schools", 
                                                                   "Total Students","Total Budget",
                                                                   "Average Math Score","Average Reading Score",
                                                                   "% Passing Math","% Passing Reading",
                                                                   "% Overall Passing"])

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

# Display the DataFrame
district_summary


# ## School Summary

# In[46]:


# Use the code provided to select the school type
school_types = school_data.set_index(["school_name"])["type"]


# In[47]:


# Calculate the total student count
per_school_counts = school_data_complete.groupby(["school_name"])['student_name'].count()
per_school_counts


# In[48]:


# Calculate the total school budget and per capita spending
per_school_budget = (school_data_complete.groupby(["school_name"]).mean()["budget"]).astype('float64')
per_school_capita = (per_school_budget / per_school_counts).astype('float64')


# In[49]:


# Calculate the average test scores
per_school_math = school_data_complete.groupby(["school_name"])['math_score'].mean()
per_school_reading = school_data_complete.groupby(["school_name"])['reading_score'].mean()
per_school_math


# In[50]:


# Calculate the number of schools with math scores of 70 or higher
school_passing_math = school_data_complete[(school_data_complete["math_score"] >= 70)] 
school_passing_math_schools = (school_passing_math.groupby(["school_name"]).count()["student_name"] / per_school_counts)*100
school_passing_math_schools_count = school_passing_math_schools[(school_passing_math_schools >= 0.7)].count()
school_passing_math_schools_count


# In[51]:


# Calculate the number of schools with reading scores of 70 or higher
school_passing_reading = school_data_complete[(school_data_complete["reading_score"] >= 70)] 
school_passing_reading_schools = (school_passing_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts)*100
school_passing_reading_schools_count = school_passing_reading_schools[(school_passing_reading_schools >= 0.7)].count()
school_passing_reading_schools_count


# In[52]:


# Use the provided code to calculate the schools that passed both math and reading with scores of 70 or higher
passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)
]
passing_math_and_reading.head()


# In[53]:


# Use the provided code to calculate the passing rates
per_school_passing_math = school_passing_math.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100
per_school_passing_reading = school_passing_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100
overall_passing_rate = passing_math_and_reading.groupby(["school_name"]).count()["student_name"] / per_school_counts * 100


# In[54]:


# Create a DataFrame called `per_school_summary` with columns for the calculations above.

per_school_summary = pd.DataFrame({"School Type":school_types,
                                   "Total Students":per_school_counts,
                                   "Total School Budget":per_school_budget,
                                   "Per Student Budget":per_school_capita,
                                   "Average Math Score":per_school_math,
                                   "Average Reading Score":per_school_reading,
                                   "% Passing Math":school_passing_math_schools,
                                   "% Passing Reading":school_passing_reading_schools,
                                   "% Overall Passing":overall_passing_rate})

per_school_summary = per_school_summary.sort_index()
per_school_summary.index.name = None
# Formatting
per_school_summary["Total School Budget"] = per_school_summary["Total School Budget"].map("${:,.2f}".format)
per_school_summary["Per Student Budget"] = per_school_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
per_school_summary


# ## Highest-Performing Schools (by % Overall Passing)

# In[55]:


# Sort the schools by `% Overall Passing` in descending order and display the top 5 rows.
per_school_summary = per_school_summary.sort_values(["% Overall Passing"], ascending=False)
per_school_summary.head()


# ## Bottom Performing Schools (By % Overall Passing)

# In[56]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
per_school_summary = per_school_summary.sort_values(["% Overall Passing"])
per_school_summary.head()


# ## Math Scores by Grade

# In[57]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by "school_name" and take the mean of each.
ninth_graders_scores = ninth_graders.groupby(["school_name"]).mean()
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()

# Use the code to select only the `math_score`.
ninth_grade_math_scores = ninth_graders_scores["math_score"]
tenth_grader_math_scores = tenth_graders_scores["math_score"]
eleventh_grader_math_scores = eleventh_graders_scores["math_score"]
twelfth_grader_math_scores = twelfth_graders_scores["math_score"]


# Combine each of the scores above into single DataFrame called `math_scores_by_grade`
math_scores_by_grade = pd.DataFrame()

#math_scores_by_grade = math_scores_by_grade.rename(columns={})
math_scores_by_grade["9th"] =ninth_grade_math_scores
math_scores_by_grade["10th"] =tenth_grader_math_scores
math_scores_by_grade["11th"] =eleventh_grader_math_scores
math_scores_by_grade["12th"] =twelfth_grader_math_scores

# Minor data wrangling
math_scores_by_grade.index.name = None

# Display the DataFrame
math_scores_by_grade


# ## Reading Score by Grade

# In[58]:


# Use the code provided to separate the data by grade
ninth_graders = school_data_complete[(school_data_complete["grade"] == "9th")]
tenth_graders = school_data_complete[(school_data_complete["grade"] == "10th")]
eleventh_graders = school_data_complete[(school_data_complete["grade"] == "11th")]
twelfth_graders = school_data_complete[(school_data_complete["grade"] == "12th")]

# Group by "school_name" and take the mean of each.
ninth_graders_scores = ninth_graders.groupby(["school_name"]).mean()
tenth_graders_scores = tenth_graders.groupby(["school_name"]).mean()
eleventh_graders_scores = eleventh_graders.groupby(["school_name"]).mean()
twelfth_graders_scores = twelfth_graders.groupby(["school_name"]).mean()

# Use the code to select only the `reading_score`.
ninth_grade_reading_scores = ninth_graders_scores["reading_score"]
tenth_grader_reading_scores = tenth_graders_scores["reading_score"]
eleventh_grader_reading_scores = eleventh_graders_scores.mean()["reading_score"]
twelfth_grader_reading_scores = twelfth_graders_scores["reading_score"]

# Combine each of the scores above into single DataFrame called `reading_scores_by_grade`
reading_scores_by_grade = pd.DataFrame()

reading_scores_by_grade["9th"] =ninth_grade_reading_scores
reading_scores_by_grade["10th"] =tenth_grader_reading_scores
reading_scores_by_grade["11th"] =eleventh_grader_reading_scores
reading_scores_by_grade["12th"] =twelfth_grader_reading_scores

# Minor data wrangling
reading_scores_by_grade = reading_scores_by_grade[["9th", "10th", "11th", "12th"]]
reading_scores_by_grade.index.name = None

# Display the DataFrame
reading_scores_by_grade


# ## Scores by School Spending

# In[59]:


# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[60]:


# Create a copy of the school summary since it has the "Per Student Budget" 
school_spending_df = per_school_summary.copy()
school_spending_df["Per Student Budget"] = (per_school_budget / per_school_counts).astype('float64')


# In[61]:


# Use `pd.cut` to categorize spending based on the bins.
school_spending_df["Spending Ranges (Per Student)"] = pd.cut(school_spending_df["Per Student Budget"], 
                                                             spending_bins, labels=labels, include_lowest=True)

school_spending_df["Per Student Budget"] = school_spending_df["Per Student Budget"].map("${:,.2f}".format)
school_spending_df = school_spending_df.sort_index()
school_spending_df


# In[62]:


#  Calculate averages for the desired columns. 
spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]
spending_reading_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Reading Score"]
spending_passing_math = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Math"]
spending_passing_reading = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Passing Reading"]
overall_passing_spending = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["% Overall Passing"]


# In[63]:


# Assemble into DataFrame
#Average Math Score, Average Reading Score, % Passing Math, % Passing Reading, % Overall Passing
#Spending Ranges (Per Student)

spending_summary = pd.DataFrame({"Average Math Score": spending_math_scores, "Average Reading Scores": spending_reading_scores,
        "% Passing Math": spending_passing_math, "% Passing Reading": spending_passing_reading,
        "% Overall Passing": overall_passing_spending})

# Display results
spending_summary


# ## Scores by School Size

# In[64]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[65]:


# Categorize the spending based on the bins
# Use `pd.cut` on the "Total Students" column of the `per_school_summary` DataFrame.

per_school_summary["School Size"] = pd.cut(per_school_summary["Total Students"], 
                                                             size_bins, labels=labels, include_lowest=True)


per_school_summary = per_school_summary.sort_index()
per_school_summary


# In[66]:


# Calculate averages for the desired columns. 
size_math_scores = per_school_summary.groupby(["School Size"]).mean()["Average Math Score"]
size_reading_scores = per_school_summary.groupby(["School Size"]).mean()["Average Reading Score"]
size_passing_math = per_school_summary.groupby(["School Size"]).mean()["% Passing Math"]
size_passing_reading = per_school_summary.groupby(["School Size"]).mean()["% Passing Reading"]
size_overall_passing = per_school_summary.groupby(["School Size"]).mean()["% Overall Passing"]


# In[67]:


# Create a DataFrame called `size_summary` that breaks down school performance based on school size (small, medium, or large).
# Use the scores above to create a new DataFrame called `size_summary`

size_summary = pd.DataFrame({"Average Math Score": size_math_scores, "Average Reading Scores": size_reading_scores,
        "% Passing Math": size_passing_math, "% Passing Reading": size_passing_reading,
        "% Overall Passing": size_overall_passing})
# Display results
size_summary


# ## Scores by School Type

# In[68]:


# Group the per_school_summary DataFrame by "School Type" and average the results.
type_math_scores = per_school_summary.groupby(["School Type"])[["Average Math Score"]].mean()
type_reading_scores = per_school_summary.groupby(["School Type"])[["Average Reading Score"]].mean()
type_passing_math = per_school_summary.groupby(["School Type"])[["% Passing Math"]].mean()
type_passing_reading = per_school_summary.groupby(["School Type"])[["% Passing Reading"]].mean()
type_overall_passing = per_school_summary.groupby(["School Type"])[["% Overall Passing"]].mean()

# Use the code provided to select new column data
average_math_score_by_type = type_math_scores["Average Math Score"]
average_reading_score_by_type = type_reading_scores["Average Reading Score"]
average_percent_passing_math_by_type = type_passing_math["% Passing Math"]
average_percent_passing_reading_by_type = type_passing_reading["% Passing Reading"]
average_percent_overall_passing_by_type = type_overall_passing["% Overall Passing"]


# In[69]:


# Assemble the new data by type into a DataFrame called `type_summary`

type_summary = pd.DataFrame({"Average Math Score": average_math_score_by_type,
                            "Average Reading Score":average_reading_score_by_type,
                            "% Passing Math":average_percent_passing_math_by_type,
                            "% Passing Reading":average_percent_passing_reading_by_type,
                            "% Overall Passing":average_percent_overall_passing_by_type})
# Display results
type_summary


# In[ ]:




