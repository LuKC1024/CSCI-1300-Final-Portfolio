from scipy import stats
from scipy.stats import t as t_dist
from scipy.stats import chi2

from abtesting_test import *

# You can comment out these lines! They are just here to help follow along to the tutorial.
print(t_dist.cdf(-2, 20)) # should print .02963
print(t_dist.cdf(2, 20)) # positive t-score (bad), should print .97036 (= 1 - .2963)

print(chi2.cdf(23.6, 12)) # prints 0.976
print(1 - chi2.cdf(23.6, 12)) # prints 1 - 0.976 = 0.023 (yay!)

# TODO: Fill in the following functions! Be sure to delete "pass" when you want to use/run a function!
# NOTE: You should not be using any outside libraries or functions other than the simple operators (+, **, etc)
# and the specifically mentioned functions (i.e. round, cdf functions...)

def slice_2D(list_2D, start_row, end_row, start_col, end_col):
    '''
    Splices a the 2D list via start_row:end_row and start_col:end_col
    :param list: list of list of numbers
    :param nums: start_row, end_row, start_col, end_col
    :return: the spliced 2D list (ending indices are exclsive)
    '''
    to_append = []
    for l in range(start_row, end_row):
        to_append.append(list_2D[l][start_col:end_col])

    return to_append

def sum(nums):
    s = 0
    for n in nums:
        s += n
    return s

def sqrt(n):
    return n ** (1/2)

def get_avg(nums):
    '''
    Helper function for calculating the average of a sample.
    :param nums: list of numbers
    :return: average of list
    '''
    #TODO: fill me in!
    return (sum(nums) / len(nums))

def get_stdev(nums):
    '''
    Helper function for calculating the standard deviation of a sample.
    :param nums: list of numbers
    :return: standard deviation of list
    '''
    #TODO: fill me in!
    to_sum = []
    avg = get_avg(nums)
    n = len(nums)
    for i in nums:
        to_sum.append((i - avg) ** 2)
    return sqrt(sum(to_sum) / (n - 1))

