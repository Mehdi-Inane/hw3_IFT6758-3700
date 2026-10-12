from typing import Tuple
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import scipy.stats as sp
import sys

sns.set()


OUTPUT_TEMPLATE = (
    "Initial (invalid) T-test p-value:\t\t{initial_ttest_p:.3g}\n"
    "Original data normality p-value:\t\t{initial_weekday_normality_p:.3g}, {initial_weekend_normality_p:.3g}\n"
    "Original data equal variance p-value:\t\t{initial_levene_p:.3g}\n"
    "Transformed data normality p-value:\t\t{transformed_weekday_normality_p:.3g}, {transformed_weekend_normality_p:.3g}\n"
    "Transformed data equal variance p-value:\t{transformed_levene_p:.3g}\n"
    "Weekly data normality p-value:\t\t\t{weekly_weekday_normality_p:.3g}, {weekly_weekend_normality_p:.3g}\n"
    "Weekly data equal variance p-value:\t\t{weekly_levene_p:.3g}\n"
    "Weekly T-test p-value:\t\t\t\t{weekly_ttest_p:.3g}\n"
    "Mann-Whitney U-test p-value:\t\t\t{utest_p:.3g}"
)

def read_data(path: str) -> pd.DataFrame:
    # do not modify
    return pd.read_json(path, lines=True) 


def split_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # do not modify
    wd = df.query("is_weekend==False")
    we = df.query("is_weekend==True")
    return wd, we


def draw_histogram(df: pd.DataFrame, title: str = None) -> Figure:
    # do not modify
    fig, ax = plt.subplots(1, 1, dpi=100)
    ret = sns.histplot(data=df, x='comment_count', hue='is_weekend', ax=ax)
    if title:
        ret.set(title=title)
    return fig


