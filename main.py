import logging
import os
import sys

from vntr_finder import VNTRFinder
from reference_vntr import identify_homologous_vntrs, load_unique_vntrs_data
# from vntr_graph import plot_graph_components, get_nodes_and_edges_of_vntr_graph


if len(sys.argv) < 2:
    sys.exit("ERROR: You should specify alignment_file")

pacbio_reads = False
if len(sys.argv) >= 3:
    pacbio_reads = sys.argv[2] == 'pacbio'
input_file = sys.argv[1]
input_is_alignment_file = input_file.endswith('bam') or input_file.endswith('sam')
directory = os.path.dirname(input_file) + '/'

LOGFILE = 'log_%s.log' % os.path.basename(input_file)
logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename=LOGFILE, level=logging.DEBUG, filemode='w')

reference_vntrs = load_unique_vntrs_data()

# reference_vntrs = identify_homologous_vntrs(reference_vntrs, 'chr15')
accurate_vntr_list = [7, 69, 119, 970, 1123, 1213, 1214, 1215, 1216, 1217, 1218, 1219, 1220, 809, 377, 378]
accurate_vntr_list = [7, 119, 1214, 1218, 1220, 1221, 377, 378, 809]

for i in range(len(reference_vntrs)):
    if not reference_vntrs[i].is_non_overlapping() or reference_vntrs[i].has_homologous_vntr():
        continue
    if reference_vntrs[i].id not in accurate_vntr_list:
        continue
    print(i, len(reference_vntrs[i].get_repeat_segments()))
    vntr_finder = VNTRFinder(reference_vntrs[i])
    if pacbio_reads:
        if input_is_alignment_file:
            copy_number = vntr_finder.find_repeat_count_from_pacbio_alignment_file(input_file, directory)
        else:
            copy_number = vntr_finder.find_repeat_count_from_pacbio_reads(input_file, directory)
    else:
        if input_is_alignment_file:
            copy_number = vntr_finder.find_repeat_count_from_alignment_file(input_file, directory)
        else:
            copy_number = vntr_finder.find_repeat_count_from_short_reads(input_file)
    # vntr_finder.find_accuracy()

# print(len(reference_vntrs))
# nodes, edges = get_nodes_and_edges_of_vntr_graph(reference_vntrs)
# plot_graph_components(nodes, edges)
