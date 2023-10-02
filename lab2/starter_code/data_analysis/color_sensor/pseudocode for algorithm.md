ClassifyColoredCube(R,G,B): 
    Initialize a data structure called colorTable to store the mean R, G and B values for each of the 6 colors (mR, mG, mB)
    Initialize a string variable called currentColor to an empty string
    Initialize a variable called shortestDistance to 999999
    For i from 0 to 5:
        Index into the colorTable to access mR, mG, mB for the ith color in the datatable 
        Compute the Euclidean distance of R,G,B from mR, mG, mB
        If this distance is lower than shortestDistance:
            Update shortest distance to this value
            Update the current color to the ith color in the data structure
        Else continue
    Return the color 