def get_standard_error(a, b):
    '''
    Helper function for calculating the standard error, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: standard error of a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    n_a = len(a)
    n_b = len(b)
    std_a = get_stdev(a)
    std_b = get_stdev(b)
    return sqrt(((std_a ** 2) / n_a) + ((std_b ** 2) / n_b))

def get_2_sample_df(a, b):
    '''
    Calculates the combined degrees of freedom between two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: integer representing the degrees of freedom between a and b (see studio 6 guide for this equation!)
    HINT: you can use Math.round() to help you round!
    '''
    #TODO: fill me in!
    se = get_standard_error(a, b)
    n_a = len(a)
    n_b = len(b)
    std_a = get_stdev(a)
    std_b = get_stdev(b)
    se4 = se ** 4
    std_a2 = std_a ** 2
    std_b2 = std_b ** 2
    return round(se4 / (((std_a2 / n_a) **2 / (n_a - 1)) + ((std_b2 / n_b) **2 / (n_b - 1))))

def get_t_score(a, b):
    '''
    Calculates the t-score, given two samples.
    :param a: list of numbers
    :param b: list of numbers
    :return: number representing the t-score given lists a and b (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    return (get_avg(a) - get_avg(b)) / get_standard_error(a, b)

def perform_2_sample_t_test(a, b):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates a p-value by performing a 2-sample t-test, given two lists of numbers.
    :param a: list of numbers
    :param b: list of numbers
    :return: calculated p-value
    HINT: the t_dist.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    t_score = get_t_score(a, b)
    df = get_2_sample_df(a, b)
    return t_dist.cdf(min(- t_score, t_score), df)


# [OPTIONAL] Some helper functions that might be helpful in get_expected_grid().
# def row_sum(observed_grid, ele_row):
# def col_sum(observed_grid, ele_col):
# def total_sum(observed_grid):
# def calculate_expected(row_sum, col_sum, tot_sum):

def get_expected_grid(observed_grid):
    '''
    Calculates the expected counts, given the observed counts.
    ** DO NOT modify the parameter, observed_grid. **
    :param observed_grid: 2D list of observed counts
    :return: 2D list of expected counts
    HINT: To clean up this calculation, consider filling in the optional helper functions below!
    '''
    #TODO: fill me in!
    # handy constants
    n_rows = len(observed_grid)
    n_cols = len(observed_grid[0])
    # comp row sums and col sums
    row_sums = []
    col_sums = []
    total = 0
    for i in range(n_rows):
        row_sums.append(0)
    for j in range(n_cols):
        col_sums.append(0)
    for i in range(n_rows):
        for j in range(n_cols):
            row_sums[i] += observed_grid[i][j]
            col_sums[j] += observed_grid[i][j]
            total += observed_grid[i][j]
    assert total == sum(row_sums)
    assert total == sum(col_sums)
    assert len(row_sums) == n_rows
    assert len(col_sums) == n_cols
    # comp expected grid
    expected_grid = []
    for i in range(n_rows):
        row = []
        for j in range(n_cols):
            row.append(None)
        expected_grid.append(row)
    for i in range(n_rows):
        for j in range(n_cols):
            expected_grid[i][j] = row_sums[i] * col_sums[j] / total
    return expected_grid
    
    

def df_chi2(observed_grid):
    '''
    Calculates the degrees of freedom of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: degrees of freedom of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    n_rows = len(observed_grid)
    n_cols = len(observed_grid[0])
    return (n_rows - 1) * (n_cols - 1)

def chi2_value(observed_grid):
    '''
    Calculates the chi^2 value of the expected counts.
    :param observed_grid: 2D list of observed counts
    :return: associated chi^2 value of expected counts (see studio 6 guide for this equation!)
    '''
    #TODO: fill me in!
    n_rows = len(observed_grid)
    n_cols = len(observed_grid[0])
    expected_grid = get_expected_grid(observed_grid)
    s = 0
    for i in range(n_rows):
        for j in range(n_cols):
            observed = observed_grid[i][j]
            expected = expected_grid[i][j]
            s += (observed - expected) ** 2 / expected
    return s


def perform_chi2_homogeneity_test(observed_grid):
    '''
    ** DO NOT CHANGE THE NAME OF THIS FUNCTION!! ** (this will mess with our autograder)
    Calculates the p-value by performing a chi^2 test, given a list of observed counts
    :param observed_grid: 2D list of observed counts
    :return: calculated p-value
    HINT: the chi2.cdf() function might come in handy!
    '''
    #TODO: fill me in!
    return 1 - chi2.cdf(chi2_value(observed_grid), df_chi2(observed_grid))

# These commented out lines are for testing your main functions. 
# Please uncomment them when finished with your implementation and confirm you get the same values :)
def data_to_num_list(s):
  '''
    Takes a copy and pasted row/col from a spreadsheet and produces a usable list of nums. 
    This will be useful when you need to run your tests on your cleaned log data!
    :param str: string holding data
    :return: the spliced list of numbers
    '''
  return list(map(float, s.split()))

a1 = """
3584
4419
4716
12616
16237
31792
4481
6939
18629
"""
b1 = """
3647
10622
70381
132565
1077460
2646
6018
8161
8894
16928
19631
"""
a_t1_list = data_to_num_list(a1) 
b_t1_list = data_to_num_list(b1)
print(get_t_score(a_t1_list, b_t1_list))
print(perform_2_sample_t_test(a_t1_list, b_t1_list))

a_count_1 = "6 3"
b_count_1 = "5 6"
a_c1_list = data_to_num_list(a_count_1) 
b_c1_list = data_to_num_list(b_count_1)
c1_observed_grid = [a_c1_list, b_c1_list]
print(chi2_value(c1_observed_grid))
print(perform_chi2_homogeneity_test(c1_observed_grid))
