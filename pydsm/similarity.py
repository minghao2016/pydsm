# -*- coding: utf-8 -*-
from pydsm.indexmatrix import IndexMatrix
import pydsm.model


def _assure_consistency(matrix, vector):
    if not vector.is_vector():
        raise ValueError("Vector should have the shape (1,n).")

    vector = vector.synchronize_word_order(matrix, axis=1)
    if matrix.col2word != vector.col2word:
        raise ValueError("Columns of each matrix must match")
    return vector

def dot(matrix, vector, assure_consistency=True):
    """
    Calculate dot product distance for all words in matrix against vector.
    """
    if assure_consistency:
        vector = _assure_consistency(matrix, vector)
    return matrix.dot(vector.transpose())


def euclidean(matrix, vector, assure_consistency=True):
    """
    Calculate inversed euclidean distance for all words in matrix against vector.
    """
    if assure_consistency:
        vector = _assure_consistency(matrix, vector)
    inv_euc= 1/(1+matrix.subtract(vector).norm(axis=1))
    return inv_euc.sort(ascending=False)


def cos(matrix, vector, assure_consistency=True):
    """
    Calculate cosine distance for all words in matrix against all words in vector.
    Params:
        matrix: A matrix to check all values against
        vector: A vector to compare against the matrix.
        assure_consistency: If set, it makes sure the matrix and vector share  the same column indices. 
                            This makes it more secure, but a bit slower.
    """

    if assure_consistency:
        vector = _assure_consistency(matrix, vector)

    if matrix.is_vector():
        return _word_cos(matrix, vector)

    dotted = matrix.dot(vector.transpose())
    mat1_norms = matrix.multiply(matrix).sum(axis=1).sqrt()
    mat2_norms = vector.multiply(vector).sum(axis=1).sqrt()
    mat1_mat2_norms = mat1_norms.multiply(mat2_norms)
    neighbors = dotted.multiply(1 / mat1_mat2_norms)

    return neighbors

def _word_cos(v1, v2, assure_consistency=True):
    """
    Faster calculation for vector pair similarity.
    """
    return v1.dot(v2.transpose()) / (v1.norm() * v2.norm())


__dsm__ = ['nearest_neighbors']
