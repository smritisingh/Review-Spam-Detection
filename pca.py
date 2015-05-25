#-------------------------------------------------------------------------------
# Name:        pca.py
# Purpose:	   to reduce dimensionality of the features vector
#
# Author:      Smriti
#
# Created:     11/05/2015
# Copyright:   (c) Smriti 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def PCA_dimension_reducer( featurevectormatrix, requiredDimensions = 0):
'''
%PCA_dimension_reducer implements PCA algorithm 
%   The algorithm determines the highest valued eigenvectors of the feature
%   matrix and reduces teh dimension space based on that. The k parameter
%   is the desired output dimension. Evidently the featrue space should
%   have greater than or equal to k dimensions.
'''
    nrows = len(featurevectormatrix)
    ncolumns = len(featurevectormatrix[0])
    if ncolumns < requiredDimensions:
        print("Error in dimensions")        
        return None
    else:
        Average = mean(featurevectormatrix);
        %subtract the avergae vector
        for i = 1:nrows
            featurevectormatrix(i,:)= double(featurevectormatrix(i)) - Average;
        end
        %find the covariance matrix
        CovarianceMatrix = cov(featurevectormatrix);
        [EigenVectors,EigenValues ]= eig(CovarianceMatrix);    
        
        if ~issorted(diag(EigenValues))
            [EigenVectors,EigenValues] = eig(A);
            [EigenValues,I] = sort(diag(EigenValues));
            EigenVectors = EigenVectors(:, I);
        end
        EigenSpace = EigenVectors(:,ncolumns-requiredDimensions+1:ncolumns);
        Finalmatrix = featurevectormatrix*EigenSpace;
    end
end