# TODO - Complete this method
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process the raw DataFrame:

        1. Keep only the 'canada' subreddit
        2. Keep only the years 2012 and 2013
        3. Add a new column 'is_weekend' with a boolean True/False value
    
    Args:
        df (pd.DataFrame): dataframe to process; contains the columns
            'date', 'subreddit', 'comment_count' by default

    Returns:
        pd.DataFrame: Must have at least the columns: 'comment_count', 'date', 'is_weekend'
    """
    df = df.copy()  # copy so that you do not modify the original dataframe 

    # TODO: Filter on years, subreddit, and add a boolean column 'is_weekend' 
    return df


# TODO - Complete this method
def tests(wd: pd.DataFrame, we: pd.DataFrame, verbose: bool = False) -> Tuple[float, float, float, float]:
    """Performs a T-test between the two inputs, checking whether the means of the two distributions are
    the same. Also checks whether the two input datasets are normally distributed and have the
    same variance (a requirement for the T-test).

    Reference: https://docs.scipy.org/doc/scipy/reference/stats.html#statistical-tests

    Args:
        wd (pd.DataFrame): weekday data
        we (pd.DataFrame): weekend data
        verbose (bool): whether to print the results

    Returns:
        Tuple[float, float, float, float]: p_test, p_wd_isnormal, p_we_isnormal, p_vartest
    """
    p_ttest, p_wd_normal, p_we_normal, p_vartest = None, None, None, None
    
    # TODO: Get the p-value for the t-test

    # TODO: Get the p-value for the normality test on the weekday and weekend data separately
    # I.e. are the 2 distributions normal?

    # TODO: Get the p-value for the test that checks whether these 2 distributions have the same variance
    # ---------- DO NOT MODIFY THE FUNCTION BELOW THIS LINE  ---------- #

    if verbose:
        print(f"p_value:\t{p_ttest.round(5)}")
        print(f"WD normality:\t{p_wd_normal.round(5)}")
        print(f"WE normality:\t{p_we_normal.round(5)}")
        print(f"Variance test:\t{p_vartest.round(5)}")

    return p_ttest, p_wd_normal, p_we_normal, p_vartest


# TODO - Complete this method
def central_limit_theorem(df: pd.DataFrame) -> pd.DataFrame:
    """Combine all the weekdays and weekend days of each year/week pair and take the mean of their
    counts (untransformed).

    Hints: You can get a "year" and a "week number" from the first two values returned
    by date.isocalendar(). This year and week number will give you an identifier for the (year, week) pair.
    Use Pandas to group by this value and aggregate by taking the mean.

    Note: the year returned by isocalendar is not always the same as the year of the date (around New
    Year). Use the isocalendar year, which is correct in this case. This is different from the
    year you used to filter the events; do not perform any additional filtering!

    Args:
        df (pd.DataFrame): cleaned dataframe containing (at minimum) the columns: 'date', 'comment_count', 'is_weekend'

    Returns:
        pd.DataFrame: Must have (at minimum) the columns: 'comment_count', 'is_weekend'
     """
    df = df.copy()

    # TODO: Combine all the weekdays and weekend days of each year/week pair and take the mean of their (untransformed) count.

    clt: pd.DataFrame = None 
    return clt


# TODO - Complete this method
def mann_whitney_u_test(wd: pd.DataFrame, we: pd.DataFrame) -> float:
    """Run the Mann-Whitney U-test between the weekday data and the weekend data.

    The Mann-Whitney U-test is a non-parametric test that can be used to decide whether samples from one group are
    larger/smaller than the observations of another group. It assumes that the two groups have:
        - Independent observations
        - Values that are ordinal (can be sorted)

    Recall that the alternative hypothesis for a two-sided test states:
        Suppose F(u) and G(u) are the cumulative distribution functions of the distributions
        that gave x and y, respectively. Then the alternative hypothesis is that the distributions
        are not equal, i.e. F(u) ≠ G(u) for at least one u.

    Args:
        wd (pd.DataFrame): weekday data
        we (pd.DataFrame): weekend data

    Returns:
        float: p-value of the Mann-Whitney U-test
     """
    # TODO

    p_utest: float = None
    return p_utest


def main():
    """ 
    Note: nothing in main() will be graded; the code here is only to help guide the development of your code
    """
    path = "./data/reddit-counts.json.gz"
    if len(sys.argv) > 1:
        path = sys.argv[1]

    # load data
    raw_df = read_data(path)

    # preliminary processing
    df = process_data(raw_df)
    wd, we = split_data(df)
    p_ttest, p_wd_normal, p_we_normal, p_vartest = tests(wd, we)

    # fix 1: best transformed tests
    trans = df.copy()

    trans['comment_count'] = trans.comment_count  # TODO: apply some transformation to the data

    T_wd, T_we = split_data(trans)
    p_T_ttest, p_T_wd_normal, p_T_we_normal, p_T_vartest = tests(T_wd, T_we)

    # fix 2: central limit theorem tests
    clt = central_limit_theorem(df)
    clt_wd, clt_we = split_data(clt)
    p_clt_ttest, p_clt_wd_normal, p_clt_we_normal, p_clt_vartest = tests(clt_wd, clt_we)

    # fix 3: u tests on original data
    p_utest = mann_whitney_u_test(wd, we)


    print(OUTPUT_TEMPLATE.format(
        initial_ttest_p = p_ttest,

        initial_weekday_normality_p = p_wd_normal,
        initial_weekend_normality_p = p_we_normal,
        initial_levene_p = p_vartest,

        transformed_weekday_normality_p = p_T_wd_normal,
        transformed_weekend_normality_p = p_T_we_normal,
        transformed_levene_p = p_T_vartest,

        weekly_weekday_normality_p=p_clt_wd_normal,
        weekly_weekend_normality_p=p_clt_we_normal,
        weekly_levene_p=p_clt_vartest,
        weekly_ttest_p=p_clt_ttest,

        utest_p = p_utest,
    ))

if __name__ == '__main__':
    main()
