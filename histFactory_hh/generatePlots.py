import ROOT as R
import copy, sys, os, inspect 

scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.append(scriptDir)
from basePlotter import *
from HHAnalysis import HH

def getBinningStrWithMax(nBins, start, end, max):
    """Return string defining a binning in histFactory, with 'nBins' bins between
    'start' and 'end', but with the upper edge replaced by 'max'."""
    
    bins = [start]
    pos = start
    for i in range(nBins):
        pos += (end-start)/nBins
        bins.append(pos)
    if bins[-1] < max:
        bins[-1] = max

    m_string = str(len(bins)-1) + ", { "
    for b in bins[0:len(bins)-1]:
        m_string += str(b) + ", "
    m_string += str(bins[-1]) + "}"

    return m_string


include_directories = []
plots = []
library_directories = []
libraries = []

code_before_loop = default_code_before_loop()
code_in_loop = default_code_in_loop()
code_after_loop = default_code_after_loop()
headers = default_headers()

include_directories.append(os.path.join(scriptDir, "..", "common"))

###### Reweighting -- template-based #########
#sample_weights = {}

#headers.append("reweight_v1tov3.h")

## For v1->v3 reweighting
#code_before_loop += """
#getBenchmarkReweighter("/home/fynu/sbrochet/scratch/Framework/CMSSW_7_6_5/src/cp3_llbb/HHTools/scripts/", 0, 11, true, "cluster_NUM_v1_to_v3_weights.root", "NUM");
#"""
#for node in range(1, 13):
#    sample_weights[ "cluster_node_" + str(node) ] = "getBenchmarkReweighter().getWeight({}-1, hh_gen_mHH, hh_gen_costhetastar)".format(node)

## For v1->1507 reweighting
#code_before_loop += """
#getBenchmarkReweighter("/home/fynu/swertz/scratch/CMSSW_7_6_3_patch2/src/cp3_llbb/HHTools/scripts/weights_v1_1507_points.root", 0, 1506, false, "point_NUM_weights_unfolded", "NUM");
#"""
#for node in range(0, 1507):
#    if node in [324, 910, 985, 990]: continue # Skip dummy Xanda
#    sample_weights[ "point_" + str(node) ] = "getBenchmarkReweighter().getWeight({}, hh_gen_mHH, hh_gen_costhetastar)".format(node)

## For v1->v1 checks:
#code_before_loop += """
#getBenchmarkReweighter("/home/fynu/swertz/scratch/CMSSW_7_6_3_patch2/src/cp3_llbb/HHTools/scripts/", 2, 13, true, "cluster_NUM_v1_to_v3_weights.root", "NUM");
#"""
#for node in range(2, 14):
#    sample_weights[ "cluster_node_rwgt_" + str(node) ] = "getBenchmarkReweighter().getWeight({}, hh_gen_mHH, hh_gen_costhetastar)".format(node)

