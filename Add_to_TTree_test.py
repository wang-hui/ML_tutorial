import ROOT
from remove_flag import remove_flag
ROOT.ROOT.EnableImplicitMT()
ROOT.gInterpreter.Declare('#include "Add_to_TTree.h"')

#InputList = [500]
InputList = [500, 600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 2500, 3000]
#InputList = ["QCD_7M_stride10"]
#InputList = ["Ms2000_Mc500", "Ms4000_Mc1000", "Ms6000_Mc1600", "Ms8000_Mc2000", "Ms9000_Mc2250", "Ms8000_Mc3000"]

InputDir = "/eos/uscms/store/user/huiwang/Dijet/ML_TTree/"
OutputDir = "ML_TTree_test/"

LvecJ1 = "pt_ordered_jet1_pt, pt_ordered_jet1_eta, pt_ordered_jet1_phi, pt_ordered_jet1_m"
LvecJ2 = LvecJ1.replace("jet1", "jet2")
LvecJ3 = LvecJ1.replace("jet1", "jet3")
LvecJ4 = LvecJ1.replace("jet1", "jet4")

SaveList = ["Mass", "fourjetmasstev", "Truth_QSMD", "dRi",
    "pt_ordered_jet1_pt", "pt_ordered_jet1_eta", "pt_ordered_jet1_phi", "pt_ordered_jet1_m",
    "pt_ordered_jet2_pt", "pt_ordered_jet2_eta", "pt_ordered_jet2_phi", "pt_ordered_jet2_m",
    "pt_ordered_jet3_pt", "pt_ordered_jet3_eta", "pt_ordered_jet3_phi", "pt_ordered_jet3_m",
    "pt_ordered_jet4_pt", "pt_ordered_jet4_eta", "pt_ordered_jet4_phi", "pt_ordered_jet4_m",
    "pt_ordered_jet1_px", "pt_ordered_jet1_py", "pt_ordered_jet1_pz", "pt_ordered_jet1_E",
    "pt_ordered_jet2_px", "pt_ordered_jet2_py", "pt_ordered_jet2_pz", "pt_ordered_jet2_E",
    "pt_ordered_jet3_px", "pt_ordered_jet3_py", "pt_ordered_jet3_pz", "pt_ordered_jet3_E",
    "pt_ordered_jet4_px", "pt_ordered_jet4_py", "pt_ordered_jet4_pz", "pt_ordered_jet4_E",

    "P1high_Mjj_div_M4j", "P1low_Mjj_div_M4j",
    "P2high_Mjj_div_M4j", "P2low_Mjj_div_M4j",
    "P3high_Mjj_div_M4j", "P3low_Mjj_div_M4j",
    "P1high_dR", "P1low_dR",
    "P2high_dR", "P2low_dR",
    "P3high_dR", "P3low_dR",
]

def mass_in_str (String):
    Mass = "0"
    if "Mc" in String:
        Mass = String.split("Mc")[1]
        Mass = Mass.split(".")[0]
    return Mass

for Input in InputList:
    FileName = "tree_ML_MCRun2_"
    if isinstance(Input, str):
        FileName = FileName + Input  + ".root"
    else:
        FileName = FileName + str(Input) + "GeV.root"

    print("processing", FileName)
    RDF = ROOT.RDataFrame("tree_ML", InputDir + FileName)

    if isinstance(Input, str):
        Mass = mass_in_str(Input)
        RDF = RDF.Define("Mass", Mass)
    else:
        RDF = RDF.Define("Mass", str(Input))
        RDF = RDF.Define("weight", str(1))

    ### single jet lvec ###
    RDF = RDF.Define("j1lvec", "ROOT::Math::PtEtaPhiMVector(" + LvecJ1 + ")")
    RDF = RDF.Define("j2lvec", "ROOT::Math::PtEtaPhiMVector(" + LvecJ2 + ")")
    RDF = RDF.Define("j3lvec", "ROOT::Math::PtEtaPhiMVector(" + LvecJ3 + ")")
    RDF = RDF.Define("j4lvec", "ROOT::Math::PtEtaPhiMVector(" + LvecJ4 + ")")

    for ji in ["1", "2", "3", "4"]:
        RDF = RDF.Define("pt_ordered_jet" + ji + "_px", "j" + ji + "lvec.Px()")
        RDF = RDF.Define("pt_ordered_jet" + ji + "_py", "j" + ji + "lvec.Py()")
        RDF = RDF.Define("pt_ordered_jet" + ji + "_pz", "j" + ji + "lvec.Pz()")
        RDF = RDF.Define("pt_ordered_jet" + ji + "_E", "j" + ji + "lvec.E()")

    RDF = RDF.Define("SortedJets", "sort_dijet_mass(j1lvec, j2lvec, j3lvec, j4lvec)")

    ### lvec of single jet in dijet ###
    RDF = RDF.Define("P1high_j1", "SortedJets[0]")
    RDF = RDF.Define("P1high_j2", "SortedJets[1]")
    RDF = RDF.Define("P1low_j1", "SortedJets[2]")
    RDF = RDF.Define("P1low_j2", "SortedJets[3]")
    RDF = RDF.Define("P2high_j1", "SortedJets[4]")
    RDF = RDF.Define("P2high_j2", "SortedJets[5]")
    RDF = RDF.Define("P2low_j1", "SortedJets[6]")
    RDF = RDF.Define("P2low_j2", "SortedJets[7]")
    RDF = RDF.Define("P3high_j1", "SortedJets[8]")
    RDF = RDF.Define("P3high_j2", "SortedJets[9]")
    RDF = RDF.Define("P3low_j1", "SortedJets[10]")
    RDF = RDF.Define("P3low_j2", "SortedJets[11]")

    for Pair in ["P1", "P2", "P3"]:
        ### mass variables ###
        RDF = RDF.Define(Pair + "high_Mjj_div_M4j", "Mjj_msorted" + Pair + "_high / 1000 / fourjetmasstev")
        RDF = RDF.Define(Pair + "low_Mjj_div_M4j", "Mjj_msorted" + Pair + "_low / 1000 / fourjetmasstev")

        RDF = RDF.Define(Pair + "high_dR", "ROOT::Math::VectorUtil::DeltaR(" +
                        Pair + "high_j1, " + Pair + "high_j2)")
        RDF = RDF.Define(Pair + "low_dR", "ROOT::Math::VectorUtil::DeltaR(" +
                        Pair + "low_j1, " + Pair + "low_j2)")

    RDF = RDF.Define("Truth_QSMD", "get_truth_qsmd(Mass, Mjj_msortedP1_high, Mjj_msortedP1_low, Mjj_msortedP2_high, Mjj_msortedP2_low, Mjj_msortedP3_high, Mjj_msortedP3_low)")
    RDF = RDF.Define("dRi", "get_dRi(Mjj_avg_dRpairing_GeV, Mjj_msortedP1_high, Mjj_msortedP1_low, Mjj_msortedP2_high, Mjj_msortedP2_low, Mjj_msortedP3_high, Mjj_msortedP3_low)")

    OutCols = ROOT.vector("string")()
    for Col in SaveList: OutCols.push_back(Col)

    RDF.Snapshot("tree_ML", OutputDir + FileName, OutCols)

    remove_flag(OutputDir + FileName)
