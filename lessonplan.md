# Lesson plan
  
  ** this file should contain teacher lesson plan details ** 

  __ students will never see this __

  ## Learning Objectives
  1. Show off Data Science and the power of Python
  2. Learn about the Pandas library.
  3. Guided coding for querying data.

## Question 2 Answer
```python
for index, row in df.iterrows():
    if row["Area"] == "Area 2":
        print(row["Date"], row["Time"], row["Stage"],
             row["Area"], row["Duration"])
```
  