####### Reweighting - ME-based #########
#sample_weights = {}
#
## Matrix element for clustering model
#include_directories.append( os.path.join(scriptDir, "..", "common", "MatrixElements", "pp_hh_5coup", "include") )
#library_directories.append( os.path.join(scriptDir, "..", "common", "MatrixElements", "pp_hh_5coup", "build") )
#libraries.append("libme_pp_hh_5coup.a")
#
## Matrix element for MV model (with loop)
#library_directories.append("/home/fynu/swertz/scratch/Madgraph/cmssw_madgraph_lp/pp_hh_all_MV_standalone/SubProcesses/P0_gg_hh/")
#library_directories.append("/home/fynu/swertz/scratch/Madgraph/cmssw_madgraph_lp/pp_hh_all_MV_standalone/SubProcesses/P1_gg_hh/")
#library_directories.append("/home/fynu/swertz/scratch/Madgraph/cmssw_madgraph_lp/pp_hh_all_MV_standalone/SubProcesses/P2_gg_hh/")
#libraries += ["libhhWrapper0.a", "libhhWrapper1.a", "libhhWrapper2.a", "gfortran", "m", "quadmath"]
#
## Matrix element for MV model (tree level only)
#include_directories.append( os.path.join(scriptDir, "..", "common", "MatrixElements", "pp_hh_tree_MV", "include") )
#library_directories.append( os.path.join(scriptDir, "..", "common", "MatrixElements", "pp_hh_tree_MV", "build") )
#libraries.append("libme_pp_hh_tree_MV_standalone.a")
#
## Reweighting class
#include_directories.append( os.path.join(scriptDir, "..", "common") )
#headers.append("reweight_me.h")
#
#code_before_loop += """
#getHHEFTReweighter("{}");
#""".format( os.path.join(scriptDir, "..", "common", "MatrixElements") )
#
## BM to MV term reweighting
#operators_MV = ["OtG", "Otphi", "O6", "OH"]
#rwgt_base = [ "SM", "box" ] + range(2, 13)
#for base, base_name in enumerate(rwgt_base):
#    for i, op1 in enumerate(operators_MV):
#        sample_weights["base_" + base_name + "_SM_" + op1] = "getHHEFTReweighter().getMVTermME(hh_gen_H1, hh_gen_H2, -1, {}, event_alpha_QCD)/getHHEFTReweighter().getBenchmarkME(hh_gen_H1, hh_gen_H2, {}, event_alpha_QCD)".format(i, base)
#        for j, op2 in enumerate(operators_MV):
#            if i < j: continue
#            sample_weights["base_" + base_name + "_" + op1 + "_" + op2] = "getHHEFTReweighter().getMVTermME(hh_gen_H1, hh_gen_H2, {}, {}, event_alpha_QCD)/getHHEFTReweighter().getBenchmarkME(hh_gen_H1, hh_gen_H2, {}, event_alpha_QCD)".format(i, j, base)

###########################"

# Plot configuration

# lljj 
weights_lljj = ['trigeff', 'llidiso', 'pu']
categories_lljj = ["All", "MuMu", "ElEl", "MuEl"] 
plots_lljj = ["mll", "mjj", "basic", "cmva", "bdtinput", "evt", "dy_rwgt_bdt"]

# Weights
# plots_lljj += ["llidisoWeight", "trigeffWeight", "puWeight"]

#llbb
# weights_llbb = ['trigeff', 'llidiso', 'pu', 'jjbtag_heavy', 'jjbtag_light']

# FIXME: We don't have cMVAv2 SFs yet, so do not include b-tagging SFs
weights_llbb = ['trigeff', 'llidiso', 'pu']
categories_llbb = ["All", "MuMu", "ElEl", "MuEl"] 
plots_llbb = plots_lljj + ["resonant_nnoutput"]
#plots_llbb = ["bdtinput", "mjj"]

systematics = {"modifObjects" : ["nominal"]}
# systematics = {"modifObjects" : ["nominal", "jecup", "jecdown", "jerup", "jerdown"], "SF" : ["elidisoup", "elidisodown", "muidup", "muiddown", "muisoup", "muisodown", "jjbtagup", "jjbtagdown", "puup", "pudown", "trigeffup", "trigeffdown", "pdfup", "pdfdown", "scale", "scaleUncorr"]}
#systematics = {"modifObjects" : ["nominal"], "SF" : ["scale"]}

## Define binning of 2D templates for fitting
#chosen2Dbinnings = {
#        "3x25": {
#            "mjjBinning": "3, { 0, 75, 140, 13000 }",
#            "bdtNbins": 25
#        },
#    }

