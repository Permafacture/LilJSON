'''

The previous version of this file was not an implementation of Visvalingam's algorithim. It did not recalculate coordinate areas after removing coordinates, and of course also didn't worry about removing coordinates in the correct order.  So, if several adjacent points were all below the threshold, the flawed implementation removed all of them without regard for the consequences.

The correct algorithim (as described at http://web.archive.org/web/20100428020453/http://www2.dcs.hull.ac.uk/CISRG/publications/DPs/DP10/DP10.html) is as follows.



==================

The algorithm is as follows:

 

Compute the effective area of each point (see Section 3.2)

Delete all points with zero area and store them in a separate list with this area

REPEAT

- Find the point with the least effective area and call it the current point. If its calculated area is less than that of the last point to be eliminated, use the latter's area instead. (This ensures that the current point cannot be eliminated without eliminating previously eliminated points.)

- Delete the current point from the original list and add this to the new list together with its associated area so that the line may be filtered at run time.

       - Recompute the effective area of the two adjoining points (see Figure 1b).

 UNTIL

       - The original line consists of only 2 points, namely the start and end points.'''
