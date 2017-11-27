with open("grupos_Matheus.pickle", "rb") as handle:
    clusters = pickle.load(handle)

with open("grupos_Thiago.pickle", "rb") as handle:
    grupos = pickle.load(handle)

rev_grupos = {}
for key, value in grupos.items():
    for string in {value}:
        rev_grupos.setdefault(string, []).append(key)

meu_cluster_values = rev_grupos.values()
matheus_cluster_values = list(clusters.values())
for v in matheus_cluster_values:
    v = list(v)
for i in range(len(matheus_cluster_values)):
    matheus_cluster_values[i] = list(matheus_cluster_values[i])

conta_erros1 = 0
meu_dict_erros = {}

for i in range(1,len(rev_grupos) + 1):
    try:
        if all(list(rg) not in matheus_cluster_values for rg in list(itertools.permutations(rev_grupos[i]))):
     #   if rev_grupos[i] not in matheus_cluster_values:
            meu_dict_erros[conta_erros1] = rev_grupos[i]
            conta_erros1 = conta_erros1 + 1
    except KeyError:
        print()

dict_matheus_erros = {}
conta_erros2 = 0
for i in range(len(matheus_cluster_values)):
    try:
        if all(list(mv) not in meu_cluster_values for mv in list(itertools.permutations(matheus_cluster_values[i]))):
        #if matheus_cluster_values[i] not in meu_cluster_values:
            dict_matheus_erros[conta_erros2] = matheus_cluster_values[i]
            conta_erros2 = conta_erros2 + 1
    except KeyError:
        print()

erros_matheus_values = list(dict_matheus_erros.values())

dict_match_erros = {}
k = 0
for meu in list(meu_dict_erros.values()):
    for meu_i in meu:
        for mat in erros_matheus_values:
            for mat_i in mat:
                if meu_i == mat_i:
                    dict_match_erros[k] = []
                    dict_match_erros[k].append(meu)
                    dict_match_erros[k].append(mat)
                    k = k + 1

dict_match_erros
