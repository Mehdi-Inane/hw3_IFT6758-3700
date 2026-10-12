<!--- 
# Université de Montréal
# IFT-6758-B  -  A22  -  Data Science 
-->

# Homework 3

Point distribution:

| Section                           | Required files        | Score |
|-----------------------------------|-----------------------|:--:|
| Reddit Weekends                   | `reddit_weekends.py`  | 35 |
| &emsp;+ plots, short answers      | `reddit_weekends.ipynb` | 10 |
| Chess Ratings                     | `chess_ratings.py`    | 35 |
| &emsp;+ plots, short answers      | `chess_ratings.ipynb` | 20 |

In general your homework will be auto-graded, which means that you must **not modify the signature of the defined functions** (same inputs and outputs). 
For questions involving Numpy and Pandas, you **must** handle all iteration through calls to the relevant library functions.
This means that you cannot use native Python for loops, list comprehensions, etc. when something could have been done with a native pandas/numpy call.
Loops are otherwise allowed.


### Submission

To submit your files, please submit **only the required files** (listed in the table above) that you have completed on **gradescope**. 
Do not include data or other miscellaneous files.
You do not need to submit all the files at the same time to run the autograder.
For example, if you have only completed `reddit_weekends.py`, you do not need to submit the rest of the files to get feedback on `reddit_weekends.py`.

## 1. Reddit Weekends

This question uses data derived from the Reddit Comment archive, which is a collection of every Reddit comment, distributed as 150 GB of compressed JSON.

The provided file `reddit-counts.json.gz` contains a count of the number of comments posted daily in each Canadian province subreddit and in r/canada itself.
Again, the format is compressed line-by-line JSON. It turns out that Pandas (≥0.21) can handle the compression automatically and we do not need to explicitly decompress:

```bash
counts = pd.read_json(path, lines=True)
```

We are asking the following question: is there a different number of Reddit comments posted on weekdays than on weekend days?

For this question, we will only look at the values in 2012 and 2013 and in the r/canada subreddit. Start by creating a DataFrame with the provided data and separating the weekdays from the weekends.

Hint: use `datetime.date.weekday`. A value of 5 is Saturday and 6 is Sunday.

Complete the program `reddit_weekends.py` for this question and follow along in the notebook `reddit_weekends.ipynb`.
You will be graded on your work in the python file, as well as on the plots and short answers in the notebook.
The python file also has a section of code to run. You can run it from the command line with the following command:

```bash
python3 reddit_weekends.py ./data/reddit-counts.json.gz
```

Note that the output produced by the command above will not be graded. We will test your functions directly through unit tests.

### 1.1 Student's T-test

- Complete `reddit_weekends.py:process_data()`
- Complete `reddit_weekends.py:tests()`

Use scipy.stats to perform a T-test on the data to get a p-value.
Can you conclude that there is a different number of comments on weekdays compared to weekends?
Try `stats.normaltest` to see whether the data is normally distributed, and `stats.levene` to see whether the two datasets have equal variances.
Do you now think you can draw a conclusion? (Hint: no, we get "0.0438".)


### 1.2 Solution 1: transforming the data

- Complete the plots in `reddit_weekends.ipynb`

Take a look at the histogram of the data. You will notice that it is skewed: this is why it was not normally distributed in the previous part.
Transform the counts so that the data does not fail the normality test. Likely options for transformations: np.log, np.exp, np.sqrt, counts**2. Choose the one that comes closest to a normal distribution.
(Hint: None of them will pass the normality test.)


### 1.3 Solution 2: the central limit theorem

- Complete `reddit_weekends.py:central_limit_theorem()`
- Complete the plots in `reddit_weekends.ipynb`

The central limit theorem says that if our numbers are large enough and we look at sample means, then the result should be normal. 
We will combine all the weekdays and weekend days of each year/week pair and take the mean of their (untransformed) counts.

Hint: you can get a "year" and a "week number" from the first two values returned by date.isocalendar().
This year and week number will give you an identifier for the week. Use Pandas to group by this value and aggregate by taking the mean.
However, the year returned by isocalendar is not always the same as the year of the date.
Use the isocalendar year, which is correct in this case.

Check these values to see whether they have a Gaussian distribution and equal variance. Apply a T-test if it makes sense.

We should note that we are subtly changing the question here. It is now something like "does the number of comments on weekends and on weekdays differ for each week?"

### 1.4 Solution 3: non-parametric test

- Complete `reddit_weekends.py:mann_whitney_u_test()`

Another option is a statistical test that does not care as much about the shape of its input. The Mann-Whitney U-test does not assume normally distributed values nor that the variances of the two distributions are equal.

Perform a U-test on the (original, untransformed, unaggregated) counts. Note that we should do a two-sided test. Make sure the function arguments are correct.

Note that we are subtly changing the question again. If we reach a conclusion because of a U-test, it is something like "it is not equally likely that there are more comments on weekends than on weekdays".

### 1.5 Questions

Answer these questions in the section specified in `reddit_weekends.ipynb`:

- Which of the four suggested transformations gets you closest to satisfying the assumptions of a T-test?
- We gave imprecise explanations in words of what the weekly test and the Mann-Whitney test were actually testing. Do the same for the original T-test and for the T-test on the transformed data. That is, describe what the conclusion would be if you could reject the null hypothesis of these tests.
- Of the four approaches, which one do you think does the best job of getting an answer to the original question: "Is there a different number of Reddit comments posted on weekdays and on weekends?" Briefly explain why. (It is not clear that there is a single correct answer to this question, but there are wrong ones!)
- When are there more Reddit comments posted in r/canada on average, on weekdays or on weekends?


