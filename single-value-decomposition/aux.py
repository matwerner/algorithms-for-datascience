import numpy as np 

def get_usa_capitals():
	L = np.array([
		[	  0,	 400,  851, 1551, 1769, 1605, 2596, 1137, 1255, 1123],
		[ 400,		 0,  454, 1198, 1370, 1286, 2198,  803, 1181,  731],
		[ 851,	 454, 	 0,  803,  920,  940, 1745,  482, 1188,  355],
		[1551,	1198,  803,    0,  663,  225, 1240,  420, 1111,  862],
		[1769,	1370,  920,  663,    0,  879,  831,  879, 1726,  700],
		[1605,	1286,  940,  225,  879,    0, 1374,  484,  968, 1056],
		[2596,	2198, 1745, 1240,  831, 1374,    0, 1603, 2339, 1524],
		[1137,	 803,  482,  420,  879,  484, 1603,    0,  872,  669],
		[1255,	1181, 1188, 1111, 1726,  968, 2339,  872,   0,  1511],
		[1123,	 731,  355,  862,  700, 1056, 1524,  699, 1511,    0],
		[ 188,	 292,  713, 1374, 1631, 1420, 2451,  957, 1092, 1018],
		[1282,	 883,  432,  586,  488,  794, 1315,  529, 1397,  290],
		[ 271,	 279,  666, 1299, 1579, 1341, 2394,  881, 1019,  985],
		[2300,	1906, 1453,  887,  586, 1017,  357, 1263, 1982, 1280],
		[ 483,	 178,  410, 1070, 1320, 1137, 2136,  660, 1010,  743],
		[1038,	 662,  262,  547,  796,  679, 1589,  240, 1061,  466],
		[2099,	1699, 1260,  999,  371, 1200,  579, 1250, 2089,  987],
		[2699,	2300, 1858, 1483,  949, 1645,  347, 1802, 2594, 1584],
		[2493,	2117, 1737, 1681, 1021, 1891,  959, 1867, 2734, 1395],
		[ 393,	 292,  597, 1185, 1494, 1220, 2300,  765,  923,  934],
	])
	R = np.array([
		[	188, 	1282,  271, 2300,  483, 1038, 2099, 2699, 2493,  393],
		[	292, 	 883,  279, 1906,  178,  662, 1699, 2300, 2117,  292],
		[	713, 	 432,  666, 1453,  410,  262, 1260, 1858, 1737,  597],
		[1374, 	 586, 1299,  887, 1070,  547,  999, 1483, 1681, 1185],
		[1631, 	 488, 1579,  586, 1320,  796,  371,  949, 1021, 1494],
		[1420, 	 794, 1341, 1017, 1137,  679, 1200, 1645, 1891, 1220],
		[2451, 	1315, 2394,  357, 2136, 1589,  579,  347,  959, 2300],
		[ 957, 	 529,  881, 1263,  660,  240, 1250, 1802, 1867,  765],

	])		