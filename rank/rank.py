from scipy import stats
from numpy import median
import warnings

# Rank two samples of data.
# Returns 0 if the samples are not significantly different.
# Returns -1 if the lhs sample values are significantly smaller than the rhs sample values.
# Returns 1 if the lhs sample values are significantly greater than the rhs sample values.
def rank(lhs, rhs, alpha=0.05):
    if len(lhs) == 0 or len(rhs) == 0:
        raise(Exception('Empty list(s) passed to rank.'))
    
    # Kruskal and MWU raise errors if called on lists containing only identical values (eg [0, 0, 0], which is common when testing neutrality.)
    # If that is the case, we can still handle it for our purposes.
    if lhs.count(lhs[0]) == len(lhs) or rhs.count(rhs[0]) == len(rhs):
        # Either or both lists contain only identical elements.
        


    if len(lhs) < 20 or len(rhs) < 20:
        warnings.warn("One or both samples provided to the rank function has less than 20 elements. This is ill-advised when performing a Wilcoxon signed rank test.")
    
    # Using the Kruskal-Wallis H test, determine whether the samples are statistically significantly different:
    _, pval = stats.kruskal(lhs, rhs)
    if pval < alpha:
        # The difference between the medians of the samples is significantly different.
        # Perform a post-hoc test to determine which sample stochastically dominates the other (which is larger).
        # This is done using the Mann-Whitney U test:
        _, pval = stats.mannwhitneyu(lhs, rhs, alternative='two-sided')
        if pval < alpha:
            # The difference between the medians of the samples is (still) significantly different.
            # Determine the significantly greater sample as the sample with the greater median (which is consistent with MWU):
            if median(lhs) < median(rhs):
                return -1
            else:
                return 1
                
        else:
            # The samples do not differ significantly (according to the Mann-Whitney U test).
            return 0    
        
    else:
        # The samples do not differ significantly (according to the Kruskal-Wallis H test).
        return 0