## 2. Chess Ratings

When comparing the performance of two groups, a common mistake is to compare them based on the best of each group, especially in scenarios where one of the groups has a significantly larger number of samples than the other (overrepresented).
One such example is in chess, where people have incorrectly tried to claim that women players are worse than men players because, looking at the best players, no woman has been world champion, or because the difference in Elo (a method for calculating the relative skill levels of players) between the best woman and the best man is large.

Why is this a mistake? Because it neglects the participation rate of these groups.
Naively, if two groups are drawn from the same distribution, the overrepresented group will be more likely to land in the tails of the distribution.
For example, say there are two groups of people: A and B.
Group A has 10 people, group B has 2.
Each of the 12 people is randomly assigned a number between 1 and 100 (with replacement).
Then, take the maximum of group A as group A's score and the maximum of group B as group B's score.
On average, group A will get a score of about 91 and group B about 67, where the only difference between the two groups is their size.
The larger group is more likely to have a high score, so it will get a higher score on average.
The fair way to compare these unequally sized groups is to compare their means (averages), not their maximum values.
Of course, in this example, it would be 50 for both groups – no difference!
Note that this only highlights the statistical effect of simply comparing overrepresented and underrepresented groups and ignores any potential issues or other biases in the data.

In this section, we will explore this in the context of the chess ratings mentioned previously.
No code to help you is provided in the python file; instead, you can follow along in the notebook `chess_ratings.ipynb`.

### 2.1 Load and clean the data

- Complete `chess_ratings.py:parse_xml()`
- Complete `chess_ratings.py:clean_data()`

A (zipped) XML file is provided to you:

    ./data/standard_oct22frl_xml.zip

It was obtained from the FIDE player database, which can be found [here](http://ratings.fide.com/download.phtml?period=2022-10-01).
Note that ratings are updated quite regularly, so we use the fixed snapshot of October 6, 2022, which is provided to you in the data directory.
You should not need to download anything.

Complete the `parse_xml()` method. Note that the first part of the method contains code to automatically extract the zip file for you.
Make sure to get the following data from the XML (and to use them as column names) in your dataframe:

    ["name", "rating", "sex", "birthday", "country", "flag", "title"]

Then, complete `clean_data()`: remove the players with NaN birthdays, convert the numeric types to the appropriate type and filter the birth years `<=2002` (because Elo ratings for people < 20 years old may not be reliable).

### 2.2 Compare the rating distributions

- Complete `chess_ratings.py:bin_counts()`
- Complete the plots in `chess_ratings.ipynb`

Now let's compare the distribution of ratings of male and female players.
Since the data is quite fine-grained, we will need to bin the ratings.
Complete `bin_counts()`, which should handle the binning for arbitrary data and choice of bins.
In addition to returning the raw counts, also return the normalized counts (`count_norm`).

Then, you will use this method to complete the plots in `chess_ratings.ipynb`.
For the plots, choose a bin *width* of 50, a range from 1000 to 2900 (make sure your range extends up to 2900!), and the bin *center* as the midpoint of each bin (i.e. for a bin between [1500, 1550], the center would be 1525).
Note that when defining your bins, you will find that `len(bin_centers) = len(bins) - 1`.

Using the binned data, draw two line plots side by side. One plot should contain the raw counts (`count`) and the other the normalized counts (`count_norm`). M/F should be two different colors.
Make sure to include these plots in your notebook when you submit.

### 2.3 Permutation tests

- Complete `chess_ratings.py:PermutationTests.job()`
- Complete `chess_ratings.py:sample_two_groups()`

Finally, we will perform the permutation tests described in the introduction.
Take the full cleaned dataset (men and women) and randomly sample two groups without replacement.
The size of the groups should reflect the real-world difference that we wish to study, i.e. the size of the male and female groups.
Finish `PermutationTests.job()`, which implements the sampling part of this experiment, and returns the maximum value of the overrepresented and underrepresented groups respectively.

Then, complete the `sample_two_groups()` method, which runs this experiment `n_iter` times.
Once finished, run this experiment in the notebook with at least `n_iter=1000`.
Run the cell that prints the mean difference obtained from the permutation tests, as well as the real differences.
Make sure to include these printed results in your notebook when you submit.

### 2.4 Questions

Answer these questions (1 to 3 sentences each) in the section specified in `chess_ratings.ipynb`:

1. Interpret the results - can you draw a conclusion? Remember that the claim discussed in the introduction to this question was "men are better than women at chess because most of the best players are men". (*Note: part of your answer here will probably be related to your answer to the next question.*)
2. Do you think the numbers obtained here tell the whole story? What could be the problems with the analysis conducted here? Is the data we are working with biased in any way (other than an overrepresentation bias)? Is Elo a good measure, and can it be used to answer the original question? Are there differences in the social, cultural and systemic treatment of men and women that may prevent the underrepresented group from achieving similar results?

The goal of these questions is to emphasize that data is a limited representation of the real world.
It is essential for us, as data scientists, to take a step back when looking at a result and to think about how it relates to the real world, rather than naively assuming that the data and the experimental setup are good, which often leads to erroneous or incorrect conclusions.
There could be several causal factors that explain a relationship that are independent of the original hypothesis: use of data that does not truly reflect the hypothesis you wish to test, biased data (including overrepresented groups), real systemic differences between the groups, etc.


# References

- **Reddit Weekends** is based on Greg Baker's data science course at SFU.
- **Chess Ratings** is based on the analysis in this [blog post.](https://en.chessbase.com/post/what-gender-gap-in-chess)
