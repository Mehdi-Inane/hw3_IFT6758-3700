"""
All the sections that require work are marked with "TODO".
"""
import numpy as np
import pandas as pd
from pathlib import Path
import shutil
from tqdm.autonotebook import tqdm
from typing import Tuple
import xml.etree.ElementTree as ET


# TODO - complete this method
def parse_xml(path: str) -> pd.DataFrame:
    """
    Parse the XML file obtained from the FIDE player database, which can be found here:

        http://ratings.fide.com/download.phtml?period=2022-10-01

    Note that ratings are updated quite regularly, so we use the fixed snapshot of
    06 Oct 2022, which is provided to you in the data directory. You should not need to download anything.

    Args:
        path (str): path to the desired .xml file; if it does not exist, automatically looks for the corresponding .zip file to extract

    Returns:
        pd.DataFrame: DataFrame containing the raw data from the xml file, with the columns:
            ["name", "rating", "sex", "birthday", "country", "flag", "title"]
    """
    path = Path(path)

    # unzip xml data if unavailable
    if not path.is_file():
        if path.with_suffix(".zip").is_file():
            shutil.unpack_archive(path.with_suffix(".zip"), path.parent)
        else:
            raise FileNotFoundError("%s nor an archive exists." % path)

    # define function to extract value, define tags to extract 
    _get_val = lambda entry, tag: entry.find(tag).text
    TARGET_ATTRIBUTES = ["name", "rating", "sex", "birthday", "country", "flag", "title"]

    # ----------  DO NOT MODIFY THE FUNCTION ABOVE THIS LINE ---------- #

    # TODO: 
    # XML element tree (use xml.etree.ElementTree)

    # TODO: iterate over the root node, to get the desired values for the desired tags
    # Make sure to load all the values in TARGET_ATTRIBUTES (use the same column name in the dataframe as the tag name!). You can use the provided _get_val(person, tag) method defined at the top to get the corresponding tag.
   
    # TODO: Convert to a dataframe

    return None


# TODO - complete this method
def clean_data(df: pd.DataFrame, year_cutoff: int) -> pd.DataFrame:
    """

    Args:
        df (pd.DataFrame): the raw dataframe returned by the parse_xml() method
        year_cutoff (int): remove the players whose birth years are GREATER THAN (>) this value; i.e. only
            include players born up to (and including) this year

    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    # TODO: Remove the rows with no birthday information

    # TODO: Convert the numeric types to integers
    
    # TODO: Keep only the players with a birth year up to year_cutoff (inclusive)

    return None


# TODO - complete this method
def bin_counts(df: pd.DataFrame, bins: list, bin_centers: list) -> pd.DataFrame:
    """ Returns a dataframe with the `ratings` grouped between the values given in `bins`, and
    labeled with the value given in `bin_centers`. In addition to the raw count, also add a normalized
    count column named "count_norm" by dividing the counts by the sum of the counts.

    Ex: Given
        >> x = pd.DataFrame({'rating' : [1, 2, 4, 6, 6, 7, 8, 11]})
        >> bins = [0, 5, 10, 15]
        >> bin_centers = [2.5, 7.5, 12.5]
    
    bin_counts(x, bins, bin_centers) must return:
        >>      rating  count  count_norm
        >>  0    7.5      4       0.500
        >>  1    2.5      3       0.375
        >>  2   12.5      1       0.125

    Args:
        df (pd.DataFrame): Cleaned dataframe with at least the column 'rating'
        bins (list): defines the bin edges; i.e. [0, 5, 10] defines two bins: [0, 5) and [5, 10]
        bin_centers (list): defines the labels that will be used; i.e. [2.5, 7.5] for the above
        will map the values as [0, 5) -> 2.5, and [5, 10) -> 7.5.

    Returns:
        pd.DataFrame: dataframe with the binned values; must have the columns
            ['rating', 'count', 'count_norm']. Rename them if necessary.
    """
    if 'rating' not in df.keys():
        raise ValueError("Incorrect input format; 'rating' must be a column in the input dataframe")

    # TODO: Hint - use pd.cut, and make sure to use reset_index() when useful
    hist = None

    # TODO: Rename the columns, making sure they still make sense (we want 'rating', 'count')

    # TODO: Add the 'count_norm' column

    return hist


class PermutationTest:
    def __init__(self, df: pd.DataFrame, n_overrep: int, n_underrep: int):
        """ Implements the permutation test experiment.

         Args:
             df (pd.DataFrame): full dataframe to partition (i.e. includes both groups)
             n_overrep (int): number of elements in the overrepresented group
             n_underrep (int): number of elements in the underrepresented group
        
         n_overrep + n_underrep should be == len(df)! Technically < len(df) is fine too...
         """
        if len(df) < n_overrep + n_underrep:
            raise ValueError(f"Sum of n_overrep + n_underrep must be <= len(df)")
        self.df = df
        self.n_overrep = n_overrep
        self.n_underrep = n_underrep
    
    # TODO - complete this method
    def job(self, seed: int = None) -> Tuple[int, int]:
        """ Samples two groups of size n_overrep, n_underrep and returns the maximum rating for each of the
        groups in that order (overrep, underrep)

        Args:
            seed (int, optional): sets the random state, if specified.

        Returns:
            Tuple[int, int]: the maximum ratings for each of the two groups, in the order (max(overrepresented), max(underrepresented))
         """
        if seed is not None:
            np.random.seed(seed)
            

        # TODO: sample two groups of size n_overrep, n_underrep and return the maximum rating for each
        # of the groups in the order (overrep, underrep)
        
        # Hint: consider using np.random.permutation on an appropriate choice of array
        return 


# TODO - complete this method
def sample_two_groups(
    df: pd.DataFrame, n_overrep: int, n_underrep: int, n_iter: int=1000
) -> Tuple[np.array, np.array]:
    """Run n_iter permutation tests on df, split into two groups (sampled WITHOUT replacement) of
    size n_overrep and n_underrep. Return two numpy arrays of length n_iter, where the elements correspond to the
    maximum rating in the overrepresented and underrepresented groups respectively.

    Args:
        df (pd.DataFrame): cleaned dataframe to process
        n_overrep (int): number of samples for the overrepresented group
        n_underrep (int): number of samples for the underrepresented group
        n_iter (int, optional): the total number of iterations to run

    Returns:
        Tuple[np.array, np.array]: Two arrays containing the maximums for the overrepresented group and the underrepresented group for each of the n_iter experiments.
    """
    best_over = []
    best_under = []

    # TODO: run n_iter runs of this experiment and return a numpy array containing the maximum values of the overrepresented and underrepresented groups respectively.

    # Hint: wrap your iterator with tqdm to get a progress bar, for example:
    # >>> for i in tqdm(range(10)):
    # >>>     print(i)

    return np.array(best_over), np.array(best_under)


