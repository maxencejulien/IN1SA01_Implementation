from fonction import *

def test_obtenir_direction():

	assert obtenir_direction((0, 0), (10, 10), 10) == (10, 10)
	assert obtenir_direction((100, 100), (0, 0), 10) == (-10, -10)
	assert obtenir_direction((0, 0), (0, 0), 5) == (0, 0)

test_obtenir_direction()


def test_case_autour():

	assert caseAutour((0, 0), 10) == [(0, 0), (0, 10), (10, 0), (10, 10)]
	assert caseAutour((10, 10), 10, True) == [(0, 0), (0, 10), (0, 20), (10, 0), (10, 20), (20, 0), (20, 10), (20, 20)]
	assert caseAutour((0, 0), 10, False, 2) == [(0, 0), (0, 10), (0, 20), (10, 0), (10, 10), (10, 20), (20, 0), (20, 10), (20, 20)]

test_case_autour()