for systematicType in systematics.keys():
    
    for systematic in systematics[systematicType]:
        if systematicType == "modifObjects":
            objects = systematic
        else:
            objects = "nominal" #ensure that we use normal hh_objects for systematics not modifying obect such as scale factors 

        ## lljj 
        basePlotter_lljj = BasePlotter(baseObjectName = "hh_llmetjj_HWWleptons_nobtag_cmva", btagWP_str = 'nobtag', objects = objects)
        
        plots.extend(basePlotter_lljj.generatePlots(categories_lljj, "no_cut", systematic = systematic, weights = weights_lljj, requested_plots = plots_lljj))
        plots.extend(basePlotter_lljj.generatePlots(categories_lljj, "mll_cut", systematic = systematic, weights = weights_lljj, requested_plots = plots_lljj))
        plots.extend(basePlotter_lljj.generatePlots(categories_lljj, "inverted_mll_cut", systematic = systematic, weights = weights_lljj, requested_plots = plots_lljj))

        # no btag -> btagM reweighting applied ; only for DY
        plots.extend(basePlotter_lljj.generatePlots(categories_lljj, "no_cut", systematic=systematic, weights=weights_lljj + ['dy_nobtag_to_btagM_BDT'], requested_plots=plots_lljj + ['DYNobtagToBTagMWeight'], extraString='_with_nobtag_to_btagM_reweighting', prependCuts=['isDY']))
        plots.extend(basePlotter_lljj.generatePlots(categories_lljj, "mll_cut", systematic=systematic, weights=weights_lljj + ['dy_nobtag_to_btagM_BDT'], requested_plots=plots_lljj + ['DYNobtagToBTagMWeight'], extraString='_with_nobtag_to_btagM_reweighting', prependCuts=['isDY']))
        plots.extend(basePlotter_lljj.generatePlots(categories_lljj, "inverted_mll_cut", systematic = systematic, weights = weights_lljj + ['dy_nobtag_to_btagM_BDT'], requested_plots = plots_lljj + ['DYNobtagToBTagMWeight'], extraString='_with_nobtag_to_btagM_reweighting', prependCuts=['isDY']))

        code_in_loop += basePlotter_lljj.get_code_in_loop()
        code_before_loop += basePlotter_lljj.get_code_before_loop()
        code_after_loop += basePlotter_lljj.get_code_after_loop()
        
        ## llbb 
        basePlotter_llbb = BasePlotter(baseObjectName = "hh_llmetjj_HWWleptons_btagM_cmva", btagWP_str = 'medium', objects = objects)
       
        plots.extend(basePlotter_llbb.generatePlots(categories_llbb, "no_cut", systematic = systematic, weights = weights_llbb, requested_plots = plots_llbb))
        plots.extend(basePlotter_llbb.generatePlots(categories_llbb, "mll_cut", systematic = systematic, weights = weights_llbb, requested_plots = plots_llbb))
        plots.extend(basePlotter_llbb.generatePlots(categories_llbb, "inverted_mll_cut", systematic = systematic, weights = weights_llbb, requested_plots = plots_llbb))

        # if systematic == 'nominal':
            # plots.extend(basePlotter_llbb.generatePlots(categories_llbb, "mll_cut", systematic = systematic, weights = weights_llbb, requested_plots = ["llidisoWeight", ], fit2DtemplatesBinning = chosen2Dbinnings))
        
        ## With mll cut + actually cut into mjj sidebands
        #plots.extend(basePlotter_llbb.generatePlots(categories_llbb, "mjj_blind", systematic = systematic, weights = weights_llbb, requested_plots = plots_llbb))
        #plots.extend(basePlotter_llbb.generatePlots(categories_llbb, "mjj_blind", systematic = systematic, weights = weights_llbb, requested_plots = ["bdtoutput"]))
        
        ## With mll cut + select into high-BDT regions
        #plots.extend(basePlotter_llbb.generatePlots(categories_llbb, "highBDT_node_SM", systematic = systematic, weights = weights_llbb, requested_plots = plots_llbb))
        #plots.extend(basePlotter_llbb.generatePlots(categories_llbb, "highBDT_node_2", systematic = systematic, weights = weights_llbb, requested_plots = plots_llbb))

        code_in_loop += basePlotter_llbb.get_code_in_loop()
        code_before_loop += basePlotter_llbb.get_code_before_loop()
        code_after_loop += basePlotter_llbb.get_code_after_loop()
