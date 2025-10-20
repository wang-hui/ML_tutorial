typedef ROOT::Math::PtEtaPhiMVector lvec;
typedef std::pair<lvec, lvec> lvecPair;

std::pair<lvecPair, lvecPair> make_dijet_pair (const lvec & J1, const lvec & J2, const lvec & J3, const lvec & J4) {
    auto Dijet1 = std::make_pair(J1, J2);
    auto Dijet2 = std::make_pair(J3, J4);

    if ((J1+J2).M() > (J3+J4).M()) return std::make_pair(Dijet1, Dijet2);
    else return std::make_pair(Dijet2, Dijet1);
}

bool bigger_mass (const std::pair<lvecPair, lvecPair> & Pair1, const std::pair<lvecPair, lvecPair> & Pair2) {
    return (Pair1.first.first + Pair1.first.second).M() > (Pair2.first.first + Pair2.first.second).M();
}

std::vector<lvec> sort_dijet_mass (const lvec & J1, const lvec & J2, const lvec & J3, const lvec & J4) {
    auto Pair1 = make_dijet_pair(J1, J2, J3, J4);
    auto Pair2 = make_dijet_pair(J1, J3, J2, J4);
    auto Pair3 = make_dijet_pair(J1, J4, J2, J3);
    std::vector<std::pair<lvecPair, lvecPair>> VecOfPairOfPair = {Pair1, Pair2, Pair3};
    std::sort(VecOfPairOfPair.begin(), VecOfPairOfPair.end(), bigger_mass);
    std::vector<lvec> SortedJets;
    for(int i = 0; i < 3; i++) {
        SortedJets.push_back(VecOfPairOfPair.at(i).first.first);
        SortedJets.push_back(VecOfPairOfPair.at(i).first.second);
        SortedJets.push_back(VecOfPairOfPair.at(i).second.first);
        SortedJets.push_back(VecOfPairOfPair.at(i).second.second);
    }
    return SortedJets;
}

int min_index (float a, float b, float c) {
    std::vector<float> Input = {a, b, c};
    auto Iter = std::min_element(Input.begin(), Input.end());
    return std::distance(Input.begin(), Iter);
}

std::pair<int, float> max_index_val (float a, float b, float c) {
    std::vector<float> Input = {a, b, c};
    auto Iter = std::max_element(Input.begin(), Input.end());
    int Index = std::distance(Input.begin(), Iter);
    float Val = Input.at(Index);
    return std::make_pair(Index, Val);
}

int get_truth_qsmd (float Mass, float Mjj_msortedP1_high, float Mjj_msortedP1_low, float Mjj_msortedP2_high, float Mjj_msortedP2_low, float Mjj_msortedP3_high, float Mjj_msortedP3_low) {
    float P1QSMD = (Mass - Mjj_msortedP1_high)*(Mass - Mjj_msortedP1_high) + (Mass - Mjj_msortedP1_low)*(Mass - Mjj_msortedP1_low);
    float P2QSMD = (Mass - Mjj_msortedP2_high)*(Mass - Mjj_msortedP2_high) + (Mass - Mjj_msortedP2_low)*(Mass - Mjj_msortedP2_low);
    float P3QSMD = (Mass - Mjj_msortedP3_high)*(Mass - Mjj_msortedP3_high) + (Mass - Mjj_msortedP3_low)*(Mass - Mjj_msortedP3_low);
    return min_index(P1QSMD, P2QSMD, P3QSMD);
}

int get_dRi (float Mjj_avg_dRpairing_GeV, float Mjj_msortedP1_high, float Mjj_msortedP1_low, float Mjj_msortedP2_high, float Mjj_msortedP2_low, float Mjj_msortedP3_high, float Mjj_msortedP3_low) {
    float P1dRMD = fabs((Mjj_msortedP1_high + Mjj_msortedP1_low) / 2 - Mjj_avg_dRpairing_GeV);
    float P2dRMD = fabs((Mjj_msortedP2_high + Mjj_msortedP2_low) / 2 - Mjj_avg_dRpairing_GeV);
    float P3dRMD = fabs((Mjj_msortedP3_high + Mjj_msortedP3_low) / 2 - Mjj_avg_dRpairing_GeV);
    return min_index(P1dRMD, P2dRMD, P3dRMD);
}

template <typename T>
T col_index (T a, T b, T c, int index) {
    std::vector<T> Input = {a, b, c};
    return Input.at(index);
}

template <typename T>
std::vector<T> to_vec (T a, T b, T c, T d) {
    std::vector<T> Input = {a, b, c, d};
    return Input;
}

float QCD_weight(float Par0, float Par1, float Par2, float Low, float High, float Tar, float Var) {
    TF1 MyFunc("MyFunc", "[0]*exp([1]*x) / pow(x, [2])");
    MyFunc.SetParameter(0, Par0);
    MyFunc.SetParameter(1, Par1);
    MyFunc.SetParameter(2, Par2);
    if (Var < Low) Var = Low;
    if (Var > High) Var = High;
    return Tar / MyFunc.Eval(Var);
}
